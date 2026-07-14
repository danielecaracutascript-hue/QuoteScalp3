from strategy.pullback import PullbackFilter
from strategy.trend import TrendFilter
from strategy.momentum import MomentumFilter
from strategy.slope import SlopeFilter
from strategy.m5_confirmation import M5ConfirmationFilter
from strategy.candle import CandleFilter
from strategy.breakout import BreakoutFilter
from strategy.rsi import RSIFilter
from strategy.adx import ADXFilter
from strategy.volume import VolumeFilter
from strategy.atr import ATRFilter
from strategy.spread import SpreadFilter
from strategy.volatility import VolatilityFilter
from strategy.setup_quality import SetupQualityFilter


import MetaTrader5 as mt5
import pandas as pd

import config

from indicators.indicator_engine import IndicatorEngine




class StrategyEngine:



    def __init__(self, symbol):

        self.symbol = symbol
        self.indicators = IndicatorEngine()
        self.last_df15 = None





    def analizza(self):


        print("\n==============================")
        print("=== STRATEGY ENGINE PRO ===")
        print("==============================")



        score_buy = 0
        score_sell = 0

        log = []



        # ==========================
        # MARKET DATA
        # ==========================


        rates15 = mt5.copy_rates_from_pos(
            self.symbol,
            mt5.TIMEFRAME_M15,
            0,
            config.TREND_CANDLES
        )


        rates5 = mt5.copy_rates_from_pos(
            self.symbol,
            mt5.TIMEFRAME_M5,
            0,
            config.CONFIRMATION_CANDLES
        )


        rates1 = mt5.copy_rates_from_pos(
            self.symbol,
            mt5.TIMEFRAME_M1,
            0,
            config.ENTRY_CANDLES
        )



        if (
            rates15 is None
            or rates5 is None
            or rates1 is None
        ):

            return None





        df15 = pd.DataFrame(rates15)

        df5 = pd.DataFrame(rates5)

        df1 = pd.DataFrame(rates1)





        # ==========================
        # INDICATORS
        # ==========================


        df15 = self.indicators.calculate(df15)

        df5 = self.indicators.calculate(df5)

        df1 = self.indicators.calculate(df1)



        if (
            df15.empty
            or df5.empty
            or df1.empty
        ):

            return None


        # Dataframe M15 (con indicatori) esposto per riuso esterno
        # (es. DecisionEngine per il calcolo del regime di mercato),
        # evitando un secondo fetch ridondante da MT5

        self.last_df15 = df15





        # ultime candele chiuse


        m15 = df15.iloc[-2]

        m5 = df5.iloc[-2]

        m1 = df1.iloc[-2]






        # ==========================
        # SCORE HANDLER
        # ==========================


        def add(result):


            nonlocal score_buy
            nonlocal score_sell


            score_buy += result["buy"]

            score_sell += result["sell"]


            log.extend(
                result["log"]
            )






        # ==========================
        # TREND M15
        # ==========================


        trend_result = TrendFilter.evaluate(
            m15
        )


        trend = trend_result["trend"]

        trend_strength = trend_result["trend_strength"]


        add(trend_result)



        if trend is None:


            return {

                "symbol":self.symbol,

                "score":0,

                "signal":"NONE",

                "log":[
                    "Nessun trend M15"
                ],

                "buy_score":0,

                "sell_score":0
            }





        # ==========================
        # M5 CONFIRMATION
        # ==========================


        if config.M5_CONFIRMATION_REQUIRED:


            add(
                M5ConfirmationFilter.evaluate(
                    trend,
                    m5
                )
            )




        # ==========================
        # SETUP QUALITY
        # ==========================


        setup_quality_result = SetupQualityFilter.evaluate(
            trend,
            m15,
            m5,
            m1
        )


        setup_quality = setup_quality_result["quality"]

        setup_quality_status = setup_quality_result["status"]


        log.extend(
            setup_quality_result["log"]
        )







        # ==========================
        # ENTRY M1 FILTERS
        # ==========================


        add(
            PullbackFilter.evaluate(
                trend,
                m1
            )
        )


        add(
            MomentumFilter.evaluate(
                trend,
                m1
            )
        )


        add(
            SlopeFilter.evaluate(
                trend,
                trend_strength,
                m1,
                df1
            )
        )



        add(
            CandleFilter.evaluate(
                trend,
                m1
            )
        )



        add(
            RSIFilter.evaluate(
                trend,
                m1
            )
        )



        add(
            ADXFilter.evaluate(
                trend,
                m1
            )
        )



        add(
            VolumeFilter.evaluate(
                trend,
                m1
            )
        )



        add(
            ATRFilter.evaluate(
                trend,
                m1,
                df1
            )
        )



        add(
            VolatilityFilter.evaluate(
                df1,
                m1,
                trend
            )
        )



        add(
            BreakoutFilter.evaluate(
                df1,
                m1,
                trend
            )
        )



        add(
            SpreadFilter.evaluate(
                trend,
                self.symbol
            )
        )







        # ==========================
        # SETUP PREMIUM BONUS
        # ==========================


        if config.SETUP_COMPLETO_ENABLED:



            setup_buy = (
                score_buy >= 75
                and trend == "BUY"
            )


            setup_sell = (
                score_sell >= 60
                and trend == "SELL"
            )



            if setup_buy:


                score_buy += config.SETUP_COMPLETO_SCORE


                log.append(
                    f"Setup completo BUY +{config.SETUP_COMPLETO_SCORE}"
                )



            elif setup_sell:


                score_sell += config.SETUP_COMPLETO_SCORE


                log.append(
                    f"Setup completo SELL +{config.SETUP_COMPLETO_SCORE}"
                )







        # ==========================
        # ADAPTIVE M5 SCORE
        # ==========================


        final_min_score = config.MIN_SCORE


        if config.M5_CONFIRMATION_REQUIRED:


            if (
                trend == "BUY"
                and m5.EMA20 < m5.EMA50
            ):


                final_min_score = config.MIN_SCORE_M5_OPPOSITE



                log.append(
                    "M5 contro trend: conferma più difficile"
                )



            elif (
                trend == "SELL"
                and m5.EMA20 > m5.EMA50
            ):


                final_min_score = config.MIN_SCORE_M5_OPPOSITE


                log.append(
                    "M5 contro trend: conferma più difficile"
                )



        # ==========================
        # ADAPTIVE SETUP QUALITY
        # ==========================


        if setup_quality_status == "BAD":


            final_min_score = max(
                final_min_score,
                config.MIN_SCORE_LOW_QUALITY
            )


            log.append(
                f"Setup quality bassa ({setup_quality}): soglia più severa"
            )







        # ==========================
        # CAP SCORE (max 100)
        # ==========================

        score_buy = min(score_buy, 100)

        score_sell = min(score_sell, 100)



        # ==========================
        # DEBUG
        # ==========================


        if config.DEBUG:


            print("\n=== DEBUG INDICATORI ===")

            print(
                f"EMA20 M15: {m15.EMA20}"
            )

            print(
                f"EMA50 M15: {m15.EMA50}"
            )

            print(
                f"EMA200 M15: {m15.EMA200}"
            )


            print("\n=== M5 CONFIRMATION ===")

            print(
                f"EMA20 M5: {m5.EMA20}"
            )

            print(
                f"EMA50 M5: {m5.EMA50}"
            )


            print("\n=== ENTRY M1 ===")

            print(
                f"EMA20 M1: {m1.EMA20}"
            )

            print(
                f"EMA50 M1: {m1.EMA50}"
            )

            print(
                f"RSI14: {m1.RSI14:.2f}"
            )

            print(
                f"ADX14: {m1.ADX14:.2f}"
            )

            print(
                f"ATR14: {m1.ATR14}"
            )

            print(
                f"VOLUME: {m1.tick_volume}"
            )

            print(
                f"VOL MEDIA: {m1.VOL20}"
            )


            print("\n=== SETUP QUALITY ===")

            print(
                f"Quality: {setup_quality} ({setup_quality_status})"
            )



            print("\n=== SCORE ===")

            print(
                f"BUY: {score_buy}"
            )

            print(
                f"SELL: {score_sell}"
            )

            print(
                f"MIN SCORE RICHIESTO: {final_min_score}"
            )



            print("\n=== LOG ===")

            for voce in log:

                print(
                    ">",
                    voce
                )








        # ==========================
        # SIGNAL
        # ==========================


        if score_buy >= final_min_score:


            signal = "BUY"

            score = score_buy



        elif score_sell >= final_min_score:


            signal = "SELL"

            score = score_sell



        else:


            signal = "NONE"

            score = max(
                score_buy,
                score_sell
            )







        return {


            "symbol":self.symbol,

            "score":score,

            "signal":signal,

            "log":log,

            "buy_score":score_buy,

            "sell_score":score_sell

        }
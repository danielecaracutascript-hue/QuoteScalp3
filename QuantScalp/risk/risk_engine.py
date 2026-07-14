import MetaTrader5 as mt5

import config


class RiskEngine:

    def __init__(
        self,
        risk_percent=config.RISK_PERCENT,
        max_lot=config.MAX_LOT,
        atr_multiplier_sl=config.ATR_SL_MULTIPLIER,
        reward_ratio=config.REWARD_RATIO
    ):

        self.risk_percent = risk_percent
        self.max_lot = max_lot
        self.atr_multiplier_sl = atr_multiplier_sl
        self.reward_ratio = reward_ratio



    def calcola_rischio(self, symbol, atr):

        print("\n======================")
        print("=== RISK ENGINE ===")
        print("======================")


        # ======================
        # ACCOUNT
        # ======================

        account = mt5.account_info()

        if account is None:
            raise Exception(
                "Account MT5 non disponibile"
            )


        balance = account.balance



        # ======================
        # RISCHIO €
        # ======================

        rischio_valuta = (
            balance *
            self.risk_percent /
            100
        )



        # ======================
        # INFO SIMBOLO
        # ======================

        info = mt5.symbol_info(symbol)

        if info is None:
            raise Exception(
                "Simbolo non trovato"
            )



        # ======================
        # PIP SIZE (dinamico)
        # ======================

        # Broker a 5 o 3 cifre decimali: 1 pip = 10 * point
        # Broker a 4 o 2 cifre decimali: 1 pip = point

        if info.digits in (3, 5):

            pip_size = info.point * 10

        else:

            pip_size = info.point



        # ======================
        # STOP LOSS ATR
        # ======================

        stop_distance = (
            atr *
            self.atr_multiplier_sl
        )


        stop_pips = (
            stop_distance /
            pip_size
        )


        # minimo sicurezza scalping

        if stop_pips < 5:

            stop_pips = 5



        # ======================
        # PIP VALUE PER LOTTO (dinamico)
        # ======================

        # trade_tick_value = valore in valuta del conto di 1 tick
        # per 1 lotto standard, già convertito da MT5 nel cambio corrente

        tick_value = info.trade_tick_value

        tick_size = (
            info.trade_tick_size
            if info.trade_tick_size
            else info.point
        )

        if not tick_value or tick_value <= 0:

            raise Exception(
                f"trade_tick_value non disponibile per {symbol}"
            )


        pip_value_per_lot = (
            tick_value *
            (pip_size / tick_size)
        )



        # ======================
        # LOT CALCULATION
        # ======================

        lotto = (
            rischio_valuta /
            (
                stop_pips *
                pip_value_per_lot
            )
        )


        # Arrotondamento al passo del broker

        volume_step = info.volume_step

        lotto = (
            int(lotto / volume_step)
            *
            volume_step
        )


        # limite minimo broker

        volume_min = info.volume_min

        lotto_sotto_minimo = lotto < volume_min

        if lotto_sotto_minimo:

            lotto = volume_min

            print(
                f"ATTENZIONE: lotto calcolato sotto il minimo broker "
                f"({volume_min}). Uso il minimo: il rischio reale sarà "
                f"superiore a quello configurato ({self.risk_percent}%)."
            )


        # limite massimo (config / broker)

        volume_max = min(
            self.max_lot,
            info.volume_max
        )

        if lotto > volume_max:

            lotto = volume_max



        # ======================
        # TAKE PROFIT
        # ======================

        take_profit_pips = (
            stop_pips *
            self.reward_ratio
        )


        return {

            "symbol": symbol,

            "balance": balance,

            "risk_money": round(
                rischio_valuta,
                2
            ),

            "atr": atr,

            "pip_size": pip_size,

            "stop_loss_pips": round(
                stop_pips,
                1
            ),

            "take_profit_pips": round(
                take_profit_pips,
                1
            ),

            "lot": lotto,

            "lot_below_minimum": lotto_sotto_minimo

        }
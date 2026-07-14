from risk.risk_engine import RiskEngine
from core.market_regime import MarketRegime
from strategy.strategy_engine import StrategyEngine

import config



class DecisionEngine:



    def __init__(self, symbol):

        self.symbol = symbol

        self.strategy = StrategyEngine(symbol)

        self.regime_engine = MarketRegime()

        self.risk_engine = RiskEngine()



    def valuta(self):


        print("\n==========================")
        print("=== DECISION ENGINE ===")
        print("==========================")



        # ==========================
        # STRATEGIA
        # (fa anche il fetch dei dati M15/M5/M1 da MT5
        # e calcola gli indicatori)
        # ==========================


        risultato = self.strategy.analizza()


        if risultato is None:

            print(
                "❌ Nessun dato mercato"
            )

            return None



        score = risultato["score"]

        segnale = risultato["signal"]



        print(
            f"Score strategia: {score}/100"
        )


        print(
            f"Segnale strategia: {segnale}"
        )



        # ==========================
        # REGIME
        # (riusa il dataframe M15 già scaricato e calcolato
        # dalla strategia, senza un secondo fetch da MT5)
        # ==========================


        df15 = self.strategy.last_df15

        regime = self.regime_engine.analyze(
            df15
        )


        print(
            f"Regime mercato: {regime}"
        )



        # ==========================
        # DECISIONE
        # ==========================


        decisione = "WAIT"

        motivo = ""



        if score < config.MIN_SCORE:


            motivo = (
                f"Score insufficiente "
                f"({score}/{config.MIN_SCORE})"
            )



        elif regime == "RANGE":


            motivo = (
                "Mercato laterale"
            )



        elif regime == "TREND_UP":


            if segnale == "BUY":

                decisione = "BUY"

                motivo = (
                    "Trend rialzista + "
                    "segnale BUY confermato"
                )


            else:

                motivo = (
                    "Trend UP senza conferma"
                )



        elif regime == "TREND_DOWN":


            if segnale == "SELL":

                decisione = "SELL"

                motivo = (
                    "Trend ribassista + "
                    "segnale SELL confermato"
                )


            else:

                motivo = (
                    "Trend DOWN senza conferma"
                )



        elif regime == "COMPRESSION":

            motivo = (
                "Compressione volatilità"
            )



        elif regime == "HIGH_VOLATILITY":

            motivo = (
                "Volatilità troppo alta"
            )



        # ==========================
        # RISK
        # ==========================


        rischio = None


        if decisione in ["BUY", "SELL"]:


            atr = df15["ATR14"].iloc[-1]


            rischio = self.risk_engine.calcola_rischio(
                self.symbol,
                atr
            )



        print(
            f"Decisione finale: {decisione}"
        )


        print(
            f"Motivo: {motivo}"
        )



        return {


            "symbol": self.symbol,

            "regime": regime,

            "score": score,

            "signal": segnale,

            "decisione": decisione,

            "motivo": motivo,

            "rischio": rischio,

            "buy_score": risultato.get(
                "buy_score",
                0
            ),

            "sell_score": risultato.get(
                "sell_score",
                0
            )

        }
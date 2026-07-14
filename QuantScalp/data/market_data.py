import MetaTrader5 as mt5
import pandas as pd


class MarketData:


    def __init__(self):

        if not mt5.initialize():

            raise Exception(
                f"Errore inizializzazione MT5: {mt5.last_error()}"
            )



    def get_rates(
        self,
        symbol,
        timeframe=mt5.TIMEFRAME_M1,
        bars=200
    ):

        """
        Recupera dati storici MT5.

        timeframe:
        M1  -> scalping ingresso
        M15 -> trend
        H1  -> regime
        """


        info = mt5.symbol_info(symbol)


        if info is None:

            raise Exception(
                f"Simbolo {symbol} non trovato"
            )



        if not info.visible:

            if not mt5.symbol_select(
                symbol,
                True
            ):

                raise Exception(
                    f"Impossibile attivare {symbol}"
                )



        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0,
            bars
        )



        if rates is None or len(rates) == 0:

            raise Exception(
                f"Nessun dato ricevuto: {mt5.last_error()}"
            )



        df = pd.DataFrame(rates)



        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )



        return df




    def get_data(
        self,
        symbol,
        timeframe=mt5.TIMEFRAME_M15,
        bars=300
    ):

        """
        Metodo principale usato dal DecisionEngine.

        Default:
        M15 = trend principale
        """


        return self.get_rates(
            symbol=symbol,
            timeframe=timeframe,
            bars=bars
        )




    def get_multi_timeframe(
        self,
        symbol
    ):

        """
        Analisi multi timeframe:

        M1:
        ingresso preciso

        M15:
        trend principale

        H1:
        regime generale
        """


        return {


            "M1": self.get_rates(
                symbol,
                mt5.TIMEFRAME_M1,
                250
            ),


            "M15": self.get_rates(
                symbol,
                mt5.TIMEFRAME_M15,
                300
            ),


            "H1": self.get_rates(
                symbol,
                mt5.TIMEFRAME_H1,
                300
            )

        }
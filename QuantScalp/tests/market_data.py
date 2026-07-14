import MetaTrader5 as mt5
import pandas as pd


class MarketData:

    def __init__(self):
        pass

    def get_rates(self, symbol, timeframe, bars):

        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0,
            bars
        )

        if rates is None:
            return None

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(df["time"], unit="s")

        return df
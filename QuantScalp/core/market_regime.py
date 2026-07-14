import pandas as pd


class MarketRegime:


    def analyze(self, df):


        volatility_now = df["ATR14"].iloc[-1]


        volatility_avg = (
            df["ATR14"]
            .rolling(50)
            .mean()
            .iloc[-1]
        )


        ema50 = df["EMA50"].iloc[-1]

        ema200 = df["EMA200"].iloc[-1]



        # compressione

        if volatility_now < volatility_avg * 0.6:

            return "COMPRESSION"



        # volatilità estrema

        if volatility_now > volatility_avg * 2:

            return "HIGH_VOLATILITY"



        # trend

        if ema50 > ema200:

            return "TREND_UP"



        if ema50 < ema200:

            return "TREND_DOWN"



        return "RANGE"
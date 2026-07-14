import pandas as pd
import numpy as np


class IndicatorEngine:


    @staticmethod
    def ema(df, period):

        return df["close"].ewm(
            span=period,
            adjust=False
        ).mean()



    @staticmethod
    def plus_minus_di(df, period=14):

        # ==========================
        # DIRECTIONAL MOVEMENT
        # ==========================

        up_move = df["high"].diff()

        down_move = -df["low"].diff()

        plus_dm = np.where(
            (up_move > down_move) & (up_move > 0),
            up_move,
            0.0
        )

        minus_dm = np.where(
            (down_move > up_move) & (down_move > 0),
            down_move,
            0.0
        )

        # ==========================
        # TRUE RANGE
        # ==========================

        high_low = df["high"] - df["low"]

        high_close = np.abs(
            df["high"] - df["close"].shift()
        )

        low_close = np.abs(
            df["low"] - df["close"].shift()
        )

        tr = pd.concat(
            [
                high_low,
                high_close,
                low_close
            ],
            axis=1
        ).max(axis=1)

        # ==========================
        # SMOOTHING DI WILDER
        # (approssimato con EWM, alpha = 1/period)
        # ==========================

        atr_smooth = tr.ewm(
            alpha=1 / period,
            adjust=False
        ).mean()

        plus_dm_smooth = pd.Series(
            plus_dm,
            index=df.index
        ).ewm(
            alpha=1 / period,
            adjust=False
        ).mean()

        minus_dm_smooth = pd.Series(
            minus_dm,
            index=df.index
        ).ewm(
            alpha=1 / period,
            adjust=False
        ).mean()

        plus_di = 100 * (
            plus_dm_smooth / (atr_smooth + 0.000001)
        )

        minus_di = 100 * (
            minus_dm_smooth / (atr_smooth + 0.000001)
        )

        return plus_di, minus_di



    @staticmethod
    def atr(df, period=14):

        high_low = df["high"] - df["low"]

        high_close = np.abs(
            df["high"] - df["close"].shift()
        )

        low_close = np.abs(
            df["low"] - df["close"].shift()
        )


        tr = pd.concat(
            [
                high_low,
                high_close,
                low_close
            ],
            axis=1
        ).max(axis=1)


        return tr.rolling(period).mean()



    @staticmethod
    def rsi(df, period=14):

        delta = df["close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)


        avg_gain = (
            gain
            .rolling(period)
            .mean()
        )

        avg_loss = (
            loss
            .rolling(period)
            .mean()
        )


        rs = (
            avg_gain /
            (avg_loss + 0.000001)
        )


        return 100 - (
            100 /
            (1 + rs)
        )



    @staticmethod
    def adx(df, period=14):

        plus = df["high"].diff()

        minus = -df["low"].diff()


        plus[plus < 0] = 0
        minus[minus < 0] = 0


        dx = (
            abs(plus - minus)
            /
            (plus + minus + 0.000001)
        )


        return (
            dx
            .rolling(period)
            .mean()
            *
            100
        )



    def calculate(self, df):

        df = df.copy()


        # Trend

        df["EMA20"] = self.ema(
            df,
            20
        )


        df["EMA50"] = self.ema(
            df,
            50
        )


        df["EMA200"] = self.ema(
            df,
            200
        )


        # Volatilità

        df["ATR14"] = self.atr(
            df,
            14
        )


        # Momentum

        df["RSI14"] = self.rsi(
            df,
            14
        )


        # Forza trend

        df["ADX14"] = self.adx(
            df,
            14
        )


        # Direzione trend (+DI / -DI)

        df["PLUS_DI"], df["MINUS_DI"] = self.plus_minus_di(
            df,
            14
        )


        # Volume medio

        df["VOL20"] = (
            df["tick_volume"]
            .rolling(20)
            .mean()
        )


        # Breakout livelli

        df["HIGH20"] = (
            df["high"]
            .rolling(20)
            .max()
        )


        df["LOW20"] = (
            df["low"]
            .rolling(20)
            .min()
        )


        df.dropna(
            inplace=True
        )


        return df
import MetaTrader5 as mt5
import pandas as pd
import numpy as np


def calcola_atr(df, periodo=14):
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())

    ranges = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    )

    true_range = ranges.max(axis=1)

    return true_range.rolling(periodo).mean()


def identifica_regime_mercato(symbol):

    rates = mt5.copy_rates_from_pos(
        symbol,
        mt5.TIMEFRAME_H1,
        0,
        50
    )

    if rates is None:
        return "DATI NON DISPONIBILI"

    df = pd.DataFrame(rates)

    df["atr"] = calcola_atr(df)

    std_recente = df["close"].iloc[-10:].std()
    std_storica = df["close"].std()

    ema20 = (
        df["close"]
        .ewm(span=20)
        .mean()
    )

    pendenza = (
        (ema20.iloc[-1] - ema20.iloc[-5])
        /
        ema20.iloc[-5]
    ) * 100


    if std_recente < (std_storica * 0.6):
        return "VOLATILITY_COMPRESSION"

    elif (
        abs(pendenza) > 0.15
        and df["atr"].iloc[-1] > df["atr"].mean()
    ):
        return "TREND_DAY"

    else:
        return "RANGE_DAY"



if __name__ == "__main__":

    print("\n=== MARKET REGIME TEST ===")

    if not mt5.initialize():
        print(
            "Errore connessione MT5:",
            mt5.last_error()
        )
        quit()


    symbol = "EURUSD"

    regime = identifica_regime_mercato(symbol)


    print(f"Simbolo: {symbol}")
    print(f"Regime attuale: {regime}")


    mt5.shutdown()
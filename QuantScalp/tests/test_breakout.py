import MetaTrader5 as mt5
import pandas as pd


def controlla_breakout(symbol):

    rates = mt5.copy_rates_from_pos(
        symbol,
        mt5.TIMEFRAME_M1,
        0,
        50
    )

    df = pd.DataFrame(rates)

    candela = df.iloc[-2]

    massimo_precedente = (
        df.iloc[-17:-2]["high"]
        .max()
    )

    minimo_precedente = (
        df.iloc[-17:-2]["low"]
        .min()
    )


    if candela.close > massimo_precedente:
        return "BREAKOUT BUY"

    elif candela.close < minimo_precedente:
        return "BREAKOUT SELL"

    else:
        return "NESSUN BREAKOUT"



if __name__ == "__main__":

    mt5.initialize()

    risultato = controlla_breakout("EURUSD")

    print("\n=== BREAKOUT TEST ===")
    print(risultato)

    mt5.shutdown()
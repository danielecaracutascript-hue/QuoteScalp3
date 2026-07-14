import MetaTrader5 as mt5

from data.market_data import MarketData
from indicators.indicator_engine import IndicatorEngine


MT5_PATH = r"C:\Program Files\MetaTrader\terminal64.exe"

LOGIN = 763175
PASSWORD = "R_2dDcFu"
SERVER = "TenTrade-Server"


print("Connessione MT5...")


if not mt5.initialize(
    path=MT5_PATH,
    login=LOGIN,
    password=PASSWORD,
    server=SERVER
):
    print("Errore MT5:", mt5.last_error())
    quit()


print("✅ MT5 collegato")


market = MarketData()


df = market.get_rates(
    "EURUSD",
    mt5.TIMEFRAME_M1,
    250
)


# Calcolo indicatori

df["EMA50"] = IndicatorEngine.ema(
    df,
    50
)

df["EMA200"] = IndicatorEngine.ema(
    df,
    200
)

df["ATR14"] = IndicatorEngine.atr(
    df,
    14
)


print("\nULTIME CANDELE CON INDICATORI:")
print(
    df[
        [
            "time",
            "close",
            "EMA50",
            "EMA200",
            "ATR14"
        ]
    ].tail(10)
)


mt5.shutdown()
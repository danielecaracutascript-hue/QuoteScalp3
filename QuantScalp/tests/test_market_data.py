import MetaTrader5 as mt5

from data.market_data import MarketData


MT5_PATH = r"C:\Program Files\MetaTrader\terminal64.exe"

LOGIN = 763175
PASSWORD = "R_2dDcFu"

SERVER = "TenTrade-Server"


if not mt5.initialize(
    path=MT5_PATH,
    login=LOGIN,
    password=PASSWORD,
    server=SERVER
):
    print(mt5.last_error())
    quit()


market = MarketData()

df = market.get_rates(
    "EURUSD",
    mt5.TIMEFRAME_M1,
    20
)

print(df)

mt5.shutdown()
import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader\terminal64.exe"

LOGIN = 763175
PASSWORD = "R_2dDcFu"
SERVER = "TenTrade-Server"

print("Connessione a MT5...")

if not mt5.initialize(
    path=MT5_PATH,
    login=LOGIN,
    password=PASSWORD,
    server=SERVER
):
    print("❌ Errore:", mt5.last_error())
    quit()

print("✅ Connessione riuscita!")

account = mt5.account_info()

print("\n=== ACCOUNT ===")
print(account)

mt5.shutdown()
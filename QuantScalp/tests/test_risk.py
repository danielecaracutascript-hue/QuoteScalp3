import MetaTrader5 as mt5

from risk.risk_engine import RiskEngine


if __name__ == "__main__":


    if not mt5.initialize():

        print(mt5.last_error())

        quit()



    engine = RiskEngine(
        risk_percent=0.5
    )


    risultato = engine.calcola_rischio(
        "EURUSD",
        atr=0.00008
    )


    print("\nRISULTATO RISK:")
    print(risultato)



    mt5.shutdown()
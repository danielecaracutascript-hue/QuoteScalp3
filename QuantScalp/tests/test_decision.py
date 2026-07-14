import MetaTrader5 as mt5
from core.decision_engine import DecisionEngine


if __name__ == "__main__":


    print("\n==========================")
    print("=== DECISION ENGINE TEST ===")
    print("==========================\n")


    # Connessione MT5

    if not mt5.initialize():

        print(
            "Errore inizializzazione MT5:",
            mt5.last_error()
        )

        quit()



    symbol = "EURUSD"


    engine = DecisionEngine(symbol)


    risultato = engine.valuta()



    if risultato is None:

        print(
            "\n❌ Nessun risultato"
        )

        mt5.shutdown()
        quit()



    print("\n==========================")
    print("=== RISULTATO FINALE ===")
    print("==========================")



    print(
        "Symbol:",
        risultato["symbol"]
    )


    print(
        "Regime:",
        risultato["regime"]
    )


    print(
        "Score:",
        risultato["score"],
        "/100"
    )


    print(
        "Signal:",
        risultato["signal"]
    )


    print(
        "Decisione:",
        risultato["decisione"]
    )


    print(
        "Motivo:",
        risultato["motivo"]
    )



    # ==========================
    # DEBUG STRATEGIA
    # ==========================

    print("\n==========================")
    print("=== DEBUG STRATEGIA ===")
    print("==========================")


    print(
        "BUY SCORE:",
        risultato.get(
            "buy_score",
            "non disponibile"
        )
    )


    print(
        "SELL SCORE:",
        risultato.get(
            "sell_score",
            "non disponibile"
        )
    )



    # ==========================
    # RISK
    # ==========================

    print("\n==========================")
    print("=== RISK ===")
    print("==========================")


    print(
        risultato.get(
            "rischio",
            None
        )
    )



    mt5.shutdown()
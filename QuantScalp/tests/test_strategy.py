import MetaTrader5 as mt5

from strategy.strategy_engine import StrategyEngine



if __name__ == "__main__":


    print("\n==============================")
    print("=== STRATEGY ENGINE TEST ===")
    print("==============================\n")



    # ==========================
    # CONNESSIONE MT5
    # ==========================

    if not mt5.initialize():

        print(
            "Errore MT5:",
            mt5.last_error()
        )

        quit()



    # ==========================
    # SIMBOLO
    # ==========================

    symbol = "EURUSD"



    # ==========================
    # ENGINE
    # ==========================

    engine = StrategyEngine(
        symbol
    )



    risultato = engine.analizza()



    if risultato is None:


        print(
            "❌ Nessun risultato strategico"
        )

        mt5.shutdown()

        quit()



    # ==========================
    # RISULTATO PRINCIPALE
    # ==========================


    print(
        "Symbol:",
        risultato.get(
            "symbol"
        )
    )


    print(
        "Score:",
        risultato.get(
            "score"
        ),
        "/100"
    )


    print(
        "Signal:",
        risultato.get(
            "signal"
        )
    )



    # ==========================
    # DEBUG SCORE
    # ==========================


    print("\n=== DEBUG SCORE ===")


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
    # LOG STRATEGIA
    # ==========================


    print("\nDettagli:")


    log = risultato.get(
        "log",
        []
    )


    if len(log) == 0:


        print(
            "Nessun criterio soddisfatto"
        )


    else:


        for x in log:

            print(
                " >",
                x
            )



    print("\n==============================")



    mt5.shutdown()
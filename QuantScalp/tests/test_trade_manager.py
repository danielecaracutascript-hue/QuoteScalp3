import MetaTrader5 as mt5

from trade.trade_manager import TradeManager



if __name__ == "__main__":


    print("\n==========================")
    print("=== TRADE MANAGER TEST ===")
    print("==========================\n")


    print(
        "ATTENZIONE: questo test controlla le posizioni aperte "
        "sul conto collegato al terminale MT5 e, se trova posizioni "
        "aperte da questo bot (stesso magic number) in profitto "
        "sufficiente, MODIFICA REALMENTE il loro stop loss "
        "(trailing stop).\n"
        "Assicurati di essere connesso a un conto DEMO prima "
        "di continuare.\n"
    )


    risposta = input(
        "Sei sicuro di voler procedere? (scrivi 'si' per continuare): "
    )


    if risposta.strip().lower() != "si":

        print("Test annullato.")

        quit()



    # ==========================
    # CONNESSIONE MT5
    # ==========================

    if not mt5.initialize():

        print(
            "Errore inizializzazione MT5:",
            mt5.last_error()
        )

        quit()



    account = mt5.account_info()

    if account is None:

        print(
            "Impossibile leggere l'account:",
            mt5.last_error()
        )

        mt5.shutdown()
        quit()



    print(
        f"Connesso al conto: {account.login} "
        f"({'DEMO' if account.trade_mode == 0 else 'REALE / ATTENZIONE'})"
    )


    if account.trade_mode != 0:

        risposta2 = input(
            "\n⚠️ QUESTO NON SEMBRA UN CONTO DEMO. "
            "Vuoi davvero continuare? (scrivi 'si' per confermare): "
        )

        if risposta2.strip().lower() != "si":

            print("Test annullato per sicurezza.")

            mt5.shutdown()
            quit()



    symbol = "EURUSD"


    # ==========================
    # STATO POSIZIONI PRIMA
    # ==========================

    posizioni = mt5.positions_get(symbol=symbol)

    n_posizioni = len(posizioni) if posizioni is not None else 0

    print(
        f"\nPosizioni aperte trovate su {symbol}: {n_posizioni}"
    )


    if n_posizioni == 0:

        print(
            "\nNessuna posizione aperta: non c'è nulla da gestire.\n"
            "Apri prima una posizione (es. con "
            "'python -m tests.test_order_manager') e rilancia questo test."
        )

        mt5.shutdown()
        quit()



    for p in posizioni:

        tipo = "BUY" if p.type == 0 else "SELL"

        print(
            f"  ticket={p.ticket} tipo={tipo} magic={p.magic} "
            f"apertura={p.price_open} sl={p.sl} tp={p.tp} "
            f"profitto={p.profit}"
        )



    conferma = input(
        "\nProcedere con il controllo/aggiornamento del trailing "
        "stop su queste posizioni? (scrivi 'si' per confermare): "
    )


    if conferma.strip().lower() != "si":

        print("Operazione annullata dall'utente.")

        mt5.shutdown()
        quit()



    # ==========================
    # TRADE MANAGER
    # ==========================

    risultati = TradeManager.gestisci_posizioni(symbol)


    print("\n==========================")
    print("=== RISULTATI ===")
    print("==========================")

    if not risultati:

        print(
            "Nessuna posizione del bot trovata "
            "(magic number diverso o nessuna posizione)."
        )

    else:

        for r in risultati:

            print(r)



    mt5.shutdown()
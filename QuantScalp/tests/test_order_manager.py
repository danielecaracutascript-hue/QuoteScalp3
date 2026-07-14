import MetaTrader5 as mt5

from core.decision_engine import DecisionEngine
from execution.order_manager import OrderManager



if __name__ == "__main__":


    print("\n==========================")
    print("=== ORDER MANAGER TEST ===")
    print("==========================\n")


    print(
        "ATTENZIONE: questo test, se la decisione risulta "
        "BUY o SELL, invierà un ORDINE REALE sul conto "
        "collegato al terminale MT5 attualmente aperto.\n"
        "Assicurati di essere connesso a un conto DEMO "
        "prima di continuare.\n"
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
    # DECISION ENGINE
    # ==========================

    engine = DecisionEngine(symbol)

    risultato = engine.valuta()


    if risultato is None:

        print("\n❌ Nessun risultato dalla decisione")

        mt5.shutdown()
        quit()



    print("\n==========================")
    print("=== RISULTATO DECISIONE ===")
    print("==========================")

    print(
        "Decisione:",
        risultato["decisione"]
    )

    print(
        "Motivo:",
        risultato["motivo"]
    )

    print(
        "Score:",
        risultato["score"],
        "/ 100"
    )



    # ==========================
    # ORDER MANAGER
    # ==========================

    if risultato["decisione"] not in ("BUY", "SELL"):

        print(
            "\nNessun ordine da aprire: il segnale non è "
            "abbastanza forte in questo momento (WAIT)."
        )

        mt5.shutdown()
        quit()



    print(
        f"\nRischio calcolato: lotto={risultato['rischio']['lot']} "
        f"SL={risultato['rischio']['stop_loss_pips']} pips "
        f"TP={risultato['rischio']['take_profit_pips']} pips"
    )


    conferma = input(
        f"\nConfermi l'invio dell'ordine {risultato['decisione']} "
        f"su {symbol}? (scrivi 'si' per confermare): "
    )


    if conferma.strip().lower() != "si":

        print("Ordine annullato dall'utente.")

        mt5.shutdown()
        quit()



    esito = OrderManager.apri_ordine(risultato)


    print("\n==========================")
    print("=== ESITO ORDINE ===")
    print("==========================")

    print(esito)



    mt5.shutdown()
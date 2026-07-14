import time

import MetaTrader5 as mt5

import config

from core.decision_engine import DecisionEngine
from execution.order_manager import OrderManager
from trade.trade_manager import TradeManager



def conta_posizioni_bot(symbol):

    """Conta quante posizioni ha aperto questo bot (stesso magic number)."""

    posizioni = mt5.positions_get(symbol=symbol)

    if posizioni is None:

        return 0


    return len(
        [
            p
            for p in posizioni
            if p.magic == config.MAGIC_NUMBER
        ]
    )



def ciclo_segnale(engine, symbol):

    """Valuta un eventuale nuovo trade e lo apre se le condizioni lo permettono."""

    posizioni_aperte = conta_posizioni_bot(symbol)

    if posizioni_aperte >= config.MAX_OPEN_POSITIONS:

        print(
            f"\n[SEGNALE] Limite posizioni raggiunto "
            f"({posizioni_aperte}/{config.MAX_OPEN_POSITIONS}), "
            f"nessuna nuova valutazione."
        )

        return


    risultato = engine.valuta()


    if risultato is None:

        print(
            "\n[SEGNALE] Nessun dato disponibile in questo ciclo."
        )

        return


    if risultato["decisione"] in ("BUY", "SELL"):

        OrderManager.apri_ordine(risultato)



def ciclo_trailing(symbol):

    """Controlla e aggiorna il trailing stop sulle posizioni aperte."""

    TradeManager.gestisci_posizioni(symbol)



def main():

    print("\n==========================")
    print("=== QUANTSCALP BOT ===")
    print("==========================\n")


    if not mt5.initialize():

        print(
            "Errore inizializzazione MT5:",
            mt5.last_error()
        )

        return


    symbol = config.DEFAULT_SYMBOL

    engine = DecisionEngine(symbol)


    print(
        f"Bot avviato su {symbol}.\n"
        f"Ricerca segnali ogni {config.SIGNAL_LOOP_SECONDS}s, "
        f"trailing stop ogni {config.TRAILING_LOOP_SECONDS}s.\n"
        f"Premi CTRL+C per fermare.\n"
    )


    prossimo_segnale = 0.0

    prossimo_trailing = 0.0


    try:

        while True:


            ora = time.time()


            if ora >= prossimo_trailing:

                try:

                    ciclo_trailing(symbol)

                except Exception as errore:

                    print(
                        f"❌ Errore nel ciclo trailing: {errore}"
                    )

                prossimo_trailing = ora + config.TRAILING_LOOP_SECONDS



            if ora >= prossimo_segnale:

                try:

                    ciclo_segnale(engine, symbol)

                except Exception as errore:

                    print(
                        f"❌ Errore nel ciclo segnale: {errore}"
                    )

                prossimo_segnale = ora + config.SIGNAL_LOOP_SECONDS



            time.sleep(1)



    except KeyboardInterrupt:

        print(
            "\n\nInterruzione richiesta dall'utente. Arresto in corso..."
        )


    finally:

        mt5.shutdown()

        print("MT5 disconnesso. Bot fermato.")



if __name__ == "__main__":

    main()
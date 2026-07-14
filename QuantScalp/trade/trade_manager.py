import MetaTrader5 as mt5

import config

from trade.position import Position
from trade.exit_manager import ExitManager



class TradeManager:



    @staticmethod
    def gestisci_posizioni(symbol):

        """
        Scorre tutte le posizioni aperte su un simbolo, filtra solo
        quelle aperte da questo bot (stesso magic number) e applica
        la logica di trailing stop a ciascuna.
        """

        print("\n==========================")
        print("=== TRADE MANAGER ===")
        print("==========================")


        posizioni_mt5 = mt5.positions_get(symbol=symbol)


        if posizioni_mt5 is None or len(posizioni_mt5) == 0:

            print("Nessuna posizione aperta")

            return []


        info = mt5.symbol_info(symbol)

        if info is None:

            print(
                f"❌ Simbolo {symbol} non trovato"
            )

            return []


        tick = mt5.symbol_info_tick(symbol)

        if tick is None:

            print(
                "❌ Tick non disponibile"
            )

            return []


        pip_size = ExitManager.pip_size(info)


        risultati = []


        for pos_raw in posizioni_mt5:


            # gestiamo solo le posizioni aperte da questo bot

            if pos_raw.magic != config.MAGIC_NUMBER:

                continue


            position = Position(pos_raw)


            prezzo_attuale = (
                tick.bid
                if position.is_buy
                else tick.ask
            )


            nuovo_sl = ExitManager.calcola_nuovo_sl(
                position,
                prezzo_attuale,
                pip_size
            )


            esito = {

                "ticket": position.ticket,

                "tipo": "BUY" if position.is_buy else "SELL",

                "azione": "nessuna"

            }


            if nuovo_sl is not None:


                nuovo_sl = round(
                    nuovo_sl,
                    info.digits
                )


                successo = ExitManager.aggiorna_sl(
                    position,
                    nuovo_sl
                )


                esito["azione"] = "trailing_sl"

                esito["nuovo_sl"] = nuovo_sl

                esito["successo"] = successo


            else:


                print(
                    f"Posizione {position.ticket} "
                    f"({'BUY' if position.is_buy else 'SELL'}): "
                    f"nessun aggiornamento SL necessario"
                )


            risultati.append(esito)


        return risultati
import MetaTrader5 as mt5

import config



class ExitManager:



    @staticmethod
    def pip_size(info):

        # Broker a 5 o 3 cifre decimali: 1 pip = 10 * point
        # Broker a 4 o 2 cifre decimali: 1 pip = point

        if info.digits in (3, 5):

            return info.point * 10

        return info.point



    @staticmethod
    def calcola_nuovo_sl(position, prezzo_attuale, pip_size):

        """
        Calcola il nuovo stop loss per il trailing, dato il prezzo
        attuale (bid per posizioni BUY, ask per posizioni SELL).

        Ritorna None se non c'è nulla da aggiornare.

        Funzione pura (nessuna chiamata a MT5), pensata per essere
        facilmente testabile in isolamento.
        """

        if not config.TRAILING_ENABLED:

            return None


        step = (
            config.TRAILING_STEP_PIPS *
            pip_size
        )


        if position.is_buy:


            profit_pips = (
                (prezzo_attuale - position.price_open) /
                pip_size
            )


            if profit_pips < config.TRAILING_START_PIPS:

                return None


            nuovo_sl = (
                prezzo_attuale -
                (config.TRAILING_DISTANCE_PIPS * pip_size)
            )


            sl_attuale = (
                position.sl
                if position.sl
                else -float("inf")
            )


            # aggiorna solo se migliora lo SL (mai verso il basso)
            # di almeno TRAILING_STEP_PIPS

            if nuovo_sl > sl_attuale + step:

                return nuovo_sl


            return None



        elif position.is_sell:


            profit_pips = (
                (position.price_open - prezzo_attuale) /
                pip_size
            )


            if profit_pips < config.TRAILING_START_PIPS:

                return None


            nuovo_sl = (
                prezzo_attuale +
                (config.TRAILING_DISTANCE_PIPS * pip_size)
            )


            sl_attuale = (
                position.sl
                if position.sl
                else float("inf")
            )


            # aggiorna solo se migliora lo SL (mai verso l'alto)
            # di almeno TRAILING_STEP_PIPS

            if nuovo_sl < sl_attuale - step:

                return nuovo_sl


            return None


        return None



    @staticmethod
    def aggiorna_sl(position, nuovo_sl):

        """Invia a MT5 la modifica dello stop loss di una posizione aperta."""

        request = {

            "action": mt5.TRADE_ACTION_SLTP,

            "position": position.ticket,

            "symbol": position.symbol,

            "sl": nuovo_sl,

            "tp": position.tp,

            "magic": config.MAGIC_NUMBER

        }


        result = mt5.order_send(request)


        if result is None:

            print(
                f"❌ order_send (trailing) ha restituito None: "
                f"{mt5.last_error()}"
            )

            return False


        if result.retcode != mt5.TRADE_RETCODE_DONE:

            print(
                f"❌ Trailing SL rifiutato: retcode={result.retcode} "
                f"comment={result.comment}"
            )

            return False


        print(
            f"✅ Trailing SL aggiornato: ticket={position.ticket} "
            f"nuovo_sl={nuovo_sl}"
        )

        return True
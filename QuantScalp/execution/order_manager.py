import MetaTrader5 as mt5

import config



class OrderManager:



    @staticmethod
    def _scegli_filling_mode(info):

        # ATTENZIONE: symbol_info().filling_mode è una bitmask che usa
        # le costanti SYMBOL_FILLING_FOK / SYMBOL_FILLING_IOC (diverse
        # dalle costanti ORDER_FILLING_FOK / IOC / RETURN, che invece
        # sono il valore da mettere nella richiesta d'ordine)

        modalita = info.filling_mode

        if modalita & mt5.SYMBOL_FILLING_FOK:

            return mt5.ORDER_FILLING_FOK

        elif modalita & mt5.SYMBOL_FILLING_IOC:

            return mt5.ORDER_FILLING_IOC

        else:

            return mt5.ORDER_FILLING_RETURN



    @staticmethod
    def apri_ordine(decisione_result):

        print("\n==========================")
        print("=== ORDER MANAGER ===")
        print("==========================")


        # ==========================
        # VALIDAZIONE INPUT
        # ==========================

        if decisione_result is None:

            print(
                "❌ Nessun risultato dalla decisione"
            )

            return None


        decisione = decisione_result.get("decisione")

        if decisione not in ("BUY", "SELL"):

            print(
                f"Nessun ordine da aprire (decisione: {decisione})"
            )

            return None


        rischio = decisione_result.get("rischio")

        if rischio is None:

            print(
                "❌ Dati di rischio mancanti, ordine annullato"
            )

            return None


        symbol = decisione_result["symbol"]

        lot = rischio["lot"]

        stop_loss_pips = rischio["stop_loss_pips"]

        take_profit_pips = rischio["take_profit_pips"]

        pip_size = rischio["pip_size"]



        # ==========================
        # INFO SIMBOLO / TICK
        # ==========================

        info = mt5.symbol_info(symbol)

        if info is None:

            print(
                f"❌ Simbolo {symbol} non trovato"
            )

            return None


        if not info.visible:

            if not mt5.symbol_select(symbol, True):

                print(
                    f"❌ Impossibile selezionare {symbol}"
                )

                return None


        tick = mt5.symbol_info_tick(symbol)

        if tick is None:

            print(
                "❌ Tick non disponibile"
            )

            return None



        # ==========================
        # PREZZO / SL / TP
        # ==========================

        if decisione == "BUY":

            order_type = mt5.ORDER_TYPE_BUY

            price = tick.ask

            sl = price - (stop_loss_pips * pip_size)

            tp = price + (take_profit_pips * pip_size)


        else:

            order_type = mt5.ORDER_TYPE_SELL

            price = tick.bid

            sl = price + (stop_loss_pips * pip_size)

            tp = price - (take_profit_pips * pip_size)


        digits = info.digits

        price = round(price, digits)
        sl = round(sl, digits)
        tp = round(tp, digits)



        # controllo distanza minima stop imposta dal broker

        stop_level_price = (
            info.trade_stops_level *
            info.point
        )

        distanza_sl = abs(price - sl)

        if (
            stop_level_price > 0
            and distanza_sl < stop_level_price
        ):

            print(
                f"⚠️ Distanza SL ({distanza_sl:.5f}) sotto il minimo "
                f"broker ({stop_level_price:.5f}): il broker potrebbe "
                f"rifiutare l'ordine"
            )



        # ==========================
        # RICHIESTA ORDINE
        # ==========================

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": symbol,

            "volume": lot,

            "type": order_type,

            "price": price,

            "sl": sl,

            "tp": tp,

            "deviation": config.DEVIATION,

            "magic": config.MAGIC_NUMBER,

            "comment": config.ORDER_COMMENT,

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": OrderManager._scegli_filling_mode(info)

        }


        print(
            f"Invio ordine: {decisione} {symbol} "
            f"lot={lot} price={price} sl={sl} tp={tp}"
        )


        result = mt5.order_send(request)


        if result is None:

            print(
                "❌ order_send ha restituito None:",
                mt5.last_error()
            )

            return {

                "success": False,

                "retcode": None,

                "error": mt5.last_error(),

                "request": request

            }



        if result.retcode != mt5.TRADE_RETCODE_DONE:

            print(
                f"❌ Ordine rifiutato: retcode={result.retcode} "
                f"comment={result.comment}"
            )

            return {

                "success": False,

                "retcode": result.retcode,

                "error": result.comment,

                "request": request

            }



        print(
            f"✅ Ordine eseguito: ticket={result.order} "
            f"volume={result.volume} prezzo={result.price}"
        )


        return {

            "success": True,

            "retcode": result.retcode,

            "ticket": result.order,

            "volume": result.volume,

            "price": result.price,

            "sl": sl,

            "tp": tp,

            "symbol": symbol,

            "type": decisione,

            "request": request

        }
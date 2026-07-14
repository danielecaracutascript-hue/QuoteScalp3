import MetaTrader5 as mt5


class SpreadFilter:

    @staticmethod
    def evaluate(trend, symbol):

        score_buy = 0
        score_sell = 0

        log = []

        tick = mt5.symbol_info_tick(symbol)
        info = mt5.symbol_info(symbol)

        if tick is None or info is None:

            return {

                "buy": 0,
                "sell": 0,
                "log": []

            }

        spread = (
            tick.ask -
            tick.bid
        ) / info.point / 10

        if spread <= 1:

            if trend == "BUY":

                score_buy = 10

            elif trend == "SELL":

                score_sell = 10

            log.append(
                f"Spread buono {spread:.1f} +10"
            )

        return {

            "buy": score_buy,
            "sell": score_sell,
            "log": log

        }
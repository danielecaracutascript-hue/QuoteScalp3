import config


class ATRFilter:

    @staticmethod
    def evaluate(trend, m1, df1):

        score_buy = 0
        score_sell = 0

        log = []

        # ==========================
        # MEDIA ATR (stessa finestra usata da VolatilityFilter)
        # ==========================

        atr_avg = (
            df1["ATR14"]
            .rolling(config.ATR_AVERAGE_PERIOD)
            .mean()
            .iloc[-1]
        )

        if m1.ATR14 > atr_avg:

            if trend == "BUY":

                score_buy = config.ATR_SCORE

            elif trend == "SELL":

                score_sell = config.ATR_SCORE

            log.append(
                f"ATR sufficiente +{config.ATR_SCORE}"
            )

        return {

            "buy": score_buy,
            "sell": score_sell,
            "log": log

        }
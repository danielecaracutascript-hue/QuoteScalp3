import config


class MomentumFilter:


    @staticmethod
    def evaluate(trend, m1):

        score_buy = 0
        score_sell = 0

        log = []


        if trend == "BUY":


            if m1.EMA20 > m1.EMA50:

                score_buy = config.MOMENTUM_SCORE

                log.append(
                    f"Momentum BUY EMA20 > EMA50 +{score_buy}"
                )


        elif trend == "SELL":


            if m1.EMA20 < m1.EMA50:

                score_sell = config.MOMENTUM_SCORE

                log.append(
                    f"Momentum SELL EMA20 < EMA50 +{score_sell}"
                )


        return {

            "buy": score_buy,

            "sell": score_sell,

            "log": log

        }
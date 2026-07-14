import config


class PullbackFilter:


    @staticmethod
    def evaluate(trend, m1):

        buy = 0
        sell = 0

        log = []


        if trend == "BUY":


            if (
                35 < m1.RSI14 < 50
                and m1.close >= m1.EMA50 * 0.9998
            ):

                buy = config.PULLBACK_SCORE

                log.append(
                    f"Pullback BUY EMA50 +{buy}"
                )


        elif trend == "SELL":


            if (
                50 < m1.RSI14 < 65
                and m1.close <= m1.EMA50 * 1.0002
            ):

                sell = config.PULLBACK_SCORE

                log.append(
                    f"Pullback SELL EMA50 +{sell}"
                )


        return {

            "buy": buy,
            "sell": sell,
            "log": log

        }
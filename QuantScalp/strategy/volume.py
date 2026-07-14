import config


class VolumeFilter:

    @staticmethod
    def evaluate(trend, m1):

        score_buy = 0
        score_sell = 0

        log = []

        if m1.tick_volume > m1.VOL20:

            if trend == "BUY":

                score_buy = config.VOLUME_SCORE

            elif trend == "SELL":

                score_sell = config.VOLUME_SCORE

            log.append(
                f"Volume sopra media +{config.VOLUME_SCORE}"
            )

        return {

            "buy": score_buy,
            "sell": score_sell,
            "log": log

        }
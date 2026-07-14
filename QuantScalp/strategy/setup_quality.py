import config


class SetupQualityFilter:


    @staticmethod
    def evaluate(trend, m15, m5, m1):

        quality = 100

        log = []


        # ==========================
        # RSI ESTREMO
        # ==========================

        if trend == "BUY":

            if m1.RSI14 >= config.RSI_OVERBOUGHT_LIMIT:

                quality -= config.RSI_EXTREME_PENALTY

                log.append(
                    f"RSI troppo alto penalità -{config.RSI_EXTREME_PENALTY}"
                )


        elif trend == "SELL":

            if m1.RSI14 <= config.RSI_OVERSOLD_LIMIT:

                quality -= config.RSI_EXTREME_PENALTY

                log.append(
                    f"RSI troppo basso penalità -{config.RSI_EXTREME_PENALTY}"
                )



        # ==========================
        # M5 CONTRARIO
        # ==========================

        # NB: M5_OPPOSITE_PENALTY è già negativo in config,
        # quindi va sommato (non sottratto) per ridurre la qualità

        if trend == "BUY":

            if m5.EMA20 < m5.EMA50:

                quality += config.M5_OPPOSITE_PENALTY

                log.append(
                    f"M5 contrario penalità {config.M5_OPPOSITE_PENALTY}"
                )


        elif trend == "SELL":

            if m5.EMA20 > m5.EMA50:

                quality += config.M5_OPPOSITE_PENALTY

                log.append(
                    f"M5 contrario penalità {config.M5_OPPOSITE_PENALTY}"
                )



        # ==========================
        # VOLUME
        # ==========================

        if m1.tick_volume < (
            m1.VOL20 * config.MIN_VOLUME_FACTOR
        ):

            quality -= config.LOW_VOLUME_PENALTY

            log.append(
                f"Volume basso penalità -{config.LOW_VOLUME_PENALTY}"
            )



        # ==========================
        # ADX
        # ==========================

        if m1.ADX14 >= config.ADX_STRONG:

            log.append(
                "ADX forte qualità OK"
            )



        # ==========================
        # RISULTATO
        # ==========================


        if quality >= config.SETUP_QUALITY_MIN:

            status = "GOOD"

        else:

            status = "BAD"



        return {

            "quality": quality,

            "status": status,

            "log": log

        }
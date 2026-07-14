import config


class VolatilityFilter:


    @staticmethod
    def evaluate(df, candle, trend):

        score_buy = 0
        score_sell = 0

        log = []


        # ATR corrente

        atr_now = candle.ATR14


        # ATR medio

        atr_avg = (
            df["ATR14"]
            .rolling(config.ATR_AVERAGE_PERIOD)
            .mean()
            .iloc[-1]
        )



        # ==========================
        # VOLATILITA' FAVOREVOLE
        # ==========================

        if atr_now > atr_avg:


            if trend == "BUY":

                score_buy = config.VOLATILITY_SCORE

                log.append(
                    f"Volatilità favorevole BUY +{config.VOLATILITY_SCORE}"
                )


            elif trend == "SELL":

                score_sell = config.VOLATILITY_SCORE

                log.append(
                    f"Volatilità favorevole SELL +{config.VOLATILITY_SCORE}"
                )



        # ==========================
        # COMPRESSIONE
        # ==========================

        elif atr_now < atr_avg * config.ATR_COMPRESSION_FACTOR:


            log.append(
                "Volatilità bassa: evitare ingresso"
            )



        # ==========================
        # VOLATILITA' ECCESSIVA
        # ==========================

        elif atr_now > atr_avg * config.ATR_EXTREME_FACTOR:


            log.append(
                "Volatilità eccessiva"
            )



        return {

            "buy": score_buy,

            "sell": score_sell,

            "log": log

        }
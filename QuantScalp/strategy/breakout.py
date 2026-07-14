import config


class BreakoutFilter:


    @staticmethod
    def evaluate(df, candle, trend):

        score_buy = 0
        score_sell = 0

        log = []


        # ultime N candele (config.BREAKOUT_PERIOD) escluse quella corrente

        period = config.BREAKOUT_PERIOD

        high_period = (
            df.iloc[-(period + 2):-2]["high"]
            .max()
        )


        low_period = (
            df.iloc[-(period + 2):-2]["low"]
            .min()
        )


        range_size = high_period - low_period



        # ==========================
        # BREAKOUT BUY
        # ==========================

        if trend == "BUY":


            # breakout vero

            if candle.close > high_period:


                score_buy = config.BREAKOUT_SCORE


                log.append(
                    f"Breakout BUY confermato +{config.BREAKOUT_SCORE}"
                )



            # prezzo vicino alla rottura

            elif candle.close > high_period - (range_size * 0.15):


                score_buy = config.PRE_BREAKOUT_SCORE


                log.append(
                    f"Pre-breakout BUY +{config.PRE_BREAKOUT_SCORE}"
                )



        # ==========================
        # BREAKOUT SELL
        # ==========================


        elif trend == "SELL":


            # breakout vero

            if candle.close < low_period:


                score_sell = config.BREAKOUT_SCORE


                log.append(
                    f"Breakout SELL confermato +{config.BREAKOUT_SCORE}"
                )



            # prezzo vicino alla rottura

            elif candle.close < low_period + (range_size * 0.15):


                score_sell = config.PRE_BREAKOUT_SCORE


                log.append(
                    f"Pre-breakout SELL +{config.PRE_BREAKOUT_SCORE}"
                )



        return {


            "buy": score_buy,

            "sell": score_sell,

            "log": log

        }
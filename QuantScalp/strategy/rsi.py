import config



class RSIFilter:


    @staticmethod
    def evaluate(trend, m1):


        score_buy = 0
        score_sell = 0

        log = []


        rsi = m1.RSI14



        # ==========================
        # BUY
        # ==========================

        if trend == "BUY":


            # RSI troppo basso
            # possibile caduta ancora in corso

            if rsi <= config.RSI_OVERSOLD:


                score_buy = config.RSI_EXTREME_SCORE


                log.append(
                    f"RSI BUY estremo {rsi:.1f} {score_buy}"
                )



            # zona ideale

            elif (
                config.RSI_IDEAL_LOW
                <= rsi
                <= config.RSI_IDEAL_HIGH
            ):


                score_buy = config.RSI_IDEAL_SCORE


                log.append(
                    f"RSI BUY ideale {rsi:.1f} +{score_buy}"
                )



            # zona accettabile

            elif (
                config.RSI_BUY_MIN
                < rsi
                <
                config.RSI_BUY_MAX
            ):


                score_buy = config.RSI_NORMAL_SCORE


                log.append(
                    f"RSI BUY valido {rsi:.1f} +{score_buy}"
                )



            else:


                log.append(
                    f"RSI BUY non valido {rsi:.1f}"
                )






        # ==========================
        # SELL
        # ==========================

        elif trend == "SELL":



            # RSI troppo alto

            if rsi >= config.RSI_OVERBOUGHT:


                score_sell = config.RSI_EXTREME_SCORE


                log.append(
                    f"RSI SELL estremo {rsi:.1f} {score_sell}"
                )



            elif (
                config.RSI_SELL_MIN
                <
                rsi
                <
                config.RSI_SELL_MAX
            ):


                score_sell = config.RSI_NORMAL_SCORE


                log.append(
                    f"RSI SELL valido {rsi:.1f} +{score_sell}"
                )



            else:


                log.append(
                    f"RSI SELL non valido {rsi:.1f}"
                )





        return {


            "buy": score_buy,

            "sell": score_sell,

            "log": log

        }
import config


class M5ConfirmationFilter:


    @staticmethod
    def evaluate(trend, m5):


        score_buy = 0
        score_sell = 0

        log = []



        # ==========================
        # CONTROLLO DATI
        # ==========================


        if m5.ATR14 <= 0:


            return {

                "buy": 0,

                "sell": 0,

                "log": [
                    "M5 ATR non valido"
                ]

            }




        atr = m5.ATR14




        # ==========================
        # TREND BUY
        # ==========================


        if trend == "BUY":



            # M5 conferma M15

            if m5.EMA20 > m5.EMA50:


                score_buy = config.M5_CONFIRMATION_SCORE


                log.append(
                    f"M5 conferma BUY +{score_buy}"
                )



            # M5 contrario

            else:



                distanza = (
                    m5.EMA50 - m5.EMA20
                ) / atr




                # piccolo ritardo del M5

                if distanza < 1.0:


                    score_buy = -5


                    log.append(
                        f"M5 leggermente contrario BUY -5 ({distanza:.2f} ATR)"
                    )



                # vero controtrend

                else:


                    score_buy = config.M5_OPPOSITE_PENALTY


                    log.append(
                        f"M5 forte controtrend BUY {score_buy} ({distanza:.2f} ATR)"
                    )







        # ==========================
        # TREND SELL
        # ==========================


        elif trend == "SELL":



            # M5 conferma M15

            if m5.EMA20 < m5.EMA50:


                score_sell = config.M5_CONFIRMATION_SCORE


                log.append(
                    f"M5 conferma SELL +{score_sell}"
                )



            # M5 contrario

            else:



                distanza = (
                    m5.EMA20 - m5.EMA50
                ) / atr





                # piccolo ritardo del M5

                if distanza < 0.5:


                    score_sell = -5


                    log.append(
                        f"M5 leggermente contrario SELL -5 ({distanza:.2f} ATR)"
                    )



                # vero controtrend

                else:


                    score_sell = config.M5_OPPOSITE_PENALTY


                    log.append(
                        f"M5 forte controtrend SELL {score_sell} ({distanza:.2f} ATR)"
                    )







        # ==========================
        # RETURN
        # ==========================


        return {


            "buy": score_buy,

            "sell": score_sell,

            "log": log

        }
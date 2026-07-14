import config



class CandleFilter:



    @staticmethod
    def evaluate(trend, m1):


        score_buy = 0
        score_sell = 0

        log = []



        # ==========================
        # DATI CANDELA
        # ==========================


        open_price = m1.open
        close_price = m1.close
        high_price = m1.high
        low_price = m1.low


        ema20 = m1.EMA20



        body = abs(close_price - open_price)

        candle_range = high_price - low_price



        if candle_range <= 0:


            return {

                "buy": 0,
                "sell": 0,
                "log": [
                    "Candela range non valido"
                ]

            }




        body_ratio = body / candle_range



        upper_wick = high_price - max(
            open_price,
            close_price
        )


        lower_wick = min(
            open_price,
            close_price
        ) - low_price





        # ==========================
        # BUY
        # ==========================


        if trend == "BUY":



            # candela rialzista

            if close_price > open_price:



                # chiusura sopra EMA20

                if close_price > ema20:



                    # corpo significativo

                    if body_ratio >= 0.40:



                        score_buy += config.CANDLE_SCORE


                        log.append(
                            f"Candela BUY confermata +{config.CANDLE_SCORE}"
                        )



                    else:


                        log.append(
                            f"Candela BUY debole corpo {body_ratio:.2f}"
                        )



                else:


                    log.append(
                        "Candela BUY sotto EMA20"
                    )



            else:


                log.append(
                    "Candela BUY rossa"
                )





            # ==========================
            # ENGULFING BUY
            # ==========================


            if (
                close_price > open_price
                and body_ratio >= 0.60
            ):


                score_buy += config.ENGULFING_SCORE


                log.append(
                    f"Engulfing BUY +{config.ENGULFING_SCORE}"
                )





            # ==========================
            # RIFIUTO RIBASSO
            # ==========================


            if lower_wick > body * 1.5:


                score_buy += config.REJECTION_SCORE


                log.append(
                    f"Rifiuto ribasso BUY +{config.REJECTION_SCORE}"
                )







        # ==========================
        # SELL
        # ==========================


        elif trend == "SELL":



            if close_price < open_price:



                if close_price < ema20:



                    if body_ratio >= 0.40:



                        score_sell += config.CANDLE_SCORE


                        log.append(
                            f"Candela SELL confermata +{config.CANDLE_SCORE}"
                        )



                    else:


                        log.append(
                            f"Candela SELL debole corpo {body_ratio:.2f}"
                        )



                else:


                    log.append(
                        "Candela SELL sopra EMA20"
                    )



            else:


                log.append(
                    "Candela SELL verde"
                )





            # ==========================
            # ENGULFING SELL
            # ==========================


            if (
                close_price < open_price
                and body_ratio >= 0.60
            ):


                score_sell += config.ENGULFING_SCORE


                log.append(
                    f"Engulfing SELL +{config.ENGULFING_SCORE}"
                )





            # ==========================
            # RIFIUTO RIALZO
            # ==========================


            if upper_wick > body * 1.5:


                score_sell += config.REJECTION_SCORE


                log.append(
                    f"Rifiuto rialzo SELL +{config.REJECTION_SCORE}"
                )





        return {


            "buy": score_buy,

            "sell": score_sell,

            "log": log

        }
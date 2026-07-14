import config



class ADXFilter:


    @staticmethod
    def evaluate(trend, m1):


        score_buy = 0
        score_sell = 0

        log = []



        # ==========================
        # LETTURA ADX
        # ==========================


        adx = m1.ADX14



        # lettura DI se presenti

        plus_di = getattr(
            m1,
            "PLUS_DI",
            None
        )


        minus_di = getattr(
            m1,
            "MINUS_DI",
            None
        )




        # ==========================
        # ADX TROPPO DEBOLE
        # ==========================


        if adx < config.ADX_MIN:


            log.append(
                f"ADX debole {adx:.1f}"
            )


            return {


                "buy":0,

                "sell":0,

                "log":log

            }





        # ==========================
        # CALCOLO FORZA TREND
        # ==========================


        if adx <= config.ADX_GOOD_MAX:


            base_score = config.ADX_SCORE

            descrizione = "ADX ideale"



        elif adx <= config.ADX_STRONG_MAX:


            base_score = config.ADX_STRONG_SCORE

            descrizione = "ADX forte"



        elif adx <= config.ADX_EXTREME_MAX:


            base_score = config.ADX_EXTREME_SCORE

            descrizione = "ADX esteso"



        else:


            base_score = 0

            descrizione = "ADX troppo estremo"






        # ==========================
        # CONTROLLO DIREZIONE
        # ==========================


        direction_penalty = 0



        if (
            plus_di is not None
            and minus_di is not None
        ):



            if trend == "BUY":


                if plus_di < minus_di:


                    direction_penalty = -config.ADX_DI_PENALTY


                    log.append(
                        f"ADX direzione opposta BUY -{config.ADX_DI_PENALTY}"
                    )



            elif trend == "SELL":


                if minus_di < plus_di:


                    direction_penalty = -config.ADX_DI_PENALTY


                    log.append(
                        f"ADX direzione opposta SELL -{config.ADX_DI_PENALTY}"
                    )






        final_score = max(
            base_score + direction_penalty,
            0
        )






        # ==========================
        # ASSEGNAZIONE SCORE
        # ==========================


        if trend == "BUY":


            score_buy = final_score


            log.append(
                f"{descrizione} {adx:.1f} +{score_buy}"
            )



        elif trend == "SELL":


            score_sell = final_score


            log.append(
                f"{descrizione} {adx:.1f} +{score_sell}"
            )






        return {


            "buy": score_buy,


            "sell": score_sell,


            "log": log

        }
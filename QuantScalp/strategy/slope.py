import config


class SlopeFilter:

    @staticmethod
    def evaluate(trend, trend_strength, m1, df):

        score_buy = 0
        score_sell = 0

        log = []

        # ==========================
        # CONTROLLO DATI
        # ==========================

        if len(df) < config.SLOPE_LOOKBACK + 2:

            return {
                "buy": 0,
                "sell": 0,
                "log": ["Slope dati insufficienti"]
            }

        # ==========================
        # CALCOLO SLOPE EMA20
        # ==========================

        ema_now = df.iloc[-2]["EMA20"]

        ema_old = df.iloc[
            -(config.SLOPE_LOOKBACK + 2)
        ]["EMA20"]

        atr = m1.ATR14

        if atr <= 0:

            return {
                "buy": 0,
                "sell": 0,
                "log": ["Slope ATR non valido"]
            }

        slope = (ema_now - ema_old) / atr

        # ==========================
        # BUY
        # ==========================

        if trend == "BUY":

            if slope >= config.SLOPE_STRONG:

                score_buy = config.SLOPE_SCORE_STRONG

                log.append(
                    f"Slope BUY forte {slope:.2f} ATR +{score_buy}"
                )

            elif slope >= config.SLOPE_MIN:

                score_buy = config.SLOPE_SCORE_WEAK

                log.append(
                    f"Slope BUY moderato {slope:.2f} ATR +{score_buy}"
                )

            elif slope >= config.SLOPE_PULLBACK_LIMIT:

                log.append(
                    f"Slope BUY pullback {slope:.2f} ATR"
                )

            else:

                # ==========================
                # PENALITA' ADATTIVA
                # ==========================

                if trend_strength == "STRONG":

                    score_buy = 0

                    log.append(
                        f"Slope BUY pullback profondo {slope:.2f} ATR"
                    )

                elif trend_strength == "PULLBACK":

                    score_buy = config.SLOPE_AGAINST_PENALTY

                    log.append(
                        f"Slope BUY debole {slope:.2f} ATR {score_buy}"
                    )

                else:

                    score_buy = config.SLOPE_STRONG_PENALTY

                    log.append(
                        f"Slope BUY inversione {slope:.2f} ATR {score_buy}"
                    )

        # ==========================
        # SELL
        # ==========================

        elif trend == "SELL":

            if slope <= -config.SLOPE_STRONG:

                score_sell = config.SLOPE_SCORE_STRONG

                log.append(
                    f"Slope SELL forte {slope:.2f} ATR +{score_sell}"
                )

            elif slope <= -config.SLOPE_MIN:

                score_sell = config.SLOPE_SCORE_WEAK

                log.append(
                    f"Slope SELL moderato {slope:.2f} ATR +{score_sell}"
                )

            elif slope <= -config.SLOPE_PULLBACK_LIMIT:

                log.append(
                    f"Slope SELL pullback {slope:.2f} ATR"
                )

            else:

                if trend_strength == "STRONG":

                    score_sell = 0

                    log.append(
                        f"Slope SELL pullback profondo {slope:.2f} ATR"
                    )

                elif trend_strength == "PULLBACK":

                    score_sell = config.SLOPE_AGAINST_PENALTY

                    log.append(
                        f"Slope SELL debole {slope:.2f} ATR {score_sell}"
                    )

                else:

                    score_sell = config.SLOPE_STRONG_PENALTY

                    log.append(
                        f"Slope SELL inversione {slope:.2f} ATR {score_sell}"
                    )

        return {

            "buy": score_buy,

            "sell": score_sell,

            "log": log

        }
import config


class TrendFilter:

    @staticmethod
    def evaluate(m15):

        score_buy = 0
        score_sell = 0

        trend = None
        strength = "NONE"

        log = []

        ema20 = m15.EMA20
        ema50 = m15.EMA50
        ema200 = m15.EMA200

        # =====================================
        # BUY FORTE
        # EMA20 > EMA50 > EMA200
        # =====================================

        if ema20 > ema50 > ema200:

            trend = "BUY"
            strength = "STRONG"

            score_buy = config.TREND_SCORE

            log.append(
                f"Trend BUY forte +{score_buy}"
            )

        # =====================================
        # BUY PULLBACK
        # EMA50 > EMA200
        # EMA20 sotto EMA50
        # =====================================

        elif ema50 > ema200 and ema20 <= ema50:

            trend = "BUY"
            strength = "PULLBACK"

            score_buy = config.TREND_SCORE

            log.append(
                f"Trend BUY in pullback +{score_buy}"
            )

        # =====================================
        # SELL FORTE
        # EMA20 < EMA50 < EMA200
        # =====================================

        elif ema20 < ema50 < ema200:

            trend = "SELL"
            strength = "STRONG"

            score_sell = config.TREND_SCORE

            log.append(
                f"Trend SELL forte +{score_sell}"
            )

        # =====================================
        # SELL PULLBACK
        # EMA50 < EMA200
        # EMA20 sopra EMA50
        # =====================================

        elif ema50 < ema200 and ema20 >= ema50:

            trend = "SELL"
            strength = "PULLBACK"

            score_sell = config.TREND_SCORE

            log.append(
                f"Trend SELL in pullback +{score_sell}"
            )

        # =====================================
        # NESSUN TREND
        # =====================================

        else:

            log.append(
                "Trend M15 assente"
            )

        return {

            "trend": trend,

            "strength": strength,

            "trend_strength": strength,

            "buy": score_buy,

            "sell": score_sell,

            "log": log

        }
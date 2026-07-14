# =====================================
# QUANTSCALP CONFIGURATION
# =====================================


# =====================================
# STRATEGY SCORE
# =====================================

MIN_SCORE = 75

MIN_SCORE_M5_OPPOSITE = 75


# punteggio massimo teorico
MAX_SCORE = 100



# =====================================
# STRATEGY WEIGHTS
# =====================================

TREND_SCORE = 20

PULLBACK_SCORE = 10

MOMENTUM_SCORE = 10

SLOPE_SCORE = 10

CANDLE_SCORE = 10

ENGULFING_SCORE = 5

REJECTION_SCORE = 5

BREAKOUT_SCORE = 15

RSI_SCORE = 10

ADX_SCORE = 15

VOLUME_SCORE = 10

ATR_SCORE = 5

VOLATILITY_SCORE = 5

SPREAD_SCORE = 10



# =====================================
# PREMIUM SETUP
# =====================================

SETUP_COMPLETO_ENABLED = True

SETUP_COMPLETO_SCORE = 10



# =====================================
# MARKET
# =====================================

DEFAULT_SYMBOL = "EURUSD"


TREND_TIMEFRAME = "M15"

CONFIRMATION_TIMEFRAME = "M5"

ENTRY_TIMEFRAME = "M1"



TREND_CANDLES = 300

CONFIRMATION_CANDLES = 200

ENTRY_CANDLES = 200





# =====================================
# RISK MANAGEMENT
# =====================================

RISK_PERCENT = 0.25


MAX_LOT = 0.50


ATR_SL_MULTIPLIER = 3.0


REWARD_RATIO = 2.0





# =====================================
# M5 CONFIRMATION
# =====================================

M5_CONFIRMATION_REQUIRED = True


M5_CONFIRMATION_SCORE = 10


M5_OPPOSITE_PENALTY = -10





# =====================================
# ADX FILTER
# =====================================


ADX_MIN = 20


# mercato normale

ADX_GOOD_MAX = 50


# trend forte

ADX_STRONG_MAX = 70


# trend molto forte

ADX_EXTREME_MAX = 85



# punteggi

ADX_SCORE = 15

ADX_STRONG_SCORE = 12

ADX_EXTREME_SCORE = 0



# oltre questo valore evitare ingressi

ADX_PANIC = 90



# penalità direzione DI

ADX_DI_PENALTY = 5





# =====================================
# RSI FILTER
# =====================================


# BUY

RSI_BUY_MIN = 40

RSI_BUY_MAX = 70



# SELL

RSI_SELL_MIN = 25

RSI_SELL_MAX = 60



# zona ideale

RSI_IDEAL_LOW = 45

RSI_IDEAL_HIGH = 60



# estremi

RSI_OVERBOUGHT = 75

RSI_OVERSOLD = 25



# punteggi

RSI_IDEAL_SCORE = 10

RSI_NORMAL_SCORE = 7

RSI_EXTREME_SCORE = -10





# =====================================
# SPREAD FILTER
# =====================================

MAX_SPREAD = 1





# =====================================
# BREAKOUT
# =====================================

BREAKOUT_PERIOD = 20


# prezzo vicino al livello, non ancora rotto
PRE_BREAKOUT_SCORE = 8





# =====================================
# VOLATILITY
# =====================================

ATR_AVERAGE_PERIOD = 50


ATR_COMPRESSION_FACTOR = 0.60


ATR_EXTREME_FACTOR = 2.00





# =====================================
# SLOPE FILTER
# =====================================


# candele EMA20 analizzate

SLOPE_LOOKBACK = 10



# movimento minimo

SLOPE_MIN = 0.20



# movimento forte

SLOPE_STRONG = 0.70



# pullback fisiologico

SLOPE_PULLBACK_LIMIT = -1.50



# inversione

SLOPE_AGAINST_LIMIT = -2.50





# score positivi

SLOPE_SCORE_WEAK = 5

SLOPE_SCORE_STRONG = 10





# penalità

SLOPE_AGAINST_PENALTY = -5

SLOPE_STRONG_PENALTY = -10





# =====================================
# CANDLE FILTER
# =====================================

CANDLE_REQUIRED = True





# =====================================
# SETUP QUALITY FILTER
# =====================================

# soglie RSI estremo (allineate a RSI_OVERBOUGHT / RSI_OVERSOLD)
RSI_OVERBOUGHT_LIMIT = 75

RSI_OVERSOLD_LIMIT = 25

RSI_EXTREME_PENALTY = 15


# volume minimo accettabile (frazione della media VOL20)
MIN_VOLUME_FACTOR = 0.70

LOW_VOLUME_PENALTY = 10


# ADX considerato "forte" ai fini della qualità del setup
ADX_STRONG = 50


# punteggio minimo di qualità per considerare il setup GOOD
SETUP_QUALITY_MIN = 70


# soglia di score più severa quando il setup ha qualità BAD
MIN_SCORE_LOW_QUALITY = 85




# =====================================
# MAIN LOOP
# =====================================

# ogni quanti secondi valutare un nuovo segnale/trade
SIGNAL_LOOP_SECONDS = 30

# ogni quanti secondi controllare il trailing stop
TRAILING_LOOP_SECONDS = 5

# numero massimo di posizioni aperte contemporaneamente dal bot
# sullo stesso simbolo
MAX_OPEN_POSITIONS = 1




# =====================================
# TRAILING STOP
# =====================================

TRAILING_ENABLED = True

# profitto minimo (in pips) prima di iniziare a trailare
TRAILING_START_PIPS = 10

# distanza mantenuta tra prezzo attuale e SL (in pips)
TRAILING_DISTANCE_PIPS = 12

# miglioramento minimo (in pips) prima di inviare una modifica SL
# (evita di bombardare il broker con richieste per micro-variazioni)
TRAILING_STEP_PIPS = 3




# =====================================
# ORDER EXECUTION
# =====================================

MAGIC_NUMBER = 990211

# slippage massimo tollerato (in punti)
DEVIATION = 10

ORDER_COMMENT = "QuantScalp"




# =====================================
# DECISION ENGINE
# =====================================

REQUIRE_TREND_CONFIRMATION = True





# =====================================
# DEBUG
# =====================================

DEBUG = True
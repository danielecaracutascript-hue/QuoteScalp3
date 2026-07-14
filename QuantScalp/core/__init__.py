def __init__(self, symbol):

    self.symbol = symbol

    self.strategy = StrategyEngine(symbol)

    self.market_data = MarketData()

    self.indicators = IndicatorEngine()

    self.regime_engine = MarketRegime()
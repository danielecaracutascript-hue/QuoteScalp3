class Position:

    """
    Wrapper leggero attorno a una posizione MT5 grezza
    (l'oggetto restituito da mt5.positions_get()), per
    avere un'interfaccia più leggibile e testabile.
    """

    def __init__(self, mt5_position):

        self.ticket = mt5_position.ticket

        self.symbol = mt5_position.symbol

        self.type = mt5_position.type

        self.volume = mt5_position.volume

        self.price_open = mt5_position.price_open

        self.sl = mt5_position.sl

        self.tp = mt5_position.tp

        self.magic = mt5_position.magic

        self.profit = mt5_position.profit



    @property
    def is_buy(self):

        # POSITION_TYPE_BUY == 0
        return self.type == 0



    @property
    def is_sell(self):

        # POSITION_TYPE_SELL == 1
        return self.type == 1
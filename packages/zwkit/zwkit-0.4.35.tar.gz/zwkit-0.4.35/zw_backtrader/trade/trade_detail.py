import pandas as pd


class trade_detail:
    """
    交易明细
    """

    def __init__(self, buy_date, name, trade_id, sell_date):
        self.name = name
        self.buy_date = buy_date
        self.trade_id = trade_id
        self.sell_date = sell_date

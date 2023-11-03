import backtrader as bt
from zw_backtrader.zw_option import log_option, cash_option


class base_cerebro:
    def __init__(self, logs: log_option, cash: cash_option):
        self.cerebro = bt.Cerebro()
        self.logs = logs
        self.cash_option = cash

    def get_cerebro(self):
        cerebro = self.cerebro
        cerebro.broker.setcash(self.cash_option.cash)  # 设置初始资金
        cerebro.broker.setcommission(self.cash_option.commission)  # 设置交易费率
        cerebro.broker.set_slippage_fixed(self.cash_option.slip)  # 设置固定滑点
        return cerebro  # 返回cerebro核心对象

import backtrader as bt
import joblib
import pandas as pd
import os
from zwkit import date_kit
import datetime as dt
import zw_backtrader.trade.trade_detail as td


class base_strategy(bt.Strategy):
    """
    策略基类
    同时只能持有一只股票
    卖了以后有10天冷静期
    """

    params = (
        ('model_path', ""),  # 模型路径
        ('log_path', '../data/backtrader/'),  # 日志路径
        ('log_name', f'logs_{date_kit.now()}.log'),  # 日志名称
        ('cold_date', 10)  # 冷静期
    )

    def __init__(self):
        # 买卖列表
        self.position_list = dict()
        # 拦截列表
        self.filter_dict = dict()
        # 日志集合
        self.log_text = []

    def log(self, txt, dt=None):
        """
        Logging function fot this strategy
        :param txt:
        :param dt:
        :return:
        """
        dt = dt or self.datas[0].datetime.date(0)
        self.log_text.append(f'{dt.isoformat()}: {txt}')
        print(f'{dt.isoformat()}: {txt}')

    def start(self):
        """
        策略启动时执行
        :return:
        """
        self.model = joblib.load(self.params.model_path)

    # def prenext(self):
    #     '''策略准备阶段,对应第1根bar ~ 第 min_period-1 根bar'''
    #     # 该函数主要用于等待指标计算，指标计算完成前都会默认调用prenext()空函数
    #     # min_period 就是 __init__ 中计算完成所有指标的第1个值所需的最小时间段
    #     print('prenext函数')
    #
    # def nextstart(self):
    #     '''策略正常运行的第一个时点，对应第 min_period 根bar'''
    #     # 只有在 __init__ 中所有指标都有值可用的情况下，才会开始运行策略
    #     # nextstart()只运行一次，主要用于告知后面可以开始启动 next() 了
    #     # nextstart()的默认实现是简单地调用next(),所以next中的策略逻辑从第 min_period根bar就已经开始执行
    #     print('nextstart函数')

    def next(self):
        # 获取每只股票的信息
        # 并放入模型验证
        for index in range(len(self.datas)):
            self._next_execute(index)

    def _next_execute(self, index):
        symbol = self.datas[index]._name
        date = self.datas[index].datetime.date(0)
        self._sell_excute(date, index)
        if self._predict_excute(index) == 1:
            if self._filter_execute(symbol, date):
                self._buy_excute(symbol, index)
            else:
                pass
                # self.log(f'近期购买,过滤{symbol}')
        else:
            pass
            # self.log(f'预测不买入{symbol}')

    def _filter_execute(self, symbol, date):
        # 过滤持仓
        if self.position_list.get(symbol) is not None:
            # 有持仓 不买入
            return False
        else:
            # 过滤冷静期
            filter_date = self.filter_dict.get(symbol)
            if filter_date is not None:
                if date < filter_date:
                    # 日期小于冷静期 不买入
                    return False
                else:
                    # 日期大于冷静期 买入
                    # 删除冷静期
                    self.filter_dict.pop(symbol)
                    return True
        return True

    def _sell_excute(self, date, index):
        for k, v in self.position_list.items():
            if date > v.sell_date:
                self.sell(data=self.datas[index], size=100, exectype=bt.Order.Market, price=self.datas[index].lines.close[0])

    def _predict_excute(self, index):
        data = self._get_data(datas=self.datas[index], index=index)
        return self.model.predict(data)

    def _buy_excute(self, symbol, index):
        adj_factor = self.datas[index].lines.adj_factor[1]
        # open = round(self.datas[index].lines.open[1] / adj_factor, 2)
        # close = round(self.datas[index].lines.close[0] / adj_factor, 2)
        # high = round(self.datas[index].lines.high[0] / adj_factor, 2)
        # low = round(self.datas[index].lines.low[0] / adj_factor, 2)
        self.buy(data=self.datas[index], size=100)

    def _get_data(self, datas, index):
        # 这个index非常必要熬
        data = pd.DataFrame()
        for v, k in enumerate(datas._colmapping):
            if self.data.data_schema is not None:
                if k not in self.data.data_schema:
                    continue
                exec(f"data.loc[0,'{k}'] = self.datas[index].lines.{k}[0]")
        return data

    def stop(self):
        """
        策略结束时执行
        将日志进行保存
        :return:
        """
        if os.path.exists(self.params.log_path) is False:
            os.mkdir(self.params.log_path)

        with open(self.params.log_path + self.params.log_name, mode='w') as f:
            f.write('\n'.join(self.log_text))

    def notify_order(self, order):
        """
        订单状态变化时执行
        :param order:
        :return:
        """

        # 判断订单的状态
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 判断订单是否完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入{order.data._name},价格:{order.executed.price},成本:{order.executed.value},手续费:{order.executed.comm}')
                self.position_list.update({order.data._name: td.trade_detail(order.data.datetime.date(0), order.data._name, trade_id=order.ref,
                                                                             sell_date=order.data.datetime.date(3))})

            else:
                self.log(f'卖出{order.data._name},价格:{order.executed.price},成本:{order.executed.value},手续费:{order.executed.comm}')
                self.position_list.pop(order.data._name)
                self.filter_dict[order.data._name] = order.data.datetime.date(0) + dt.timedelta(days=self.params.cold_date)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'订单失败: {order.data._name} 状态: {order.getstatusname()}')

    def notify_trade(self, trade):
        """
        交易状态变化时执行
        :param trade:
        :return:
        """
        if not trade.isclosed:
            return
        self.log(f'利润,毛利:{trade.pnl},净利:{trade.pnlcomm}')

    # def notify_cashvalue(self, cash, value):
    #     """
    #     资金变化时执行
    #     :param cash:
    #     :param value:
    #     :return:
    #     """
    #     self.log(f'资金:{cash},市值:{value}')

    # def notify_fund(self, cash, value, fundvalue, shares):
    #     """
    #     资金变化时执行
    #     :param cash:
    #     :param value:
    #     :param fundvalue:
    #     :param shares:
    #     :return:
    #     """
    #     self.log(f'资金:{cash},市值:{value},净值:{fundvalue},持仓:{shares}')

# class test_strategy(bt.Strategy):
#     """
#     策略基类
#     """
#
#     def __init__(self):
#         # 买卖列表
#         self.buying_list = []
#         self.selling_list = []
#
#     def next(self):
#         for index in range(len(self.datas)):
#             data = self._get_data(datas=self.datas[index], index=index)
#             print(data)
#
#             # 进行预测
#
#     def _get_data(self, datas, index):
#         data = pd.DataFrame()
#         for v, k in enumerate(datas._colmapping):
#             if k is None:
#                 continue
#             exec(f"data.loc[0,'{k}'] = self.datas[index].lines.{k}[0]")
#         return data

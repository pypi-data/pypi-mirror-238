import backtrader as bt
import pandas as pd

import zw_backtrader.zw_cerebro as zw
import zw_backtrader.strategy.strategy as zw_strategy

import zw_backtrader.zw_option as z


class data_on(bt.feeds.PandasData):
    lines = ('datetime', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount',)
    params = (
        ('datetime', -1), ('open', -1), ('high', -1), ('low', -1), ('close', -1), ('pre_close', -1), ('change', -1), ('pct_chg', -1), ('vol', -1),
        ('amount', -1),)
    datafields = ['datetime', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount']


#


if "__main__" == __name__:
    # z.lines_params_helper(('trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount'))

    # 1. 创建日志对象
    logs = zw.log_option()
    # 2. 创建资金对象
    cash = zw.cash_option()
    # 3. 创建cerebro对象
    cerebro = zw.base_cerebro(logs, cash)
    # 4. 导出cerebro核心对象
    cerebro1 = cerebro.get_cerebro()
    # 5. 导入数据
    base_data = pd.read_csv("/Users/summer/PycharmProjects/daily-random-forest-project/data/data.csv")
    test_data = base_data[base_data['ts_code'] == '603019.SH']
    test_data = test_data[test_data['trade_date'] > 20160601]
    aa = test_data[['trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount']]
    aa.columns = ['datetime', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount']
    aa['datetime'] = aa['datetime'].apply(lambda x: pd.to_datetime(x, format='%Y%m%d'))
    # aa.set_index('datetime', inplace=True)
    data = data_on(dataname=aa)
    # data = bt.feeds.PandasData(dataname=test_data)
    # 6. 添加数据
    cerebro1.adddata(data=data, name='603019.SH')
    # 7. 导入策略
    cerebro1.addstrategy(strategy=zw_strategy.test_strategy)
    # 8. 运行策略
    cerebro1.run()
    # 9. 绘图
    # cerebro1.plot()

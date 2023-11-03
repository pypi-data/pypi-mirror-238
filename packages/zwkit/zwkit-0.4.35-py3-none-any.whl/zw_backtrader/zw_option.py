class log_option:
    """
    日志选项
    """

    def __init__(self, log_file_name="log.txt"):
        self.log_file_name = log_file_name


class cash_option:
    """
    股票资金选项
    """

    def __init__(self, cash=50000.0, commission=0.0003, slip=0.005):
        self.cash = cash  # 初始资金
        self.commission = commission  # 交易费率
        self.slip = slip  # 滑点


def lines_params_helper(add_list):
    lines = ()
    params = []
    for col in add_list:
        lines += (col,)
        params.append((col, -1))
    params = tuple(params)
    print("lines = ", lines)
    print("params = ", params)

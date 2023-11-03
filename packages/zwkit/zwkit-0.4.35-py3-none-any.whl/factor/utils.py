def winsorize_std(series, n=3):
    mean, std = series.mean(), series.std()
    return series.clip(mean - std * n, mean + std * n)


def winsorize_mad(series, n=3):
    median, mad = series.median(), series.mad()
    return series.clip(median - mad * n, median + mad * n)

def standardize(series):
    return (series - series.mean()) / series.std()


def neutralize(series):
    # 待补充
    return series

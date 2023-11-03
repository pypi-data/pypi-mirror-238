import pandas as pd
import re

def get_before_date(date, days=60):
    """
    取得指定日期前60天的日期
    :param date:
    :param days:
    :return:
    """
    date = pd.to_datetime(date)
    date = date - pd.Timedelta(days=days)
    return date.strftime("%Y-%m-%d")

def now(type="%Y%m%d%H%M%S"):
    """
    获取当前时间
    :return:
    """
    return pd.to_datetime("now").strftime(type)


#调用is_yyyymmdd和is_yyyy_mm_dd判断是否为yyyymmdd或者yyyy-mm-dd
def to_yyyymmdd(date):
    if is_yyyymmdd(date):
        return date
    elif is_yyyy_mm_dd(date):
        return date.replace('-', '')
    else:
        return None

def to_yyyy_mm_dd(date):
    if is_yyyymmdd(date):
        return date[0:4] + '-' + date[4:6] + '-' + date[6:8]
    elif is_yyyy_mm_dd(date):
        return date
    else:
        return None


#用正则表达式判断是否为yyyymmdd
def is_yyyymmdd(date):
    """
    用正则表达式判断是否为yyyymmdd
    :param date:
    :return:
    """

    pattern = re.compile(r'^\d{4}\d{2}\d{2}$')
    match = pattern.match(date)
    if match:
        return True
    else:
        return False

#用正则表达式判断是否为yyyy-MM-dd
def is_yyyy_mm_dd(date):
    """
    用正则表达式判断是否为yyyy-MM-dd
    :param date:
    :return:
    """
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    match = pattern.match(date)
    if match:
        return True
    else:
        return False
# -*- coding: utf-8 -*-
"""
@Time    : 18-2-7

@File    : utility.py

@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003@gmail.com
"""

import tushare as ts
from datetime import datetime, timedelta, date


# 日期格式YYYYMMDD转为YYYY-MM-DD
def formatDate(Date, format_type='YYYYMMDD'):
  """
  将数字格式日期转换成str格式
  :param Date: 数字格式日期；例如：20180102
  :param format_type:
  :return: 字符串格式日期；例如：”20180102“
  """
  d=str(Date)
  format_type = format_type.replace('YYYY', d[0:4])
  format_type = format_type.replace('MM', d[4:6])
  format_type = format_type.replace('DD', d[-2:])
  return format_type


def str2date(strdate='20180101'):
  """
  转换字符串为datetime
  :param strdate: 日期字符串，格式为：“YYYYMMDD”
  :return: datetime
  """
  return datetime(year=int(strdate[0:4]), month=int(strdate[4:6]), day=int(strdate[6:8]))


def int2date(intdate: int):
  """将整数格式的日期转换成date
  If you have date as an integer, use this method to obtain a datetime.date object.

  Parameters
  ----------
  intdate : int
    Date as a regular integer value (example: 20160618)

  Returns
  -------
  dateandtime.date
    A date object which corresponds to the given value `intdate`.
  """
  y = int(intdate / 10000)
  m = int((intdate % 10000) / 100)
  d = int(intdate % 100)
  return date(y, m, d)

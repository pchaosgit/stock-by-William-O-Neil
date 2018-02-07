# -*- coding: utf-8 -*-
"""
@Time    : 18-2-7

@File    : utility.py

@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003@gmail.com
"""

import tushare as ts
from datetime import datetime, timedelta


# 日期格式YYYYMMDD转为YYYY-MM-DD
def formatDate(Date, format_type='YYYYMMDD'):
  """
  将数字格式日期转换成str格式
  :param Date: 数字格式日期；例如：20180102
  :param format_type:
  :return: 字符串格式日期；例如：”20180102“
  """
  format_type = format_type.replace('YYYY', Date[0:4])
  format_type = format_type.replace('MM', Date[4:6])
  format_type = format_type.replace('DD', Date[-2:])
  return format_type


def str2date(strdate='20180101'):
  """
  转换字符串为datetime
  :param strdate: 日期字符串，格式为：“YYYYMMDD”
  :return: datetime
  """
  return datetime(year=int(strdate[0:4]), month=int(strdate[4:6]), day=int(strdate[6:8]))







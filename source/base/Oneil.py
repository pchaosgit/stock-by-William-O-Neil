# -*- coding: utf-8 -*-
"""
@Time    : 18-2-7
@File    : Oneil.py
@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003@gmail.com
"""
import tushare as ts
from datetime import datetime, timedelta


class Oneil():
  """
  基础工具类
  包含常用函数
  """
  pass


class OneilKDZD(Oneil):
  """
  口袋支点
  """

  def __init__(self):
    # todo 本地缓存
    self.sbdf = ts.get_stock_basics()
    self.sbdf.sort_index(inplace=True)

  #
  def listingDate(self, n=365):
    """
    返回上市超过n天的股票列表;默认为一年
    """
    end_date = datetime.now() + timedelta(days=-n)
    return self.sbdf.mask(lambda x: (x['timeToMarket'] < end_date.year*10000 + end_date.month*100 + end_date.day & x['timeToMarket'] > 0 ))

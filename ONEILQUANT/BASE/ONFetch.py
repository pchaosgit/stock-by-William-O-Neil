# -*- coding: utf-8 -*-
"""
@Time    : 2018-02-22

@File    : ONFetch.py

@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003#gmail.com
"""


class ONFetchbase():
  def get_stock_list(self):
    pass

  def stock_day_adv(self, code, start, end):
    pass

  def index_day_adv(self, code, start, end):
    pass

  def stock_min_adv(code, start, end, frequence='1min'):
    pass


import QUANTAXIS as QA
from datetime import datetime as dt
import pandas as pd
from pathlib import Path


class ONFetchQAMongo(ONFetchbase):
  """
  使用quantaxis获取股票数据
  """

  def __init__(self):
    self._indexday = pd.DataFrame()
    self._filelist = {
      "indexday": "./indexday.pkl.gz"
    }

  def stock_day_adv(self, code, start="", end=""):
    if (len(start) == 0):
      # 获取所有的数据
      return QA.QA_fetch_stock_day_adv(code)
    else:
      return QA.QA_fetch_stock_day_adv(code, start, end)

  def index_day_adv(self, code, start, end):
    return QA.QA_fetch_index_day_adv(code, start, end)

  @property
  def indexday(self):
    # 上证指数交易日期
    if len(self._indexday) == 0:
      # todo 判断本地文件时间，再决定是否更新本地文件
      indexdayfile = Path(self._filelist['indexday'])
      if indexdayfile.exists():
        # 读取本地
        self._indexday = pd.read_pickle(indexdayfile.name)
      else:
        # 通过quantaxis在线获取股票基本资料
        self._indexday = self.index_day_adv("000001", start='1990-01-01', end=dt.now())
        self._indexday = pd.DataFrame(self._indexday.close.sort_index())
        if not indexdayfile.exists():
          # 保存到文件
          self._indexday.to_pickle(indexdayfile.name)
    return self._indexday


def static_vars(**kwargs):
  def decorate(func):
    for variable in kwargs:
      setattr(func, variable, kwargs[variable])
    return func

  return decorate


@static_vars(counter=0)
def foo():
  foo.counter += 1

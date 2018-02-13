# -*- coding: utf-8 -*-
"""
@Time    : 18-2-7
@File    : test_oneilKDZD.py
@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003#gmail.com
"""
from unittest import TestCase
from . import env
# append parent directory to import path
from ONEIL.Oneil.Oneil import OneilKDZD as oneil


class TestOneilsourceKDZD(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_listingDate(self):
    o = oneil()
    # 默认上市一年以上
    df = o.listingDate()
    # 上市超过一年的股票数量大于2000个
    self.assertTrue(len(df) > 2000)
    df1 = o.listingDate(200)
    self.assertTrue(len(df) < len(df1), "上市一年的股票数量<200天的股票数量")

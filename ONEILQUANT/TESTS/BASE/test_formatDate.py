# -*- coding: utf-8 -*-
"""
@Time    : 18-2-17

@File    : test_formatDate

@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003#gmail.com
"""

from unittest import TestCase
from ONEILQUANT.BASE import utility as ut
from datetime import datetime, date

class Test_BaseUtility(TestCase):
  def test_formatDate(self):
    # todo d为整型
    d = '20180102'
    fd = ut.formatDate(d)
    self.assertTrue(len(fd) == 8, "")

  def test_str2date(self):
    d = '20180102'
    fd = ut.str2date(d)
    self.assertTrue(type(fd) == datetime, "datetime type:{0}".format(type(fd)))

  def test_int2date(self):
    d = 20180102
    fd = ut.int2date(d)
    self.assertTrue(type(fd) == date, "datetime type:{0}".format(type(fd)))
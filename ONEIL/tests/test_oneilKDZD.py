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

  def test_listingDate(self):
    o = oneil()
    df=o.listingDate()
    self.assertTrue(len(df) > 0)

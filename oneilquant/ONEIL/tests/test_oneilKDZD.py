# -*- coding: utf-8 -*-
"""
@Time    : 18-2-7
@File    : test_oneilKDZD.py
@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003#gmail.com
"""
from unittest import TestCase
# append parent directory to import path
from oneilquant.ONEIL.Oneil import OneilKDZD as oneil


class TestOneilKDZD(TestCase):
    def setUp(self):
        self.oq = oneil()

    def tearDown(self):
        self.oq = None

    def test_listingDate(self):
        # 默认上市一年以上
        n1 = 365
        df = self.oq.listingDate(n1)
        # 上市超过一年的股票数量大于2000个
        len1 = len(df)
        self.assertTrue(len(df) > 2500, "上市一年以上股票数量，2018年最少大于2500只")
        # 不同上市时间的股票数比较
        n2 = 200
        df1 = self.oq.listingDate(n2)
        self.assertTrue(len(df) < len(df1), "上市一年的股票数量<{0}天的股票数量".format(n2))
        print(df1)
        n3 = 0
        df = self.oq.listingDate(n3)
        # 上市超过0天的股票数量大于上市超过一年的股票数量
        self.assertTrue(len(df) >= len1, "上市一年以上股票数量，2018年最少大于2500只")
        print('上市所有股票数量：{} 上市大于{}天股票数量：{}'.format(len(df), n1, len1))

# if __name__=='__main__':
#   TestCase.run()

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
from pathlib import Path
import pandas as pd


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
        self._sbdf = pd.DataFrame()
        self._oneildf = pd.DataFrame()
        #
        self._sbdFilename = "./stock_basics.pkl.gz"
        self._sbdFile = Path(self._sbdFilename)

    @property
    def sbdf(self):
        """
        股票基本资料
        :return: 股票基本资料
            DataFrame
               code,代码
               name,名称
               industry,细分行业
               area,地区
               pe,市盈率
               outstanding,流通股本
               totals,总股本(万)
               totalAssets,总资产(万)
               liquidAssets,流动资产
               fixedAssets,固定资产
               reserved,公积金
               reservedPerShare,每股公积金
               eps,每股收益
               bvps,每股净资
               pb,市净率
               timeToMarket,上市日期
        """
        if len(self._sbdf) == 0:
            # todo 判断本地文件时间，再决定是否更新本地文件
            if self._sbdFile.exists():
                # 读取本地
                self._sbdf = pd.read_pickle(self._sbdFilename)
            else:
                # 通过tushare在线获取股票基本资料
                self._sbdf = ts.get_stock_basics()
                self._sbdf.sort_index(inplace=True)
                if not self._sbdFile.exists():
                    # 保存到文件
                    self._sbdf.to_pickle(self._sbdFilename)
        return self._sbdf

    @sbdf.setter
    def sbdf(self, value):
        self._sbdf = value

    @sbdf.deleter
    def sbdf(self):
        del self._sbdf

    @property
    def oneildf(self):
        """
        欧奈尔
        :return:
        """
        return self._oneildf

    @oneildf.setter
    def oneildf(self, value):
        self._oneildf = value

    #
    def listingDate(self, n=365):
        """
        返回上市超过n天的股票列表;默认为一年
                :return: 股票基本资料
            DataFrame
               code,代码
               name,名称
               industry,细分行业
               area,地区
               pe,市盈率
               outstanding,流通股本
               totals,总股本(万)
               totalAssets,总资产(万)
               liquidAssets,流动资产
               fixedAssets,固定资产
               reserved,公积金
               reservedPerShare,每股公积金
               eps,每股收益
               bvps,每股净资
               pb,市净率
               timeToMarket,上市日期
        """
        end_date = datetime.now() + timedelta(days=-n)
        # return self._sbdf.mask(lambda x: x['timeToMarket'] < end_date.year * 10000 + end_date.month * 100 + end_date.day & x['timeToMarket'] > 0)
        return self.sbdf[
            (self._sbdf['timeToMarket'] < end_date.year * 10000 + end_date.month * 100 + end_date.day) & (
                    self._sbdf['timeToMarket'] > 0)]

    # 口袋支点
    def KDZD(self):
        pass

    # 一年新高
    def YNXG(self):
        pass

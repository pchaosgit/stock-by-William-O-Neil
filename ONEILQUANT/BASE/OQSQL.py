# -*- coding: utf-8 -*-
"""
@Time    : 18-2-17

@File    : OQSQL.py.py

@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003#gmail.com
"""


import pymongo


def OQ_util_sql_mongo_setting(ip='127.0.0.1', port=27017):
  client = pymongo.MongoClient(ip, int(port))
  # QA_util_log_info('ip:{},port:{}'.format(str(ip), str(port)))
  return client
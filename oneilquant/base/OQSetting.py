# -*- coding: utf-8 -*-
"""
@Time    : 18-2-17

@File    : OQSetting.py

@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003#gmail.com
"""

class OQ_Setting():
  """
  参数设置模块
  """
  def __init__(self, ip='127.0.0.1', port=27017):
    self.ip = ip
    self.port = port
    self.username = None
    self.password = None

    @property
    def client(self):
        return QA_util_sql_mongo_setting(self.ip, self.port)

    def change(self, ip, port):
        self.ip = ip
        self.port = port
        global DATABASE
        DATABASE = self.client.oneilquant
        return self

    def login(self, user_name, password):
        user = QA_user_sign_in(user_name, password, self.client)
        if user is not None:
            self.user_name = user_name
            self.password = password
            self.user = user
            return self.user
        else:
            return False

# mongo ds249025.mlab.com:49025/stockdb -u dbuser -p dbtest
DATABASE = QA_Setting(ds249025.mlab.com, 49025).client.oneilquant

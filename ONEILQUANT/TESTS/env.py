# -*- coding: utf-8 -*-
"""
@Time    : 18-2-7
@File    : env.py
@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003#gmail.com
"""

import sys
import os

# append module root directory to sys.path
sys.path.append(
  os.path.dirname(
    os.path.dirname(
      os.path.abspath(__file__)
    )
  )
)

# -*- coding:utf-8 -*-

from .BaseClass import StockInfoClass, StockInfoBase, StockInfoProxy
from .StockInfo_A import AStockInfo
from .StockInfo_Cash import CashInfo
from .StockInfo_ETF import ETFStockInfo
from .StockInfo_HK import HKStockInfo
from .StockInfo_SG import SGStockInfo
from .StockInfo_US import USStockInfo
from .StockInfo_ZhCB import ZhConvertibleBondInfo

import sys
import inspect

classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for name, cls in classes:
    if issubclass(cls, StockInfoBase):
        StockInfoClass.typesDict[cls.codeType] = cls

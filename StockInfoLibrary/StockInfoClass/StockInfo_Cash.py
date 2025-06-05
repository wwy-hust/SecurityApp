# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..CurrencyExchangeManager import CurrencyExchangeMgr


class CashInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.CURRENCY

	def fetchCodeData(self):
		self.resetData()
		self.data['name'] = self.code
		if self.code == 'CNY':
			self.data['price'] = 1.0
		else:
			self.data['price'] = float(CurrencyExchangeMgr.instance().getExchangeRate(self.code, CurrencyType.CNY))
		self.data['real_price'] = self.data['price']
		self.data['dividend_ratio_ttm'] = CurrencyExchangeMgr.instance().getCashBondRate(self.code)

	def initWithCache(self, data):
		self.fetchCodeData()

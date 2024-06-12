# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..CurrencyExchangeManager import CurrencyExchangeMgr
from ..UserDefinedStockInfoData import DEFAULT_SG_INFO, MANUAL_SG_INFO


class SGStockInfo(StockInfoBase):
	currencyType = CurrencyType.SGD
	codeType = CodeType.SG_STOCK

	def fetchCodeData(self):
		global DEFAULT_SG_INFO, MANUAL_SG_INFO
		self.resetData()

		# Fetch Name & Price
		if self.data['name'] == "":
			if self.code in MANUAL_SG_INFO:
				if "name" in MANUAL_SG_INFO[self.code]:
					self.data['name'] = MANUAL_SG_INFO[self.code]["name"]
		if self.data['name'] == "":
			if self.code in DEFAULT_SG_INFO:
				if "name" in DEFAULT_SG_INFO[self.code]:
					self.data['name'] = DEFAULT_SG_INFO[self.code]["name"]

		if self.data['price'] == 0.0:
			if "price" in MANUAL_SG_INFO[self.code]:
				self.data['price'] = MANUAL_SG_INFO[self.code]["price"]
		if self.data['price'] == 0.0:
			if "price" in DEFAULT_SG_INFO[self.code]:
				self.data['price'] = DEFAULT_SG_INFO[self.code]["price"]

		self.data['real_price'] = self.data['price'] * float(CurrencyExchangeMgr.instance().getExchangeRate(self.currencyType, CurrencyType.CNY))

# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..CurrencyExchangeManager import CurrencyExchangeMgr
from ..UserDefinedStockInfoData import DEFAULT_US_INFO, MANUAL_US_INFO


class USStockInfo(StockInfoBase):
	currencyType = CurrencyType.USD
	codeType = CodeType.US_STOCK

	def fetchCodeData(self):
		global DEFAULT_US_INFO, MANUAL_US_INFO
		self.resetData()

		# Fetch Name & Price
		us_stock_data = GetAkShareData("us_stock_data")
		us_stock_filtered = us_stock_data.loc[lambda df:df['symbol'] == self.code, ['cname', 'price', 'mktcap', 'pe']]

		if self.data['name'] == "":
			if self.code in MANUAL_US_INFO:
				if "name" in MANUAL_US_INFO[self.code]:
					self.data['name'] = MANUAL_US_INFO[self.code]["name"]
		if self.data['name'] == "":
			if len(us_stock_filtered) != 0:
				self.data['name'] = us_stock_filtered['cname'].values[0]
		if self.data['name'] == "":
			if self.code in DEFAULT_US_INFO:
				if "name" in DEFAULT_US_INFO[self.code]:
					self.data['name'] = DEFAULT_US_INFO[self.code]["name"]

		if self.data['price'] == 0.0:
			if self.code in MANUAL_US_INFO:
				if "price" in MANUAL_US_INFO[self.code]:
					self.data['price'] = MANUAL_US_INFO[self.code]["price"]
		if self.data['price'] == 0.0:
			if len(us_stock_filtered) != 0:
				self.data['price'] = float(us_stock_filtered['price'].values[0])
		if self.data['price'] == 0.0:
			if self.code in DEFAULT_US_INFO:
				if "price" in DEFAULT_US_INFO[self.code]:
					self.data['price'] = DEFAULT_US_INFO[self.code]["price"]

		self.data['real_price'] = self.data['price'] * float(CurrencyExchangeMgr.instance().getExchangeRate(self.currencyType, CurrencyType.CNY))

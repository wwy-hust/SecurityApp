# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..CurrencyExchangeManager import CurrencyExchangeMgr
from ..UserDefinedStockInfoData import DEFAULT_ETF_INFO, MANUAL_ETF_INFO
from ..Config import G_DataSource, DataSourceType
from ..FutuAPIDataHelper import FutuApi_ETF_GetStockInfoData

class ETFStockInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.ETF

	def postInitWithUserDefinedData(self):
		if self.data['name'] == "":
			if self.code in MANUAL_ETF_INFO:
				if "name" in MANUAL_ETF_INFO[self.code]:
					self.data['name'] = MANUAL_ETF_INFO[self.code]["name"]
		# if self.data['name'] == "":
		# 	if len(etf_filtered) != 0:
		# 		self.data['name'] = etf_filtered["名称"].values[0]
		if self.data['name'] == "":
			if self.code in DEFAULT_ETF_INFO:
				if "name" in DEFAULT_ETF_INFO[self.code]:
					self.data['name'] = DEFAULT_ETF_INFO[self.code]["name"]

		if self.data['price'] == 0.0:
			if self.code in MANUAL_ETF_INFO:
				if "price" in MANUAL_ETF_INFO[self.code]:
					self.data['price'] = MANUAL_ETF_INFO[self.code]["price"]
		# if self.data['price'] == 0.0:
		# 	if len(etf_filtered) != 0:
		# 		self.data['price'] = float(etf_filtered["最新价"].values[0])
		if self.data['price'] == 0.0:
			if self.code in DEFAULT_ETF_INFO:
				if "price" in DEFAULT_ETF_INFO[self.code]:
					self.data['price'] = DEFAULT_ETF_INFO[self.code]["price"]

		if self.data['dividend_ratio_ttm'] == 0.0:
			if self.code in MANUAL_ETF_INFO:
				if "dividend_ratio_ttm" in MANUAL_ETF_INFO[self.code]:
					self.data['dividend_ratio_ttm'] = MANUAL_ETF_INFO[self.code]["dividend_ratio_ttm"]
		if self.data['dividend_ratio_ttm'] == 0.0:
			if self.code in DEFAULT_ETF_INFO:
				if "dividend_ratio_ttm" in DEFAULT_ETF_INFO[self.code]:
					self.data['dividend_ratio_ttm'] = DEFAULT_ETF_INFO[self.code]["dividend_ratio_ttm"]

		self.data['real_price'] = self.data['price']

	def fetchCodeData(self):
		global DEFAULT_ETF_INFO, MANUAL_ETF_INFO
		self.resetData()

		if G_DataSource == DataSourceType.FUTU:
			self.data.update(FutuApi_ETF_GetStockInfoData(self.code))
			self.data['real_price'] = self.data['price']
		elif G_DataSource == DataSourceType.AKSHARE:
			etf_data = GetAkShareData("etf_data")
			etf_filtered = etf_data.loc[lambda df:df['代码'] == self.code, ["名称", "最新价"]]
			if len(etf_filtered) == 0:
				etf_data = GetAkShareData("lof_data")
				etf_filtered = etf_data.loc[lambda df:df['代码'] == self.code, ["名称", "最新价"]]
		self.postInitWithUserDefinedData()

	def initWithCache(self, data):
		self.fetchCodeData()
		self.postInitWithUserDefinedData()

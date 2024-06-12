# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..CurrencyExchangeManager import CurrencyExchangeMgr
from ..UserDefinedStockInfoData import DEFAULT_ETF_INFO, MANUAL_ETF_INFO


class ETFStockInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.ETF

	def fetchCodeData(self):
		global DEFAULT_ETF_INFO, MANUAL_ETF_INFO
		self.resetData()

		etf_data = GetAkShareData("etf_data")
		etf_filtered = etf_data.loc[lambda df:df['代码'] == self.code, ["名称", "最新价"]]
		if len(etf_filtered) == 0:
			etf_data = GetAkShareData("lof_data")
			etf_filtered = etf_data.loc[lambda df:df['代码'] == self.code, ["名称", "最新价"]]

		if self.data['name'] == "":
			if self.code in MANUAL_ETF_INFO:
				if "name" in MANUAL_ETF_INFO[self.code]:
					self.data['name'] = MANUAL_ETF_INFO[self.code]["name"]
		if self.data['name'] == "":
			if len(etf_filtered) != 0:
				self.data['name'] = etf_filtered["名称"].values[0]
		if self.data['name'] == "":
			if self.code in DEFAULT_ETF_INFO:
				if "name" in DEFAULT_ETF_INFO[self.code]:
					self.data['name'] = DEFAULT_ETF_INFO[self.code]["name"]

		if self.data['price'] == 0.0:
			if self.code in MANUAL_ETF_INFO:
				if "price" in MANUAL_ETF_INFO[self.code]:
					self.data['price'] = MANUAL_ETF_INFO[self.code]["price"]
		if self.data['price'] == 0.0:
			if len(etf_filtered) != 0:
				self.data['price'] = float(etf_filtered["最新价"].values[0])
		if self.data['price'] == 0.0:
			if self.code in DEFAULT_ETF_INFO:
				if "price" in DEFAULT_ETF_INFO[self.code]:
					self.data['price'] = DEFAULT_ETF_INFO[self.code]["price"]

		self.data['real_price'] = self.data['price']

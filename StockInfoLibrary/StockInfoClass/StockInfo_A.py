# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..Config import G_DataSource, DataSourceType
from ..FutuAPIDataHelper import FutuApi_A_GetStockInfoData

class AStockInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.A_STOCK

	def fetchCodeData(self):
		self.resetData()
 
		if G_DataSource == DataSourceType.FUTU:
			self.data.update(FutuApi_A_GetStockInfoData(self.code))
			self.data['real_price'] = self.data['price']
		elif G_DataSource == DataSourceType.AKSHARE:
			# Fetch Name & Price
			a_stock_data = GetAkShareData("a_stock_data")
			code_stock_data = a_stock_data.loc[lambda df:df['代码'] == self.code, ['名称', '最新价']]
			if len(code_stock_data) == 0:
				return

			self.data['price'] = float(code_stock_data['最新价'].values[0])
			self.data['real_price'] = self.data['price']
			self.data['name'] = code_stock_data['名称'].values[0]

			# Fetch MarketValue & PETTM
			try:
				lg_indicator = ak.stock_a_indicator_lg(symbol=self.code)
				iLocIdx = 0 if lg_indicator.iloc[0]['trade_date'].year > lg_indicator.iloc[-1]['trade_date'].year else -1
				self.data['market_value'] = round(lg_indicator.iloc[iLocIdx]['total_mv'] / 10000, 2)
				self.data['pe_ttm'] = round(lg_indicator.iloc[iLocIdx]['pe_ttm'], 2)
			except:
				self.data['market_value'] = 1
				self.data['pe_ttm'] = 0.0

	def initWithCache(self, data):
		self.resetData()
		self.data.update(data)
		self.data['real_price'] = self.data['price']

# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..CurrencyExchangeManager import CurrencyExchangeMgr
from ..UserDefinedStockInfoData import DEFAULT_US_INFO, MANUAL_US_INFO
from ..Config import G_DataSource, DataSourceType
from ..FutuAPIDataHelper import FutuApi_US_GetStockInfoData

VOO_HIGH = 0.0
VOO_LOW = 0.0

class USStockInfo(StockInfoBase):
	currencyType = CurrencyType.USD
	codeType = CodeType.US_STOCK

	def fetchCodeData(self):
		global DEFAULT_US_INFO, MANUAL_US_INFO
		global VOO_HIGH, VOO_LOW
		self.resetData()

		if G_DataSource == DataSourceType.FUTU:
			self.data.update(FutuApi_US_GetStockInfoData(self.code))
			self.data['real_price'] = self.data['price'] * float(CurrencyExchangeMgr.instance().getExchangeRate(self.currencyType, CurrencyType.CNY))

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

		if self.data['dividend_ratio_ttm'] == 0.0:
			if self.code in MANUAL_US_INFO:
				if "dividend_ratio_ttm" in MANUAL_US_INFO[self.code]:
					self.data['dividend_ratio_ttm'] = MANUAL_US_INFO[self.code]["dividend_ratio_ttm"]
		if self.data['dividend_ratio_ttm'] == 0.0:
			if self.code in DEFAULT_US_INFO:
				if "dividend_ratio_ttm" in DEFAULT_US_INFO[self.code]:
					self.data['dividend_ratio_ttm'] = DEFAULT_US_INFO[self.code]["dividend_ratio_ttm"]

		self.data['real_price'] = round(self.data['price'] * float(CurrencyExchangeMgr.instance().getExchangeRate(self.currencyType, CurrencyType.CNY)), 2)
		if len(us_stock_filtered['mktcap']) == 0:
			self.data['market_value'] = 0
		else:
			self.data['market_value'] = round(int(us_stock_filtered['mktcap'].values[0]) / 100000000, 2)
		if len(us_stock_filtered['pe']) == 0 or us_stock_filtered['pe'].values[0] is None:
			self.data['pe_ttm'] = 0
		else:
			self.data['pe_ttm'] = round(float(us_stock_filtered['pe'].values[0]), 2)

		try:
			stock_us_daily_df = ak.stock_us_daily(symbol=self.code, adjust="qfq")
			filtered_stock_us_daily_df = stock_us_daily_df[-43:]
			high = filtered_stock_us_daily_df["high"].max()
			low = filtered_stock_us_daily_df["low"].min()

			if VOO_HIGH == 0.0 and VOO_LOW == 0.0:
				stock_us_daily_df = ak.stock_us_daily(symbol="VOO", adjust="qfq")
				filtered_VOO_daily_df = stock_us_daily_df[-43:]
				VOO_HIGH = filtered_VOO_daily_df["high"].max()
				VOO_LOW = filtered_VOO_daily_df["low"].min()

			self.data['volatility'] = round(((high - low) / low) / ((VOO_HIGH - VOO_LOW) / VOO_LOW), 2)
		except:
			self.data['volatility'] = 0.0


	def initWithCache(self, data):
		self.fetchCodeData()

# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..CurrencyExchangeManager import CurrencyExchangeMgr
from ..UserDefinedStockInfoData import DEFAULT_HK_INFO, MANUAL_HK_INFO
from ..Config import G_DataSource, DataSourceType
from ..FutuAPIDataHelper import FutuApi_HK_GetStockInfoData

class HKStockInfo(StockInfoBase):
	currencyType = CurrencyType.HKD
	codeType = CodeType.HK_STOCK

	def fetchCodeData(self):
		self.resetData()

		if G_DataSource == DataSourceType.FUTU:
			self.data.update(FutuApi_HK_GetStockInfoData(self.code))
			self.data['real_price'] = round(self.data['price'] * float(CurrencyExchangeMgr.instance().getExchangeRate(self.currencyType, CurrencyType.CNY)), 2)
		else:
			# Fetch Name & Price
			hk_stock_data = GetAkShareData("hk_stock_data")
			hk_stock_filtered = hk_stock_data.loc[lambda df:df['symbol'] == self.code, ['name', 'lasttrade']]
			if len(hk_stock_filtered) == 0:
				return

			self.data['price'] = float(hk_stock_filtered['lasttrade'].values[0])
			self.data['real_price'] = round(self.data['price'] * float(CurrencyExchangeMgr.instance().getExchangeRate(self.currencyType, CurrencyType.CNY)), 2)
			self.data['name'] = hk_stock_filtered['name'].values[0]

			# Fetch MarketValue & PETTM
			try:
				indicator1 = ak.stock_hk_indicator_eniu(symbol='hk' + self.code, indicator='市值')
				indicator2 = ak.stock_hk_indicator_eniu(symbol='hk' + self.code, indicator='市盈率')
				self.data['market_value'] = round(indicator1['market_value'].values[-1], 2)
				self.data['pe_ttm'] = round(indicator2['pe'].values[-1], 2)
			except:
				self.data['market_value'] = 0
				self.data['pe_ttm'] = 0

		
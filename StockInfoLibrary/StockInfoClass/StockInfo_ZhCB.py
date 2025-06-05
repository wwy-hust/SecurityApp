# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..CurrencyExchangeManager import CurrencyExchangeMgr
from ..UserDefinedStockInfoData import DEFAULT_ZHCVB_INFO, MANUAL_ZHCVB_INFO


class ZhConvertibleBondInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.ZH_CONVERTIBLE_BOND

	def fetchCodeData(self):
		self.resetData()
		zh_bond_data = GetAkShareData("zh_convertible_bond_data")
		code_bond_data = zh_bond_data.loc[lambda df:df["code"] == self.code, ['name', 'trade']]
		if len(code_bond_data) == 0:
			return
	
		self.data['price'] = float(code_bond_data['trade'].values[0])
		self.data['real_price'] = self.data['price']
		self.data['name'] = code_bond_data['name'].values[0]

	def initWithCache(self, data):
		self.fetchCodeData()


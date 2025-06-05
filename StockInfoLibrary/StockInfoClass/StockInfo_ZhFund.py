# -*- coding:utf-8 -*-
import akshare as ak
from .BaseClass import StockInfoBase
from ..TypeDefine import CodeType, CurrencyType
from ..AkShareDataHelper import GetAkShareData, CallAKShareFuncWithCache
from ..CurrencyExchangeManager import CurrencyExchangeMgr
from ..UserDefinedStockInfoData import DEFAULT_ZH_PUBLIC_FUND_INFO, MANUAL_ZH_PUBLIC_FUND_INFO


class ZhPublicFundInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.ZH_PUBLIC_FUND

	def fetchCodeData(self):
		self.resetData()
		info = ak.fund_individual_basic_info_xq(symbol=self.code)

		nameIndex = list(info['item']).index('基金名称')
		self.data['name'] = info['value'][nameIndex]

		fullnameIndex = list(info['item']).index('基金全称')
		self.data['fullname'] = info['value'][fullnameIndex]

		companyIndex = list(info['item']).index('基金公司')
		self.data['company'] = info['value'][companyIndex]

		fundTypeIndex = list(info['item']).index('基金类型')
		self.data['fundType'] = info['value'][fundTypeIndex]

		scaleIndex = list(info['item']).index('最新规模')
		self.data['scale'] = info['value'][scaleIndex]

		strategyIndex = list(info['item']).index('投资策略')
		self.data['strategy'] = info['value'][strategyIndex]

		targetIndex = list(info['item']).index('投资目标')
		self.data['target'] = info['value'][targetIndex]

		benchmarkIndex = list(info['item']).index('业绩比较基准')
		self.data['benchmark'] = info['value'][benchmarkIndex]

		raw_df = CallAKShareFuncWithCache("fund_open_fund_daily_em")
		fund_df = raw_df.loc[lambda d:d['基金代码']==self.code]
		if len(fund_df) == 0:
			return
		fund_series = fund_df.iloc[0]

		self.data['name'] = fund_series.iloc[1]
		if fund_series.iloc[2] == "":
			self.data['price'] = fund_series.iloc[4]
		else:
			self.data['price'] = fund_series.iloc[2]
		self.data['real_price'] = self.data['price']

		# print(fund_df, fund_series)

	def initWithCache(self, data):
		self.fetchCodeData()

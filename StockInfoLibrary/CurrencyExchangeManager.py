# -*- coding:utf-8 -*-
from . import AkShareDataHelper
from .UserDefinedStockInfoData import DEFAULT_CASH_EXCHANGE_RATE, MANUAL_CASH_EXCHANGE_RATE


class CurrencyExchangeMgr(object):
	_instance = None

	@classmethod
	def instance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		self.foreign_exchange_data = None
		try:
			self.foreign_exchange_data = AkShareDataHelper.GetAkShareData("foreign_exchange_data")
		except:
			self.foreign_exchange_data = None
			print("encounter error in fetching exchangeRate.. use Default exchange", DEFAULT_CASH_EXCHANGE_RATE)

	def getExchangeRate(self, fromCurrencyType, toCurrencyType):
		global DEFAULT_CASH_EXCHANGE_RATE, MANUAL_CASH_EXCHANGE_RATE
		if len(MANUAL_CASH_EXCHANGE_RATE) != 0:
			if "ccyPair" in MANUAL_CASH_EXCHANGE_RATE:
				return MANUAL_CASH_EXCHANGE_RATE.get("%s:%s" % (fromCurrencyType, toCurrencyType), 1.0)
		if self.foreign_exchange_data is not None:
			if "ccyPair" in self.foreign_exchange_data:
				exchangeRate = float(self.foreign_exchange_data.loc[lambda df:df['ccyPair'] == "%s/%s" % (fromCurrencyType, toCurrencyType), 'bidPrc'].values[0])
			else:
				exchangeRate = float(self.foreign_exchange_data.loc[lambda df:df['货币对'] == "%s/%s" % (fromCurrencyType, toCurrencyType), '买报价'].values[0])
			return exchangeRate
		else:
			return DEFAULT_CASH_EXCHANGE_RATE.get("%s:%s" % (fromCurrencyType, toCurrencyType), 1.0)

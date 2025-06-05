# -*- coding:utf-8 -*-
import datetime
import math
from .TypeDefine import *
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

	def get_previous_working_day(self):
		today = datetime.date.today()
		if today.weekday() == 0:  # 周一，前一个工作日是上周五
			previous_day = today - datetime.timedelta(days=3)
		elif today.weekday() == 6:  # 周日，前一个工作日是上周五
			previous_day = today - datetime.timedelta(days=2)
		else:  # 其他工作日，前一个工作日就是前一天
			previous_day = today - datetime.timedelta(days=1)
		return previous_day.strftime("%Y%m%d")

	def getCashBondRate(self, currencyType):
		t = self.get_previous_working_day()
		RateData = AkShareDataHelper.GetAkShareData("bond_zh_us_rate", kwargs={"start_date":t})
		# print("cash bound ",currencyType, t, RateData['美国国债收益率10年'].values)
		if currencyType in (CurrencyType.USD, CurrencyType.HKD):
			found = False
			foundVal = 0.0
			index = -1
			while found == False:
				foundVal = RateData['美国国债收益率10年'].values[index]
				if isinstance(foundVal, float) and not math.isnan(foundVal):
					found = True
				else:
					index -= 1
			# print("foundVal for ", currencyType, foundVal)
			return foundVal
		elif currencyType == CurrencyType.CNY:
			return RateData['中国国债收益率10年'].values[-1]
		else:
			return 0.0

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

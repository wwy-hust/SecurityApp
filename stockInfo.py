# -*- coding:utf-8 -*-
from utils import *


class CodeType(object):
	A_STOCK = 0
	HK_STOCK = 1
	US_STOCK = 2
	ETF = 3
	CURRENCY = 4

	INVALID = 9999


class CurrencyType(object):
	CNY = "CNY"
	HKD = "HKD"
	USD = "USD"


class CurrencyExchangeMgr(object):
	_instance = None

	@classmethod
	def instance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		self.foreign_exchange_data = getBasicData("foreign_exchange_data")

	def getExchangeRate(self, fromCurrencyType, toCurrencyType):
		exchangeRate = float(self.foreign_exchange_data.loc[lambda df:df['ccyPair'] == "%s/%s" % (fromCurrencyType, toCurrencyType), 'bidPrc'].values[0])
		return exchangeRate


def getCodeType(code):
	if not isCodeValid(code):
		code_type = CodeType.INVALID
	elif isCodeAStock(code):
		code_type = CodeType.A_STOCK
	elif isCodeHKStock(code):
		code_type = CodeType.HK_STOCK
	elif isCodeETF(code):
		code_type = CodeType.ETF
	elif isCodeCash(code):
		code_type = CodeType.CURRENCY
	elif isCodeUSStock(code):
		code_type = CodeType.US_STOCK
	else:
		code_type = CodeType.INVALID
	return code_type


class StockInfoClass(type):
	typesDict = {}

	def __new__(mcs, clsname, bases, attrs):
		c = super(StockInfoClass, mcs).__new__(mcs, clsname, bases, attrs)
		for itemType in c.itemType:
			mcs.typesDict[c.codeType] = c
		return c


class StockInfoProxy(object):
	def __init__(self, code):
		super(StockInfoProxy, self).__init__()
		self.code = code
		self.code_type = getCodeType(code)

	def __getattr__(self, name):
		return getattr(StockInfoClass.typesDict.get(self.code_type, StockInfoBase)(self), name)

	def __str__(self):
		return 'StockInfoProxy => %s:(%s)' % (StockInfoClass.typesDict.get(self.code_type, StockInfoBase).__name__, self.code)


class StockInfoBase(object):
	code = ""
	codeType = CodeType.INVALID
	currencyType = CurrencyType.CNY

	data = {}

	def __init__(self, proxy):
		self.proxy = proxy
		self.code = proxy.code
		self.code_type = proxy.code_type

	def resetData(self):
		self.data['price'] = 0.0
		self.data['real_price'] = 0.0
		self.data['name'] = ""
		self.data['market_value'] = 0.0
		self.data['pe_ttm'] = 0.0

	def fetchCodeData(self):
		raise NotImplementedError

	def __getattr__(self, attr):
		return self.data.get(attr, None)


class AStockInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.A_STOCK

	def fetchCodeData(self):
		self.resetData()

		# Fetch Name & Price
		a_stock_data = getBasicData("a_stock_data")
		code_stock_data = a_stock_data.loc[lambda df:df['code'] == self.code, ['name', 'trade']]
		if len(code_stock_data) == 0:
			return

		self.data['price'] = float(code_stock_data['trade'].values[0])
		self.data['real_price'] = self.data['price']
		self.data['name'] = code_stock_data['name'].values[0]

		# Fetch MarketValue & PETTM
		lg_indicator = ak.stock_a_lg_indicator(stock=self.code)
		self.data['market_value'] = round(lg_indicator['total_mv'][0] / 10000, 2)
		self.data['pe_ttm'] = round(lg_indicator['pe_ttm'][0], 2)


class HKStockInfo(StockInfoBase):
	currencyType = CurrencyType.HKD
	codeType = CodeType.HK_STOCK

	def fetchCodeData(self):
		self.resetData()

		# Fetch Name & Price
		hk_stock_data = getBasicData("hk_stock_data")
		hk_stock_filtered = hk_stock_data.loc[lambda df:df['symbol'] == self.code, ['name', 'lasttrade']]
		if len(hk_stock_filtered) == 0:
			return

		self.data['price'] = float(hk_stock_filtered['lasttrade'].values[0])
		self.data['real_price'] = self.data['price'] * float(CurrencyExchangeMgr.instance().getExchangeRate('HKD', 'CNY'))
		self.data['name'] = hk_stock_filtered['name'].values[0]

		# Fetch MarketValue & PETTM
		indicator1 = ak.stock_hk_eniu_indicator(symbol='hk' + self.code, indicator='市值')
		indicator2 = ak.stock_hk_eniu_indicator(symbol='hk' + self.code, indicator='市盈率')
		self.data['market_value'] = round(indicator1['market_value'].values[-1], 2)
		self.data['pe_ttm'] = round(indicator2['pe'].values[-1], 2)


class USStockInfo(StockInfoBase):
	currencyType = CurrencyType.USD
	codeType = CodeType.US_STOCK

	def fetchCodeData(self):
		self.resetData()

		# Fetch Name & Price
		us_stock_data = getBasicData("us_stock_data")
		us_stock_filtered = us_stock_data.loc[lambda df:df['symbol'] == self.code, ['cname', 'price', 'mktcap', 'pe']]
		if len(us_stock_filtered) == 0:
			return

		self.data['price'] = float(us_stock_filtered['price'].values[0])
		self.data['real_price'] = self.data['price'] * float(CurrencyExchangeMgr.instance().getExchangeRate('USD', 'CNY'))
		self.data['name'] = us_stock_filtered['cname'].values[0]
		self.data['market_value'] = round(float(us_stock_filtered['mktcap'].values[0]) / 100000000, 2)
		self.data['pe_ttm'] = round(float(us_stock_filtered['pe'].values[0]), 2)


class ETFStockInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.ETF

	def fetchCodeData(self):
		self.resetData()

		etf_data = getBasicData("etf_data")
		etf_filtered = etf_data.loc[lambda df:df['基金代码'] == self.code, ["基金简称", "市价"]]
		if len(etf_filtered) == 0:
			return

		self.data['price'] = float(etf_filtered["市价"].values[0])
		self.data['real_price'] = self.data['price']
		self.data['name'] = etf_filtered["基金简称"].values[0]


class CurrencyInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.CURRENCY

	def fetchCodeData(self):
		self.resetData()
		self.data['name'] = self.code
		if self.code == 'CNY':
			self.data['price'] = 1.0
		else:
			self.data['price'] = float(CurrencyExchangeMgr.instance().getExchangeRate(self.code, 'CNY'))
		self.data['real_price'] = self.data['price']


def __init_globals():
	import sys
	import inspect
	classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
	for name, cls in classes:
		if issubclass(cls, StockInfoBase):
			StockInfoClass.typesDict[cls.codeType] = cls

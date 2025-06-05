# -*- coding:utf-8 -*-
from .StockCodeHelper import GetCodeType, GetTypeInPortfolio
from ..TypeDefine import CodeType, TypeInPortfolio, CurrencyType

class StockInfoClass(type):
	typesDict = {}

	def __new__(mcs, clsname, bases, attrs):
		c = super(StockInfoClass, mcs).__new__(mcs, clsname, bases, attrs)
		for itemType in c.itemType:
			mcs.typesDict[c.codeType] = c
		return c


class StockInfoProxy(object):
	def initWithCode(self, code):
		codeStr = code.split(".")
		if len(codeStr) < 2:
			print("Invalid Code: ", codeStr)
		typeCode = codeStr[0]
		readCode = ".".join(codeStr[1:])
		self.originCode = code
		self.code = readCode
		self.code_type = GetCodeType(typeCode)
		self.stockInfo = None
		self.typeInPorfolio = GetTypeInPortfolio(self)

	def __init__(self, code):
		super(StockInfoProxy, self).__init__()
		self.initWithCode(code)

	def __getattr__(self, name):
		if self.stockInfo:
			return getattr(self.stockInfo, name)
		return getattr(StockInfoClass.typesDict.get(self.code_type, StockInfoBase)(self), name)

	def __str__(self):
		return 'StockInfoProxy => %s:(%s) {%s}' % (StockInfoClass.typesDict.get(self.code_type, StockInfoBase).__name__, self.code, self.getDataStr())


class StockInfoBase(object):
	code = ""
	codeType = CodeType.INVALID
	currencyType = CurrencyType.CNY

	def __init__(self, proxy):
		proxy.stockInfo = self
		self.code = proxy.code
		self.code_type = proxy.code_type
		self.data = {}

	def resetData(self):
		self.data['price'] = 0.0
		self.data['real_price'] = 0.0
		self.data['name'] = ""
		# self.data['market_value'] = 0.0
		# self.data['pe_ttm'] = 0.0
		self.data['dividend_ratio_ttm'] = 0.0
		self.data['volatility'] = 0.0 # 波动率 = 标的2月内波动 / 大盘指数2月内波动
		# self.data['profit'] = None

	def fetchCodeData(self):
		raise NotImplementedError

	def initWithCache(self, data):
		raise NotImplementedError

	def __getattr__(self, attr):
		return self.data.get(attr, None)

	def getDataStr(self):
		return str(self.data)

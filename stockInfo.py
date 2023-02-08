# -*- coding:utf-8 -*-
from utils import *
from copy import deepcopy


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


A_STOCK_LRB_INDICATOR_MAP = {
	"报告期": "REPORT_DATE",

	"营业总收入": "TOTAL_OPERATE_INCOME",
	"主营业务收入": "OPERATE_INCOME",

	"营业总成本": "TOTAL_OPERATE_COST",
	"营业成本": "OPERATE_COST",
	"销售费用": "SALE_EXPENSE",
	"研发费用": "RESEARCH_EXPENSE",
	"管理费用": "MANAGE_EXPENSE",
	"财务费用": "FINANCE_EXPENSE",
	"利息支出": "INTEREST_EXPENSE",
	"手续费及佣金支出": "FEE_COMMISSION_EXPENSE",

	"营业利润": "OPERATE_PROFIT",
	"(加)营业外收入": "NONBUSINESS_INCOME",
	"(减)营业外支出": "NONBUSINESS_EXPENSE",

	"利润总额": "TOTAL_PROFIT",
	"(减)所得税": "INCOME_TAX",

	"净利润": "NETPROFIT",

	# 按照经营持续性分类
	"持续经营净利润": "CONTINUED_NETPROFIT",
	"非持续经营净利润": "DISCONTINUED_NETPROFIT",
	# 按所有权归属分类
	"归属于母公司股东的净利润": "PARENT_NETPROFIT",
	"少数股东损益": "MINORITY_INTEREST",
}

HK_STOCK_MAP = {
	"报告期": "截止日期",

	"营业总收入": "营业收入(计算)",
	"其他收入": "其他收入",

	"营业成本": "销售成本",
	"销售费用": "销售及分销成本",
	"研发费用": "研发费用",
	"管理费用": "行政开支",
	"财务费用": "财务成本",
	"其他支出": "其他支出",
	"资产减值": "资产减值损失",

	"营业利润": "经营溢利(计算)",
	"影响税前利润的其他项目": "影响税前利润的其他项目",

	"利润总额": "税前利润",
	"(减)所得税": "所得税",
	"影响净利润的其他项目": "影响净利润的其他项目",
	
	"净利润": "净利润",

	# 按所有权归属分类
	"归属于母公司股东的净利润": "本公司拥有人应占净利润|2",
	"少数股东损益": "非控股权益应占净利润|2",
}

class CurrencyExchangeMgr(object):
	_instance = None

	LocalForeignExchangeRateMap = {
		"HKD:CNY": 0.854,
		"USD:CNY": 6.7015,
	}

	@classmethod
	def instance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		self.foreign_exchange_data = None
		try:
			self.foreign_exchange_data = getBasicData("foreign_exchange_data")
		except:
			self.foreign_exchange_data = None
			print("encounter error in fetching exchangeRate.. use Default exchange", self.LocalForeignExchangeRateMap)

	def getExchangeRate(self, fromCurrencyType, toCurrencyType):
		if self.foreign_exchange_data is not None:
			if "ccyPair" in self.foreign_exchange_data:
				exchangeRate = float(self.foreign_exchange_data.loc[lambda df:df['ccyPair'] == "%s/%s" % (fromCurrencyType, toCurrencyType), 'bidPrc'].values[0])
			else:
				exchangeRate = float(self.foreign_exchange_data.loc[lambda df:df['货币对'] == "%s/%s" % (fromCurrencyType, toCurrencyType), '买报价'].values[0])
			return exchangeRate
		else:
			
			return self.LocalForeignExchangeRateMap.get("%s:%s" % (fromCurrencyType, toCurrencyType), 1.0)


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
		self.stockInfo = None

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
		self.data['market_value'] = 0.0
		self.data['pe_ttm'] = 0.0
		self.data['profit'] = None

	def fetchCodeData(self, fetchProfitStatement=False):
		raise NotImplementedError

	def __getattr__(self, attr):
		return self.data.get(attr, None)

	def getDataStr(self):
		return str(self.data)


class AStockInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.A_STOCK

	def fetchCodeData(self, fetchProfitStatement=False):
		self.resetData()

		# Fetch Name & Price
		a_stock_data = getBasicData("a_stock_data")
		code_stock_data = a_stock_data.loc[lambda df:df['代码'] == self.code, ['名称', '最新价']]
		if len(code_stock_data) == 0:
			return

		self.data['price'] = float(code_stock_data['最新价'].values[0])
		self.data['real_price'] = self.data['price']
		self.data['name'] = code_stock_data['名称'].values[0]

		# Fetch MarketValue & PETTM
		try:
			lg_indicator = ak.stock_a_lg_indicator(symbol=self.code)
			iLocIdx = 0 if lg_indicator.iloc[0]['trade_date'].year > lg_indicator.iloc[-1]['trade_date'].year else -1
			self.data['market_value'] = round(lg_indicator.iloc[iLocIdx]['total_mv'] / 10000, 2)
			self.data['pe_ttm'] = round(lg_indicator.iloc[iLocIdx]['pe_ttm'], 2)
		except:
			self.data['market_value'] = 1
			self.data['pe_ttm'] = 0.0

		# # Fetch Profit Statement
		if fetchProfitStatement:
			lrb = callAKShareFuncWithCache("stock_profit_sheet_by_quarterly_em", getSymbolWithPrefix(self.code))
			# lrb = ak.stock_profit_sheet_by_quarterly_em(getSymbolWithPrefix(self.code))
			fetchLRBKeys = A_STOCK_LRB_INDICATOR_MAP.values()
			df = lrb.loc[:, fetchLRBKeys]
			self.data['profit'] = df


class HKStockInfo(StockInfoBase):
	currencyType = CurrencyType.HKD
	codeType = CodeType.HK_STOCK

	def fetchCodeData(self, fetchProfitStatement=False):
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

		# # Fetch Profit Statement
		if fetchProfitStatement:
			return
			df = callAKShareFuncWithCache("stock_financial_hk_report_em", stock=self.code, symbol="利润表", indicator="报告期")
			# df = ak.stock_financial_hk_report_em(stock=self.code, symbol="利润表", indicator="报告期")
			fetchLRBKeys = HK_STOCK_MAP.values()
			df1 = df.loc[:, fetchLRBKeys]
			self.data['profit'] = df1


class USStockInfo(StockInfoBase):
	currencyType = CurrencyType.USD
	codeType = CodeType.US_STOCK

	def fetchCodeData(self, fetchProfitStatement=False):
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

		# # Fetch Profit Statement
		if fetchProfitStatement:
			pass

class ETFStockInfo(StockInfoBase):
	currencyType = CurrencyType.CNY
	codeType = CodeType.ETF

	def fetchCodeData(self, fetchProfitStatement=False):
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

# -*- coding:utf-8 -*-

class CodeType(object):
	A_STOCK = 0
	HK_STOCK = 1
	US_STOCK = 2
	ETF = 3
	CURRENCY = 4
	ZH_CONVERTIBLE_BOND = 5
	SG_STOCK = 6
	ZH_PUBLIC_FUND = 7

	INVALID = 9999


class TypeInPortfolio(object):
	A = "A"
	HK = "HK"
	US = "US"
	CASH = "CASH"

	INVALID = "INV"


class CurrencyType(object):
	CNY = "CNY"
	HKD = "HKD"
	USD = "USD"
	SGD = "SGD"



# -*- coding:utf-8 -*-
from ..TypeDefine import CodeType, TypeInPortfolio

def GetCodeType(typeCode):
	if typeCode == "a":
		code_type = CodeType.A_STOCK
	elif typeCode == "hk":
		code_type = CodeType.HK_STOCK
	elif typeCode == "us":
		code_type = CodeType.US_STOCK
	elif typeCode == "etf":
		code_type = CodeType.ETF
	elif typeCode == "cash":
		code_type = CodeType.CURRENCY
	elif typeCode == "cb":
		code_type = CodeType.ZH_CONVERTIBLE_BOND
	elif typeCode == "sg":
		code_type = CodeType.SG_STOCK
	elif typeCode == "fund":
		code_type = CodeType.ZH_PUBLIC_FUND
	else:
		code_type = CodeType.INVALID
	return code_type


FOREIGN_ETF_CODELIST = ("513880", "513000", "159866", "513520", "164824", "159502", "159509", "501225")
HK_ETF_CODELIST = ("513120", )


def GetTypeInPortfolio(stockInfo):
	if stockInfo.code_type == CodeType.HK_STOCK:
		return TypeInPortfolio.HK
	elif stockInfo.code_type == CodeType.SG_STOCK:
		return TypeInPortfolio.US
	elif stockInfo.code_type == CodeType.US_STOCK:
		return TypeInPortfolio.US
	elif stockInfo.code_type == CodeType.A_STOCK or stockInfo.code_type == CodeType.ZH_CONVERTIBLE_BOND:
		return TypeInPortfolio.A
	elif stockInfo.code_type == CodeType.ETF:
		if stockInfo.code in FOREIGN_ETF_CODELIST:
			return TypeInPortfolio.US
		elif stockInfo.code in HK_ETF_CODELIST:
			return TypeInPortfolio.HK
		else:
			return TypeInPortfolio.A
	elif stockInfo.code_type == CodeType.CURRENCY:
		return TypeInPortfolio.CASH
	elif stockInfo.code_type == CodeType.ZH_PUBLIC_FUND:
		return TypeInPortfolio.A
	return TypeInPortfolio.INVALID



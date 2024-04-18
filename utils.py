# -*- coding:utf-8 -*-
import akshare as ak
import pandas as pd
import numpy as np
import os, sys
import time
import json


FOREIGN_ETF_CODELIST = ("513880", "513000", "159866", "513520", "164824", "159502", "159509", "501225")
HK_ETF_CODELIST = ("513120", )

ZH_CONVERTIBLE_BOND_CODE_SET_CACHE = None

def isCodeAStock(code):
	if not code.isdigit():
		return False
	code = str(code)
	return len(code) == 6 and code[0] in ('0', '3', '6')


def isCodeHKStock(code):
	if not code.isdigit():
		return False
	code = str(code)
	return len(code) == 5


def isCodeETF(code):
	if not code.isdigit():
		return False
	code = str(code)
	return len(code) == 6 and code[0] in ('1', '5')


def isCodeCash(code):
	code = str(code)
	return code in ('CNY', 'HKD', 'USD')


def isCodeZHConvertibleBond(code):
	global ZH_CONVERTIBLE_BOND_CODE_SET_CACHE
	if ZH_CONVERTIBLE_BOND_CODE_SET_CACHE is None:
		codeDfRaw = getBasicData('zh_convertible_bond_code')
		ZH_CONVERTIBLE_BOND_CODE_SET_CACHE = set(codeDfRaw['债券代码'])
	return code in ZH_CONVERTIBLE_BOND_CODE_SET_CACHE


def isCodeUSStock(code):
	return not isCodeAStock(code) and not isCodeHKStock(code) and not isCodeETF(code) and not isCodeCash(code)


def is_contains_chinese(strs):
	for _char in strs:
		if '\u4e00' <= _char <= '\u9fa5':
			return True
	return False


def containInValidChar(strs):
	for c in ('.', '*', ',', '`', '!', '@', '#', '$', '%', '^', '&', '(', ')'):
		if c in strs:
			return True
	return False


def isCodeValid(code):
	code = str(code)
	isValid = code != 'nan' and not is_contains_chinese(code) and not containInValidChar(code)
	# print('checking code', code, isValid)
	return isValid


def getSymbolWithPrefix(code):
	if isCodeAStock(code):
		if code[0] in ('0', '3'):
			return "sz" + code
		else:
			return "SH" + code
	else:
		return code


def formatToString_yoy(yoy):
	return "%02.02f%%" % (yoy * 100)


def formatToString_profit(profit):
	if profit > 10000000:	# 千万及亿如此显示
		return "%02.02f亿" % (profit / 100000000)
	elif profit > 10000:
		return "%02.02f万" % (profit / 10000)
	else:
		return "%02.02f" % profit


def reportDateList(year):
    ret = []
    ret.append("%d-03-31" % year)
    ret.append("%d-06-30" % year)
    ret.append("%d-09-30" % year)
    ret.append("%d-12-31" % year)
    return tuple(ret)


FOREIGN_EXCHANGE_DATA = None
A_STOCK_DATA = None
HK_STOCK_DATA = None
ETF_DATA = None
LOF_DATA = None
US_STOCK_DATA = None
ZH_CONVERTIBLE_BOND_DATA = None
ZH_CONVERTIBLE_BOND_CODE = None
OPEN_FUND_DAILY_DATA = None


AKShareDataMap = {
	"foreign_exchange_data": ('fx_spot_quote', 'data/foreign_exchange_data.pickle', FOREIGN_EXCHANGE_DATA),
	"a_stock_data": ('stock_zh_a_spot_em', 'data/a_stock_data.pickle', A_STOCK_DATA),
	"hk_stock_data": ('stock_hk_spot', 'data/hk_stock_data.pickle', HK_STOCK_DATA),
	"etf_data": ('fund_etf_spot_em', 'data/etf_data.pickle', ETF_DATA),
	"lof_data": ('fund_lof_spot_em', 'data/lof_data.pickle', LOF_DATA),
	"us_stock_data": ('stock_us_spot', 'data/us_stock_data.pickle', US_STOCK_DATA),
	"zh_convertible_bond_data": ('bond_zh_hs_cov_spot', 'data/zh_convertible_bond_data.pickle', ZH_CONVERTIBLE_BOND_DATA),
	"zh_convertible_bond_code": ('bond_zh_cov_info_ths', 'data/zh_convertible_bond_code.pickle', ZH_CONVERTIBLE_BOND_CODE),
	"open_fund_daily_data": ('fund_open_fund_daily_em', 'data/open_fund_daily_data.pickle', OPEN_FUND_DAILY_DATA),
}

clearedThisTime = False
def clearCacheData():
	global clearedThisTime
	if clearedThisTime:
		return
	clearedThisTime = True
	for path, dir_list, file_list in os.walk("data"):
		for _file in file_list:
			os.remove(os.path.join(path, _file))
		for _dir in dir_list:
			os.rmdir(os.path.join(path, _dir))
		print("Cleared All file under data folder")


def cacheAllAKShareData():
	for key, (funcName, filePath, cacheData) in AKShareDataMap.items():
		print("Caching AKShare Data for %s" % key)
		getBasicData(key, True)


def getBasicData(getFileKey=None, force=False):
	global FOREIGN_EXCHANGE_DATA, A_STOCK_DATA, HK_STOCK_DATA, ETF_DATA, LOF_DATA, US_STOCK_DATA, ZH_CONVERTIBLE_BOND_DATA, OPEN_FUND_DAILY_DATA
	global AKShareDataMap

	TIME_STAMP_FILE_PATH = "data/config.txt"

	if force:
		clearCacheData()

	timeStr = time.strftime("%Y-%m-%d", time.localtime())
	if os.path.exists(TIME_STAMP_FILE_PATH):
		content = None
		with open(TIME_STAMP_FILE_PATH) as cfgFile:
			content = json.load(cfgFile)
		if content and content["datetime"] != timeStr:
			clearCacheData()
			with open(TIME_STAMP_FILE_PATH, "w") as cfgFile:
				json.dump({"datetime": timeStr}, cfgFile, indent=4)
	else:
		clearCacheData()
		with open(TIME_STAMP_FILE_PATH, "w") as cfgFile:
			json.dump({"datetime": timeStr}, cfgFile, indent=4)

	if getFileKey is not None:
		funcName, localFileName, globalVal = AKShareDataMap[getFileKey]
		if globalVal is not None:
			pass
		elif not os.path.exists(localFileName):
			# print("gettting %s from ak.%s" % (getFileKey, funcName))
			globalVal = getattr(ak, funcName)()
			globalVal.to_pickle(localFileName)
		else:
			# print("loading %s from %s" % (getFileKey, localFileName))
			globalVal = pd.read_pickle(localFileName)
		return globalVal


def callAKShareFuncWithCache(funcName, *args, **kwargs):
	localFileName = funcName
	for arg in args:
		localFileName += "_%s" % arg
	for k, arg in kwargs.items():
		localFileName += "_%s" % arg
	localFilePath = "data/%s.pickle" % localFileName
	if os.path.exists(localFilePath):
		ret = pd.read_pickle(localFilePath)
		print("read from cache %s" % localFileName)
		return ret
	else:
		ret = getattr(ak, funcName)(*args)
		ret.to_pickle(localFilePath)
		return ret
# -*- coding:utf-8 -*-
import akshare as ak
import pandas as pd
import numpy as np
import os, sys
import time
import json


def isCodeAStock(code):
	code = str(code)
	return len(code) == 6 and code[0] in ('0', '3', '6')


def isCodeHKStock(code):
	code = str(code)
	return len(code) == 5


def isCodeETF(code):
	code = str(code)
	return len(code) == 6 and code[0] in ('1', '5')


def isCodeCash(code):
	code = str(code)
	return code in ('CNY', 'HKD', 'USD')


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
US_STOCK_DATA = None
OPEN_FUND_DAILY_DATA = None


def clearCacheData():
	for path, dir_list, file_list in os.walk("data"):
		for _file in file_list:
			os.remove(os.path.join(path, _file))
		for _dir in dir_list:
			os.rmdir(os.path.join(path, _dir))
		print("Cleared All file under data folder")


def getBasicData(getFileKey=None):
	global FOREIGN_EXCHANGE_DATA, A_STOCK_DATA, HK_STOCK_DATA, ETF_DATA, US_STOCK_DATA, OPEN_FUND_DAILY_DATA

	aMap = {
		"foreign_exchange_data": ('fx_spot_quote', 'data/foreign_exchange_data.pickle', FOREIGN_EXCHANGE_DATA),
		"a_stock_data": ('stock_zh_a_spot_em', 'data/a_stock_data.pickle', A_STOCK_DATA),
		"hk_stock_data": ('stock_hk_spot', 'data/hk_stock_data.pickle', HK_STOCK_DATA),
		"etf_data": ('fund_em_etf_fund_daily', 'data/etf_data.pickle', ETF_DATA),
		"us_stock_data": ('stock_us_spot', 'data/us_stock_data.pickle', US_STOCK_DATA),
		"open_fund_daily_data": ('fund_open_fund_daily_em', 'data/fund_open_fund_daily_em.pickle', OPEN_FUND_DAILY_DATA),
	}

	TIME_STAMP_FILE_PATH = "data/config.txt"

	timeStr = time.strftime("%Y-%m-%d %H", time.localtime())
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
		funcName, localFileName, globalVal = aMap[getFileKey]
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
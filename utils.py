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


FOREIGN_EXCHANGE_DATA = None
A_STOCK_DATA = None
HK_STOCK_DATA = None
ETF_DATA = None
US_STOCK_DATA = None


def clearCacheData():
	for path, dir_list, file_list in os.walk("data"):
		for _file in file_list:
			os.remove(os.path.join(path, _file))
		for _dir in dir_list:
			os.rmdir(os.path.join(path, _dir))
		print("Cleared All file under data")


def getBasicData(getFileKey=None):
	global FOREIGN_EXCHANGE_DATA, A_STOCK_DATA, HK_STOCK_DATA, ETF_DATA, US_STOCK_DATA

	aMap = {
		"foreign_exchange_data": ('fx_spot_quote', 'data/foreign_exchange_data.pickle', FOREIGN_EXCHANGE_DATA),
		"a_stock_data": ('stock_zh_a_spot', 'data/a_stock_data.pickle', A_STOCK_DATA),
		"hk_stock_data": ('stock_hk_spot', 'data/hk_stock_data.pickle', HK_STOCK_DATA),
		"etf_data": ('fund_em_etf_fund_daily', 'data/etf_data.pickle', ETF_DATA),
		"us_stock_data": ('stock_us_spot', 'data/us_stock_data.pickle', US_STOCK_DATA),
	}

	TIME_STAMP_FILE_PATH = "data/config.txt"

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


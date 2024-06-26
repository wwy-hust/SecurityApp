# -*- coding:utf-8 -*-
import akshare as ak
import pandas as pd
import numpy as np
import os, sys
import time
import json


FOREIGN_EXCHANGE_DATA = None
A_STOCK_DATA = None
HK_STOCK_DATA = None
ETF_DATA = None
LOF_DATA = None
US_STOCK_DATA = None
ZH_CONVERTIBLE_BOND_DATA = None
ZH_CONVERTIBLE_BOND_CODE = None
OPEN_FUND_DAILY_DATA = None
BOND_ZH_US_RATE = None


AKShareDataMap = {
	"foreign_exchange_data": ('fx_spot_quote', '/AkshareDownloadedData/foreign_exchange_data.pickle', FOREIGN_EXCHANGE_DATA),
	"a_stock_data": ('stock_zh_a_spot_em', '/AkshareDownloadedData/a_stock_data.pickle', A_STOCK_DATA),
	"hk_stock_data": ('stock_hk_spot', '/AkshareDownloadedData/hk_stock_data.pickle', HK_STOCK_DATA),
	"etf_data": ('fund_etf_spot_em', '/AkshareDownloadedData/etf_data.pickle', ETF_DATA),
	"lof_data": ('fund_lof_spot_em', '/AkshareDownloadedData/lof_data.pickle', LOF_DATA),
	"us_stock_data": ('stock_us_spot', '/AkshareDownloadedData/us_stock_data.pickle', US_STOCK_DATA),
	"zh_convertible_bond_data": ('bond_zh_hs_cov_spot', '/AkshareDownloadedData/zh_convertible_bond_data.pickle', ZH_CONVERTIBLE_BOND_DATA),
	"zh_convertible_bond_code": ('bond_zh_cov_info_ths', '/AkshareDownloadedData/zh_convertible_bond_code.pickle', ZH_CONVERTIBLE_BOND_CODE),
	"open_fund_daily_data": ('fund_open_fund_daily_em', '/AkshareDownloadedData/open_fund_daily_data.pickle', OPEN_FUND_DAILY_DATA),
	"bond_zh_us_rate": ('bond_zh_us_rate', '/AkshareDownloadedData/bond_zh_us_rate.pickle', BOND_ZH_US_RATE)
}


def GetRelativeDirectory():
	# 获取当前文件的绝对路径
	current_path = os.path.abspath(__file__)
	# 获取当前文件所在的目录
	current_directory = os.path.dirname(current_path)
	return current_directory


clearedThisTime = False
def ClearCacheData():
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


def ForceWriteConfigTxt(updateCallback = None):
	TIME_STAMP_FILE_PATH = GetRelativeDirectory() + "/AkshareDownloadedData/config.txt"
	# print(TIME_STAMP_FILE_PATH)
	timeStr = time.strftime("%Y-%m-%d", time.localtime())
	if os.path.exists(TIME_STAMP_FILE_PATH):
		content = None
		with open(TIME_STAMP_FILE_PATH) as cfgFile:
			content = json.load(cfgFile)
		if content and content["datetime"] != timeStr:
			if updateCallback:
				updateCallback()
			with open(TIME_STAMP_FILE_PATH, "w") as cfgFile:
				json.dump({"datetime": timeStr}, cfgFile, indent=4)
	else:
		if updateCallback:
			updateCallback()
		with open(TIME_STAMP_FILE_PATH, "w") as cfgFile:
			json.dump({"datetime": timeStr}, cfgFile, indent=4)


def CacheAllAKShareData():
	ForceWriteConfigTxt()
	for key, (funcName, filePath, cacheData) in AKShareDataMap.items():
		print("Caching AKShare Data for %s" % key)
		try:
			cacheData = getattr(ak, funcName)()
			cacheData.to_pickle(GetRelativeDirectory() + filePath)
		except:
			print("Failed to get data for %s, please check your network" % key)
   

def GetAkShareData(getFileKey=None, force=False, kwargs={}):
	global FOREIGN_EXCHANGE_DATA, A_STOCK_DATA, HK_STOCK_DATA, ETF_DATA, LOF_DATA, US_STOCK_DATA, ZH_CONVERTIBLE_BOND_DATA, OPEN_FUND_DAILY_DATA, BOND_ZH_US_RATE
	global AKShareDataMap

	if force:
		ClearCacheData()

	ForceWriteConfigTxt(ClearCacheData)

	if getFileKey is not None:
		funcName, localFileName, globalVal = AKShareDataMap[getFileKey]
		localFilePath = GetRelativeDirectory() + localFileName
		if globalVal is not None:
			pass
		elif not os.path.exists(localFilePath):
			# print("gettting %s from ak.%s" % (getFileKey, funcName))
			globalVal = getattr(ak, funcName)(**kwargs)
			globalVal.to_pickle(localFilePath)
		else:
			# print("loading %s from %s" % (getFileKey, localFileName))
			globalVal = pd.read_pickle(localFilePath)
		return globalVal


def CallAKShareFuncWithCache(funcName, *args, **kwargs):
	localFileName = funcName
	for arg in args:
		localFileName += "_%s" % arg
	for k, arg in kwargs.items():
		localFileName += "_%s" % arg
	localFilePath = GetRelativeDirectory() + "/AkshareDownloadedData/%s.pickle" % localFileName
	if os.path.exists(localFilePath):
		ret = pd.read_pickle(localFilePath)
		print("read from cache %s" % localFileName)
		return ret
	else:
		ret = getattr(ak, funcName)(*args)
		ret.to_pickle(localFilePath)
		return ret

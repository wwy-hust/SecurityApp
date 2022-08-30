# -*- coding:utf-8 -*-
import akshare as ak
import pandas as pd
import numpy as np
import math
import os, sys
from utils import *

'''
【Supported Index】
沪深300	000300.SH
中证500	000905.SH
中证800	000906.SH
中证1000	000852.SH

上证50	000016.SH
中证红利	000922.CSI
中证医疗	399989.SZ
沪深300周期	000968.CSI

'''
def getAllIndexName():
	df = ak.index_value_name_funddb()


def getTenYearsChineseGovernmentBonds():
	df = ak.bond_zh_us_rate()
	df['日期']
	df['中国国债收益率10年']

def getInterestMargin(indexSymbol='中证800', indicator='市盈率'):
	indexStartTimeDf = ak.index_value_name_funddb()
	indexDf = ak.index_value_hist_funddb(symbol=indexSymbol, indicator=indicator)
	bondsDf = ak.bond_zh_us_rate()

	newDf = indexDf.set_index('日期').join(bondsDf.set_index('日期'))
	newDf = newDf.loc[:,['中国国债收益率10年', indicator]]
	# newDf.to_excel('bonds.xlsx')

	if indicator == '市盈率':
		interestMarginSerise = (100 / newDf[indicator]) - (newDf['中国国债收益率10年'])
		interestMarginSerise.name = '股债利差(市盈率倒数)'
	elif indicator == "股息率":
		interestMarginSerise = newDf[indicator] - newDf['中国国债收益率10年']
		interestMarginSerise.name = '股债利差(股息率)'

	maxMargin = interestMarginSerise.max()
	minMargin = interestMarginSerise.min()

	def calcPercent(margin):
		return (margin - minMargin) / (maxMargin - minMargin) * 100

	interestMarginPercentSerise = interestMarginSerise.apply(calcPercent)
	interestMarginPercentSerise.name = '股债利差百分位'

	outputDf = pd.DataFrame(interestMarginSerise).join(interestMarginPercentSerise)

	outputDf.to_excel("interestMargin/interestMargin_%s_%s.xlsx" % (indexSymbol, indicator))


getInterestMargin(indexSymbol='沪深300', indicator='市盈率')
getInterestMargin(indexSymbol='沪深300', indicator='股息率')
getInterestMargin(indexSymbol='中证500', indicator='市盈率')
getInterestMargin(indexSymbol='中证500', indicator='股息率')
getInterestMargin(indexSymbol='中证800', indicator='市盈率')
getInterestMargin(indexSymbol='中证800', indicator='股息率')

# -*- coding:utf-8 -*-
import akshare as ak
import pandas as pd
import numpy as np
import math
import os, sys
import openpyxl
import traceback

from utils import *
from stockInfo import StockInfoProxy
import stockInfo
stockInfo.__init_globals()


Stock = {
	'000876': 1000,
	'300192': 6400,
	'600025': 6000,
	'688300': 879,

	'00788': 42000,
	'01448': 2000,

	'512980': 16700,

	'SY': 200,

	'HKD': 46621,
	'CNY': 15433 + 1381,
}


def getStockCodeDictFromExcel(excelPath, selectCols):
	assert len(selectCols) == 2
	if os.path.exists(excelPath):
		sheet = pd.read_excel(excelPath)
		codeAndNum = sheet[selectCols]
		cols = (codeAndNum[t] for t in selectCols)
		return dict(zip(*cols))


def generatePositions(positionFilePath):
	global Stock
	retDict = getStockCodeDictFromExcel(positionFilePath, ['Code', 'Num'])
	if retDict:
		Stock = retDict

	ret = []
	for stock, num in Stock.items():
		stockInfo = StockInfoProxy(stock)
		# try:
		stockInfo.fetchCodeData()
		# except:
		# 	print("Error")
		print(stockInfo)
		ret.append((stockInfo.code, stockInfo.name, stockInfo.price, stockInfo.real_price, num, int(num * stockInfo.real_price)))

	sumVal = 0
	for entry in ret:
		sumVal += entry[5]

	percentList = []
	for entry in ret:
		percent = float('%.4f' % float(entry[5] / sumVal))
		percentList.append(percent)

	df = pd.DataFrame(ret, columns=['Code', 'Name', 'Price', 'RealPrice', 'Num', 'Value'])
	df['Percent'] = percentList
	df.sort_values(by='Value', ascending=False, inplace=True)
	print(df)
	# df.to_excel(positionFilePath, index=False)

	wb = openpyxl.load_workbook(positionFilePath)
	ws = wb.active
	for rowIdx, row in enumerate(df.iterrows(), 2):
		ws.cell(row=rowIdx, column=1).value = row[1]['Code']
		ws.cell(row=rowIdx, column=2).value = row[1]['Name']
		ws.cell(row=rowIdx, column=3).value = row[1]['Price']
		ws.cell(row=rowIdx, column=4).value = row[1]['RealPrice']
		ws.cell(row=rowIdx, column=5).value = row[1]['Num']
		ws.cell(row=rowIdx, column=6).value = '=%s*%s' % (ws.cell(row=rowIdx, column=4).coordinate, ws.cell(row=rowIdx, column=5).coordinate)
		ws.cell(row=rowIdx, column=7).value = '=%s/J1' % (ws.cell(row=rowIdx, column=6).coordinate)
	ws['J1'].value = '=SUM(F2:F%d)' % (rowIdx)
	wb.save(positionFilePath)


if __name__ == "__main__":
	generatePositions("position.xlsx")
	# outputFinancialInfo("valueTrack.xlsx")

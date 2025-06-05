from StockInfoLibrary.StockInfoClass import StockInfoProxy
from StockInfoLibrary.AkShareDataHelper import *
from StockInfoLibrary.TypeDefine import CodeType, TypeInPortfolio

from StockInfoLibrary.Config import G_DataSource, DataSourceType

G_DataSource = DataSourceType.AKSHARE

def test_AStockInfo():
	stockInfo = StockInfoProxy("a.600519")
	stockInfo.fetchCodeData()
	print(stockInfo)

	assert stockInfo.code == "600519"
	assert stockInfo.name == "贵州茅台"
	assert stockInfo.code_type == CodeType.A_STOCK
	assert stockInfo.typeInPorfolio == TypeInPortfolio.A

def test_HKStockInfo():
	stockInfo = StockInfoProxy("hk.00700")
	stockInfo.fetchCodeData()
	print(stockInfo)

	assert stockInfo.code == "00700"
	assert stockInfo.name == "腾讯控股"
	assert stockInfo.code_type == CodeType.HK_STOCK
	assert stockInfo.typeInPorfolio == TypeInPortfolio.HK

def test_USStockInfo():
	stockInfo = StockInfoProxy("us.AAPL")
	stockInfo.fetchCodeData()
	print(stockInfo)

	assert stockInfo.code == "AAPL"
	assert stockInfo.name == "苹果公司"
	assert stockInfo.code_type == CodeType.US_STOCK
	assert stockInfo.typeInPorfolio == TypeInPortfolio.US
	
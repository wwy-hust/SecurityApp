# -*- coding:utf-8 -*-

class StyleClassification(object):
	RobustDevidend = 1
	UnderEstimateRollback = 2
	Growth = 3
	Trade = 4
	Cash = 5
	Unknown = 6

G_RobustDevidend_StockSet = {
	"us.TLT", 
	"a.601985", # 中国核电
	"hk.01816", # 中广核电力
	"hk.00916", # 龙源电力H
	"a.600795", # 国电电力
	"a.600483", # 福能股份
	"a.600900", # 长江电力
	"a.600642", # 申能股份

	"sg.T14", # 达仁堂sg
	"a.600285", # 羚锐制药
	"a.000999", # 华润三九
	"a.600750", # 江中药业

	"hk.00883", # 中国海洋石油
	"hk.00010", # 恒隆集团
	"hk.01088", # 中国神华
}

G_UnderEstimateRollback_StockSet = {
	"hk.01093", # 石药集团
	"hk.00975", # 蒙古焦煤
	"hk.09988", # 阿里巴巴

	"a.300760", # 迈瑞医疗
	"a.300653", # 正海生物
	"etf.513120", # 港股创新药ETF
	
	"a.002129", # TCL中环
	
	"a.002597", # 金禾实业

	"a.002262", # 恩华药业
	"a.600161", # 天坛生物

	"a.600519", # 贵州茅台
	"a.600809", # 山西汾酒
	"a.000568", # 泸州老窖
	"a.002714", # 牧原股份
	"a.002244", # 滨江集团
}

G_Growth_StockSet = {
	"a.300811", # 铂科新材
	"a.300750", # 宁德时代
	"us.TSLA", # 特斯拉
	"hk.00700", # 腾讯控股
	"us.PDD", # 拼多多
	"hk.03690", # 美团
	"hk.01810", # 小米集团
	"hk.09961", # 携程集团
	"us.MSFT", # 微软
	"hk.01336", # 新华保险
	
	"a.301550", # 斯菱股份
	"a.601689", # 拓普集团
	"us.HSAI", # 禾赛
	"hk.09660", # 地平线机器人
	
	"a.603393", # 新天然气
	"us.INOD", 
	"hk.01347", # 华虹半导体
	"hk.00981", # 中芯国际

	"a.688721", # 龙图光罩
	"a.603160", # 汇顶科技
	"a.603986", # 兆易创新
	"a.688521", # 芯原股份
	"a.688008", # 澜起科技
	"a.688582", # 芯动联科
	"a.688608", # 恒玄科技
	"a.688018", # 乐鑫科技
	"a.688049", # 炬芯科技
	"us.AVGO", # 博通
	"us.NVDA", # 英伟达
	
	"a.688050", # 爱博医疗
	"a.300896", # 爱美客
	"a.688166", # 博瑞医药
	"us.LLY",
	"a.300181", # 佐力药业
	"hk.09606", # 映恩生物-B
	
	"a.600055", # 万东医疗
	
    "etf.513730", # 东南亚科技ETF
    "hk.02722", # 重庆机电

	"a.002155", # 湖南黄金
	"hk.03993", # 洛阳钼业
	"a.601899", # 紫金矿业
	"hk.02899", # 紫金矿业
	"hk.06693", # 赤峰黄金
	"hk.01818", # 招金矿业

	"a.300661", # 圣邦股份
}

G_Trade_StockSet = {
	"us.TMF", # 3倍做多20年期美国国债

	"a.603662", # 柯力传感
	"a.688017", # 绿的谐波
	"a.603728", # 鸣志电器
	"a.688322", # 奥比中光-UW
	"a.603009", # 北特科技
	
    "a.688270", # 臻镭科技
    "etf.159985", # 豆粕ETF
	"a.301269", # 华大九天
	"us.SQQQ", # 三倍做空纳指
	"us.YANG", # 三倍做空KWEB
	"us.VIXY", # 恐慌指数
	"us.TQQQ", # 三倍做多纳指
	"us.SOXS", # 三倍做空半导体
	"us.SPXS", # 三倍做空标普500
	"us.SDOW", # 三倍做空道指
	"us.PSQ",  # 一倍做空纳指 

    "a.301236", # 软通动力
    "a.301596", # 瑞迪智驱
    "a.002518", # 科士达
    "a.300748", # 金力永磁
    
    "a.603993", # 洛阳钼业
    "a.300474", # 景嘉微
    "hk.00728", # 中国电信

    "a.603496", # 恒为科技
    "a.002843", # 泰嘉股份
    "a.002600", # 领益智造
    "a.002851", # 麦格米特

    "a.300604", # 长川科技
    "a.600301", # 华锡有色
    "a.002460", # 赣锋锂业
    "hk.02362", # 金川国际
    "a.000651", # 格力电器
    "a.000582", # 北部湾港
    
    "us.TSM", # 台湾积体电路制造公司
    "us.INTC", # 英特尔公司
    "a.002436", # 兴森科技
    "a.000932", # 华菱钢铁
    "us.RNMBY", # 莱茵金属
    "a.000657", # 中钨高新

    "a.600123", # 兰花科创
	"us.HOOD", # Robinhood
	"us.META", # Meta
	"hk.07500", # 南方两倍做空恒指
	"hk.07552", # 南方两倍做空恒科
	"etf.159562", # 黄金股ETF
}

G_Currency_Set = {
	"cash.CNY",
	"cash.HKD",
	"cash.USD",
}

def StyleClassToString(styleClass):
	if styleClass == StyleClassification.RobustDevidend:
		return "Robust Devidend"
	elif styleClass == StyleClassification.UnderEstimateRollback:
		return "UnderEstimate Rollback"
	elif styleClass == StyleClassification.Growth:
		return "Growth"
	elif styleClass == StyleClassification.Trade:
		return "Trade"
	elif styleClass == StyleClassification.Cash:
		return "Cash"
	return "Unknown"

def GetStyleClassification(originCode):
	global G_RobustDevidend_StockSet, G_UnderEstimateRollback_StockSet, G_Growth_StockSet, G_Trade_StockSet
	if originCode in G_RobustDevidend_StockSet:
		return StyleClassification.RobustDevidend
	elif originCode in G_UnderEstimateRollback_StockSet:
		return StyleClassification.UnderEstimateRollback
	elif originCode in G_Growth_StockSet:
		return StyleClassification.Growth
	elif originCode in G_Trade_StockSet:
		return StyleClassification.Trade
	elif originCode in G_Currency_Set:
		return StyleClassification.Cash
	return StyleClassification.Unknown


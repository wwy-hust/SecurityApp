# -*- coding:utf-8 -*-

STOCK_TO_INDUSTRY_MAP = {
    "us.TLT": "债券",
    "us.TMF": "债券",

    "hk.00010": "地产", # 恒隆集团
    "a.002244": "地产", # 滨江集团

    "hk.00975": "矿业", # 蒙古焦煤
    "hk.00883": "矿业", # 中国海洋石油
    "a.603393": "矿业", # 新天然气
    "a.603993": "矿业", # 洛阳钼业
    "a.600301": "矿业", # 华锡有色
    "a.002460": "矿业", # 赣锋锂业
    "hk.02362": "矿业", # 金川国际
    "a.601899": "矿业", # 紫金矿业
    "hk.02899": "矿业", # 紫金矿业
    "a.000657": "矿业", # 中钨高新
    "a.600123": "矿业", # 兰花科创
    "a.002155": "矿业", # 湖南黄金
    "hk.03993": "矿业", # 洛阳钼业
    "hk.06693": "矿业", # 赤峰黄金
    "hk.01818": "矿业", # 招金矿业
    "hk.01088": "矿业", # 中国神华
    "etf.159562": "矿业", # 黄金股ETF
    
    "hk.01336": "金融", # 新华保险

    "a.601985": "公用事业", # 中国核电
    "a.600795": "公用事业", # 国电电力
    "hk.00916": "公用事业", # 龙源电力H
    "a.600642": "公用事业", # 申能股份
    "a.600900": "公用事业", # 长江电力
    "hk.01816": "公用事业", # 中广核电力
    "a.000582": "公用事业", # 北部湾港
    
    "etf.513120": "医疗", # 港股创新药ETF
    "hk.01093": "医疗", # 石药集团
    "a.002262": "医疗", # 恩华药业
    "a.300760": "医疗", # 迈瑞医疗
    "a.300653": "医疗", # 正海生物
    "hk.09606": "医疗", # 映恩生物-B

    "a.300181": "医疗", # 佐力药业
    "a.000999": "医疗", # 华润三九
    "a.600750": "医疗", # 江中药业
    "a.600285": "医疗", # 羚锐制药
    "sg.T14": "医疗", # 达仁堂sg
    "a.600161": "医疗", # 天坛生物
    "a.600055": "医疗", # 万东医疗
    "a.688050": "医疗", # 爱博医疗
    "a.300896": "医疗", # 爱美客
    "a.688166": "医疗", # 博瑞医药
    "us.LLY": "医疗", # 礼来

    "hk.09988": "互联网", # 阿里巴巴
    "hk.00700": "互联网", # 腾讯控股
    "us.PDD": "互联网", # 拼多多
    "hk.03690": "互联网", # 美团
    "hk.01810": "互联网", # 小米集团
    "hk.09961": "互联网", # 携程集团
    "us.MSFT": "互联网", # 微软
    "us.META": "互联网", # Meta Platforms
    "us.HOOD": "互联网", # Robinhood

    "a.002129": "新能源", # TCL中环
    "a.300750": "新能源", # 宁德时代
    "us.TSLA": "新能源", # 特斯拉

    "a.002597": "化工", # 金禾实业

    "a.300811": "新材料", # 铂科新材
    
    "a.301550": "机器人", # 斯菱股份
    "a.601689": "机器人", # 拓普集团
    "us.HSAI": "机器人", # 禾赛
    "a.603728": "机器人", # 鸣志电器
    "a.688322": "机器人", # 奥比中光-UW
    "a.603009": "机器人", # 北特科技
    "a.603662": "机器人", # 柯力传感
    "a.301596": "机器人", # 瑞迪智驱
    "a.300748": "机器人", # 金力永磁
    "a.002600": "机器人", # 领益智造

    "us.INOD": "AI", # INOD
    "a.301236": "AI", # 软通动力
    "a.002518": "AI", # 科士达
    "a.300474": "AI", # 景嘉微
    "hk.00728": "AI", # 中国电信
    "a.603496": "AI", # 恒为科技
    "a.002851": "AI", # 麦格米特
    "a.002843": "AI", # 泰嘉股份
    "hk.02722": "AI", # 重庆机电

    "hk.01347": "半导体", # 华虹半导体
    "hk.00981": "半导体", # 中芯国际
    "a.688721": "半导体", # 龙图光罩
    "a.603160": "半导体", # 汇顶科技
    "a.603986": "半导体", # 兆易创新
    "a.688521": "半导体", # 芯原股份
    "a.688008": "半导体", # 澜起科技
    "a.688582": "半导体", # 芯动联科
    "a.688608": "半导体", # 恒玄科技
    "a.688018": "半导体", # 乐鑫科技
    "a.688049": "半导体", # 炬芯科技
    "us.AVGO": "半导体", # 博通
    "us.NVDA": "半导体", # 英伟达
    "a.301269": "半导体", # 华大九天
    "a.300604": "半导体", # 长川科技
    "us.TSM": "半导体", # 台湾积体电路制造公司
    "us.INTC": "半导体", # 英特尔公司
    "a.002436": "半导体", # 兴森科技
    "a.300661": "半导体", # 圣邦股份
    "hk.09660": "半导体", # 地平线机器人
    
    "etf.513730": "ETF", # 东南亚科技ETF
    "etf.159985": "ETF", # 豆粕ETF
    "us.SQQQ": "ETF", # SQQQ
    "us.YANG": "ETF", # 三倍做空KWEB
    "us.TQQQ": "ETF", # TQQQ
    "hk.07500": "ETF", # 南方两倍做空恒指
    "hk.07552": "ETF", # 南方两倍做空恒科
    "us.SOXS": "ETF", # 三倍做空半导体
    "us.SPXS": "ETF", # 三倍做空标普500
    "us.PSQ": "ETF", # 一倍做空纳指 
    "us.SDOW": "ETF", # 三倍做空道指
    
    "a.688270": "军工", # 臻镭科技
    "us.RNMBY": "军工", # 莱茵金属

    "cash.CNY": "现金", # 人民币
    "cash.USD": "现金", # 美元
    "cash.HKD": "现金", # 港币
    "cash.EUR": "现金", # 欧元
    "cash.GBP": "现金", # 英镑
    "cash.JPY": "现金", # 日元
    "cash.CHF": "现金", # 瑞士法郎
    "cash.CAD": "现金", # 加拿大元

    "a.000932": "钢铁", # 华菱钢铁

    "a.000651": "消费", # 格力电器
    "a.002714": "消费", # 牧原股份
    "a.600519": "消费", # 贵州茅台
    "a.000568": "消费", # 泸州老窖
    "a.600809": "消费", # 山西汾酒
}

def GetIndustryClassification(originCode):
    return STOCK_TO_INDUSTRY_MAP.get(originCode, "UNKNOWN")

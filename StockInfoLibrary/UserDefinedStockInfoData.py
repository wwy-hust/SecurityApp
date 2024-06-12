# -*- coding:utf-8 -*-
# 这里存放用户自定义的数据

# 数据获取的来源&优先级排序：下面XXX是某一类型，例如A股，HK股。
# 优先级从高到低
# 1. MANUAL_XXX_INFO
# 2. data from akshare
# 3. DEFAULT_XXX_INFO


############# Currency Exchange Rate #############
# 默认汇率，如果获取不到汇率会取这里的数据
DEFAULT_CASH_EXCHANGE_RATE = {
    "HKD:CNY": 0.854,
    "USD:CNY": 7.25,
}

MANUAL_CASH_EXCHANGE_RATE = {}
##################################################


###################### ETF #######################
DEFAULT_ETF_INFO = {
    "511090": {
        "name": "30年国债ETF",
    },
    "164824": {
        "name": "印度基金",
    },
}

MANUAL_ETF_INFO = {
    "511090": {
        "price": 111.9,
    },
    "164824": {
        "price": 1.53,
    },
}
##################################################


#################### A Stock #####################
DEFAULT_A_INFO = {}
MANUAL_A_INFO = {}
##################################################


#################### HK Stock ####################
DEFAULT_HK_INFO = {}
MANUAL_HK_INFO = {}
##################################################


#################### US Stock ####################
DEFAULT_US_INFO = {
    "TMF": {
        "name": "3倍做多20年期美国国债"
    },
    "VKTX": {
        "name": "Viking Therapeutics"
    },
    "VIXY": {
        "name": "波动率指数"
    }
}
MANUAL_US_INFO = {
    "TMF": {
        "price": 49,
    },
    "VKTX": {
        "price": 57,
    },
    "VIXY": {
        "price": 11.44,
    }
}
##################################################


#################### SG Stock ####################
DEFAULT_SG_INFO = {
    "T14": {
		"name": "达仁堂SG",
	}
}
MANUAL_SG_INFO = {
    "T14": {
		"price": 2.6,
	}
}
##################################################


############## ZH Convertible Bond ###############
DEFAULT_ZHCVB_INFO = {}
MANUAL_ZHCVB_INFO = {}
##################################################

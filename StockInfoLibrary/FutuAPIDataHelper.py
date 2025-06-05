import futu as ft
from futu import SubType, KLType, AuType
from .Config import G_Futu_Address, G_Futu_Port

gQuoteContext = None

def InitQuoteContext():
    global gQuoteContext
    if gQuoteContext is None:
        gQuoteContext = ft.OpenQuoteContext(host=G_Futu_Address, port=G_Futu_Port)
        gQuoteContext.start()
        gQuoteContext.set_handler(ft.TickerHandlerBase())

def CloseQuoteContext():
    global gQuoteContext
    if gQuoteContext is not None:
        gQuoteContext.close()
        gQuoteContext = None

def FutuApi_HK_GetStockInfoData(code):
    global gQuoteContext
    if gQuoteContext is None:
        InitQuoteContext()
    realCode = 'HK.' + code
    retData = {}
    ok, data = gQuoteContext.get_market_snapshot([realCode])
    if ok == 0:
        retData['name'] = data.name.values[0]
        retData['price'] = data.last_price.values[0]
        retData['market_value'] = round(data.total_market_val.values[0] / 100000000, 2)
        retData['pe_ttm'] = data.pe_ttm_ratio.values[0]
        retData['profit'] = round(data.net_profit.values[0] / 100000000, 2)
        retData['dividend_ratio_ttm'] = data.dividend_lfy_ratio.values[0]

        ret_sub, err_message = gQuoteContext.subscribe([realCode, 'HK.800000'], [SubType.K_WEEK], subscribe_push=False)
        ret, data = gQuoteContext.get_cur_kline(realCode, 8, KLType.K_WEEK, AuType.QFQ)
        baseret, base = gQuoteContext.get_cur_kline('HK.800000', 8, KLType.K_WEEK, AuType.QFQ)
        if ret == 0 and baseret == 0:
            stockHigh = max(data['high'])
            stockLow = min(data['low'])
            baseHigh = max(base['high'])
            baseLow = min(base['low'])
            retData['volatility'] = round(((stockHigh - stockLow) / stockLow) / ((baseHigh - baseLow) / baseLow), 2)
        return retData
    else:
        return {}

def FutuApi_A_GetStockInfoData(code):
    global gQuoteContext
    if gQuoteContext is None:
        InitQuoteContext()
    realCode = code
    if code[0] == '6':
        realCode = 'SH.' + code
    elif code[0] == '3' or code[0] == '0':
        realCode = 'SZ.' + code
    retData = {}
    ok, data = gQuoteContext.get_market_snapshot([realCode])
    if ok == 0:
        retData['name'] = data.name.values[0]
        retData['price'] = data.last_price.values[0]
        retData['market_value'] = round(data.total_market_val.values[0] / 100000000, 2)
        retData['pe_ttm'] = data.pe_ttm_ratio.values[0]
        retData['profit'] = round(data.net_profit.values[0] / 100000000, 2)
        retData['dividend_ratio_ttm'] = data.dividend_ratio_ttm.values[0]

        ret_sub, err_message = gQuoteContext.subscribe([realCode, 'SH.000300'], [SubType.K_WEEK], subscribe_push=False)
        ret, data = gQuoteContext.get_cur_kline(realCode, 8, KLType.K_WEEK, AuType.QFQ)
        baseret, base = gQuoteContext.get_cur_kline('SH.000300', 8, KLType.K_WEEK, AuType.QFQ)
        if ret == 0 and baseret == 0:
            stockHigh = max(data['high'])
            stockLow = min(data['low'])
            baseHigh = max(base['high'])
            baseLow = min(base['low'])
            retData['volatility'] = round(((stockHigh - stockLow) / stockLow) / ((baseHigh - baseLow) / baseLow), 2)
        return retData
    else:
        print(ok, data)
        return {}

def FutuApi_A_GetStockInfoData_Batch(codes):
    global gQuoteContext
    if gQuoteContext is None:
        InitQuoteContext()
    # print(codes)
    realCodes = {}
    for idx, code in enumerate(codes):
        if codes[idx][0] == '6':
            realCodes[code] = 'SH.' + code
        elif codes[idx][0] == '3' or codes[0] == '0':
            realCodes[code] = 'SZ.' + code
    retDatas = {}
    # print(realCodes, realCodes.values(), list(realCodes.values()))
    ok, datas = gQuoteContext.get_market_snapshot(list(realCodes.values()))
    # print(ok)
    if ok == 0:
        ret_sub, err_message = gQuoteContext.subscribe(list(realCodes.values()) + ['SH.000300'], [SubType.K_WEEK], subscribe_push=False)
        baseret, base = gQuoteContext.get_cur_kline('SH.000300', 8, KLType.K_WEEK, AuType.QFQ)
        lenData = len(datas)
        i = 0
        while i < lenData:
            # print(datas.loc[i])
            retData = {}
            localData = dict(datas.loc[i])
            code = localData['code'].split('.')[1]
            retData['name'] = localData['name']
            retData['price'] = localData['last_price']
            retData['market_value'] = round(localData['total_market_val'] / 100000000, 2)
            retData['pe_ttm'] = localData['pe_ttm_ratio']
            retData['profit'] = round(localData['net_profit'] / 100000000, 2)
            retData['dividend_ratio_ttm'] = localData['dividend_ratio_ttm']

            ret, data = gQuoteContext.get_cur_kline(localData['code'], 8, KLType.K_WEEK, AuType.QFQ)
            if ret == 0 and baseret == 0:
                stockHigh = max(data['high'])
                stockLow = min(data['low'])
                baseHigh = max(base['high'])
                baseLow = min(base['low'])
                retData['volatility'] = round(((stockHigh - stockLow) / stockLow) / ((baseHigh - baseLow) / baseLow), 2)

            retDatas[code] = retData
            i += 1
        return retDatas
    else:
        print(ok, datas)
        return {}

def FutuApi_HK_GetStockInfoData_Batch(codes):
    global gQuoteContext
    if gQuoteContext is None:
        InitQuoteContext()
    realCodes = {}
    for idx, code in enumerate(codes):
        realCodes[idx] = 'HK.' + code
    retDatas = {}
    # print(realCodes, realCodes.values(), list(realCodes.values()))
    ok, datas = gQuoteContext.get_market_snapshot(list(realCodes.values()))
    # print(ok)
    if ok == 0:
        ret_sub, err_message = gQuoteContext.subscribe(list(realCodes.values()) + ['HK.800000'], [SubType.K_WEEK], subscribe_push=False)
        baseret, base = gQuoteContext.get_cur_kline('HK.800000', 8, KLType.K_WEEK, AuType.QFQ)
        lenData = len(datas)
        i = 0
        while i < lenData:
            # print(datas.loc[i])
            retData = {}
            localData = dict(datas.loc[i])
            code = localData['code'].split('.')[1]
            retData['name'] = localData['name']
            retData['price'] = localData['last_price']
            retData['market_value'] = round(localData['total_market_val'] / 100000000, 2)
            retData['pe_ttm'] = localData['pe_ttm_ratio']
            retData['profit'] = round(localData['net_profit'] / 100000000, 2)
            retData['dividend_ratio_ttm'] = localData['dividend_ratio_ttm']

            ret, data = gQuoteContext.get_cur_kline(localData['code'], 8, KLType.K_WEEK, AuType.QFQ)
            if ret == 0 and baseret == 0:
                stockHigh = max(data['high'])
                stockLow = min(data['low'])
                baseHigh = max(base['high'])
                baseLow = min(base['low'])
                retData['volatility'] = round(((stockHigh - stockLow) / stockLow) / ((baseHigh - baseLow) / baseLow), 2)

            retDatas[code] = retData
            i += 1
        return retDatas
    else:
        print(ok, datas)
        return {}

def FutuApi_US_GetStockInfoData_Batch(codes):
    global gQuoteContext
    if gQuoteContext is None:
        InitQuoteContext()
    realCodes = {}
    for idx, code in enumerate(codes):
        realCodes[idx] = 'US.' + code
    retDatas = {}
    # print(realCodes, realCodes.values(), list(realCodes.values()))
    ok, datas = gQuoteContext.get_market_snapshot(list(realCodes.values()))
    # print(ok)
    if ok == 0:
        lenData = len(datas)
        i = 0
        while i < lenData:
            # print(datas.loc[i])
            retData = {}
            localData = dict(datas.loc[i])
            code = localData['code'].split('.')[1]
            retData['name'] = localData['name']
            retData['price'] = localData['last_price']
            retData['market_value'] = round(localData['total_market_val'] / 100000000, 2)
            retData['pe_ttm'] = localData['pe_ttm_ratio']
            retData['profit'] = round(localData['net_profit'] / 100000000, 2)
            retData['dividend_ratio_ttm'] = localData['dividend_ratio_ttm']
            retDatas[code] = retData
            i += 1
        return retDatas
    else:
        print(ok, datas)
        return {}


def FutuApi_US_GetStockInfoData(code):
    global gQuoteContext
    if gQuoteContext is None:
        InitQuoteContext()
    realCode = 'US.' + code
    retData = {}
    ok, data = gQuoteContext.get_market_snapshot([realCode])
    if ok == 0:
        retData['name'] = data.name.values[0]
        retData['price'] = data.last_price.values[0]
        retData['market_value'] = round(data.total_market_val.values[0] / 100000000, 2)
        retData['pe_ttm'] = data.pe_ttm_ratio.values[0]
        retData['profit'] = round(data.net_profit.values[0] / 100000000, 2)
        retData['dividend_ratio_ttm'] = data.dividend_ratio_ttm.values[0]
        return retData
    else:
        return {}

def FutuApi_ETF_GetStockInfoData(code):
    global gQuoteContext
    if gQuoteContext is None:
        InitQuoteContext()
    realCode = code
    if code[0] == '5':
        realCode = 'SH.' + code
    elif code[0] == '1':
        realCode = 'SZ.' + code
    retData = {}
    ok, data = gQuoteContext.get_market_snapshot([realCode])

    if ok == 0:
        retData['name'] = data.name.values[0]
        retData['price'] = data.last_price.values[0]

        ret_sub, err_message = gQuoteContext.subscribe([realCode, 'SH.000300'], [SubType.K_WEEK], subscribe_push=False)
        baseret, base = gQuoteContext.get_cur_kline('SH.000300', 8, KLType.K_WEEK, AuType.QFQ)
        ret, data = gQuoteContext.get_cur_kline(realCode, 8, KLType.K_WEEK, AuType.QFQ)

        if ret == 0 and baseret == 0:
            stockHigh = max(data['high'])
            stockLow = min(data['low'])
            baseHigh = max(base['high'])
            baseLow = min(base['low'])
            retData['volatility'] = round(((stockHigh - stockLow) / stockLow) / ((baseHigh - baseLow) / baseLow), 2)

        return retData
    else:
        return {}

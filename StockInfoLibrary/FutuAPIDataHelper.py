import futu as ft

gQuoteContext = None

def InitQuoteContext():
    global gQuoteContext
    if gQuoteContext is None:
        gQuoteContext = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
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
        retData['dividend_ratio_ttm'] = data.dividend_ratio_ttm.values[0]
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
        return retData
    else:
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
        return retData
    else:
        return {}

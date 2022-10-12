# -*- coding:utf-8 -*-
import akshare as ak
from itsdangerous import TimedJSONWebSignatureSerializer
import pandas as pd
import numpy as np
import math
import os, sys, copy
import traceback
import time

from utils import *
from stockInfo import StockInfoProxy
import stockInfo
stockInfo.__init_globals()

import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Format, Scheme, Trim, Prefix, Symbol, Group
from dash.dash_table import FormatTemplate

FORMATOR_MONEY = Format(precision=0, group=Group.yes, scheme=Scheme.fixed).symbol(Symbol.yes).symbol_prefix('¥')
FORMATOR_PERCENT = FormatTemplate.percentage(2)

REPORT_YEAR_FROM = 2019
REPORT_CURRENT_YEAR = 2022
REPORT_YEAR_TO = 2025

CONFIG_FILENAME = "market_value_config.json"
MARKET_VALUE_CONFIG_DICT = {}
LOCAL_STOCK_DICT = {}


def generateHtml():
    global MARKET_VALUE_CONFIG_DICT
    with open(CONFIG_FILENAME, "r") as f:
        MARKET_VALUE_CONFIG_DICT = json.load(f)
    for group, groupInfo in MARKET_VALUE_CONFIG_DICT.items():
        for stockCode, stockConfig in groupInfo.items():
            LOCAL_STOCK_DICT[stockCode] = StockInfoProxy(stockCode)
            LOCAL_STOCK_DICT[stockCode].fetchCodeData(True)


app = dash.Dash()
TABLE_TITLE_KEYS = ('年份', '预估净利润', '预估增长率(%)', 'Q1净利润', 'Q1单季同比(%)', 'Q2净利润', 'Q2单季同比(%)', 'Q3净利润', 'Q3单季同比(%)', 'Q4净利润', 'Q4单季同比(%)', '年度净利润', '低估市值', '合理市值', '高估市值')
DATATABLE_TITLE = (
    {'id': '年份', 'name': '年份'}, 
    {'id': '预估净利润', 'name': '预估净利润', 'type': 'numeric', 'format': FORMATOR_MONEY},
    {'id': '预估增长率(%)', 'name': '预估增长率(%)', 'type': 'numeric', 'format': FORMATOR_PERCENT}, 
    {'id': 'Q1净利润', 'name': 'Q1净利润', 'type': 'numeric', 'format': FORMATOR_MONEY},
    {'id': 'Q1单季同比(%)', 'name': 'Q1单季同比(%)', 'type': 'numeric', 'format': FORMATOR_PERCENT},
    {'id': 'Q2净利润', 'name': 'Q2净利润', 'type': 'numeric', 'format': FORMATOR_MONEY},
    {'id': 'Q2单季同比(%)', 'name': 'Q2单季同比(%)', 'type': 'numeric', 'format': FORMATOR_PERCENT},
    {'id': 'Q3净利润', 'name': 'Q3净利润', 'type': 'numeric', 'format': FORMATOR_MONEY},
    {'id': 'Q3单季同比(%)', 'name': 'Q3单季同比(%)', 'type': 'numeric', 'format': FORMATOR_PERCENT},
    {'id': 'Q4净利润', 'name': 'Q4净利润', 'type': 'numeric', 'format': FORMATOR_MONEY},
    {'id': 'Q4单季同比(%)', 'name': 'Q4单季同比(%)', 'type': 'numeric', 'format': FORMATOR_PERCENT},
    {'id': '年度净利润', 'name': '年度净利润', 'type': 'numeric', 'format': FORMATOR_MONEY},
    {'id': '低估市值', 'name': '低估市值', 'type': 'numeric', 'format': FORMATOR_MONEY},
    {'id': '合理市值', 'name': '合理市值', 'type': 'numeric', 'format': FORMATOR_MONEY},
    {'id': '高估市值', 'name': '高估市值', 'type': 'numeric', 'format': FORMATOR_MONEY}
)

STYLE_TD = {'border-style': 'dashed', 'border-width': 'thin'}


def createTable(group, stockcode, pe_low, pe_medium, pe_high):
    stockConfig = MARKET_VALUE_CONFIG_DICT[group][stockcode]
    tbl = html.Table(
        [html.Thead(
            html.Tr([html.Th(col) for col in TABLE_TITLE_KEYS])
        ),
        html.Tbody([
            html.Tr([
                html.Td(report_date, style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),
                html.Td("", style=STYLE_TD),

                html.Td("", style=STYLE_TD, id="%s_%d_low_marketValue" % (stockcode, report_date)),
                html.Td("", style=STYLE_TD, id="%s_%d_medium_marketValue" % (stockcode, report_date)),
                html.Td("", style=STYLE_TD, id="%s_%d_high_marketValue" % (stockcode, report_date)),
            ]) for report_date in range(REPORT_YEAR_FROM, REPORT_YEAR_TO)
        ])
        ],
        style={'border-style': 'groove', 'border-width': 'medium'}
    )

    profit_s1, profit_s2, profit_s3, profit_s4 = 0, 0, 0, 0
    yoy_s1, yoy_s2, yoy_s3, yoy_s4 = 0, 0, 0, 0
    yearProfit, yearProfit_yoy = 0, 0
    for idx, year in enumerate(range(REPORT_YEAR_FROM, REPORT_YEAR_TO)):
        tbl.children[1].children[idx].children[0] = html.Td(year, style=STYLE_TD)

        reportDates = reportDateList(year)

        row_s1 = LOCAL_STOCK_DICT[stockcode].profit.loc[lambda df:df['REPORT_DATE'] =='%s 00:00:00' % reportDates[0],:]
        row_s2 = LOCAL_STOCK_DICT[stockcode].profit.loc[lambda df:df['REPORT_DATE'] =='%s 00:00:00' % reportDates[1],:]
        row_s3 = LOCAL_STOCK_DICT[stockcode].profit.loc[lambda df:df['REPORT_DATE'] =='%s 00:00:00' % reportDates[2],:]
        row_s4 = LOCAL_STOCK_DICT[stockcode].profit.loc[lambda df:df['REPORT_DATE'] =='%s 00:00:00' % reportDates[3],:]

        allvalid = all((len(row_s1), len(row_s2), len(row_s3), len(row_s4)))

        if len(row_s1):
            if profit_s1:
                yoy_s1 = (row_s1['NETPROFIT'].values[0] / profit_s1) - 1 
            profit_s1 = row_s1['NETPROFIT'].values[0]
            tbl.children[1].children[idx].children[3] = html.Td(formatToString_profit(row_s1['NETPROFIT'].values[0]), style=STYLE_TD)
            tbl.children[1].children[idx].children[4] = html.Td(formatToString_yoy(yoy_s1) if yoy_s1 else "", style=STYLE_TD)
        if len(row_s2):
            if profit_s2:
                yoy_s2 = (row_s2['NETPROFIT'].values[0] / profit_s2) - 1
            profit_s2 = row_s2['NETPROFIT'].values[0]
            tbl.children[1].children[idx].children[5] = html.Td(formatToString_profit(row_s2['NETPROFIT'].values[0]), style=STYLE_TD)
            tbl.children[1].children[idx].children[6] = html.Td(formatToString_yoy(yoy_s2) if yoy_s2 else "", style=STYLE_TD)
        if len(row_s3):
            if profit_s3:
                yoy_s3 = (row_s3['NETPROFIT'].values[0] / profit_s3) - 1
            profit_s3 = row_s3['NETPROFIT'].values[0]
            tbl.children[1].children[idx].children[7] = html.Td(formatToString_profit(row_s3['NETPROFIT'].values[0]), style=STYLE_TD)
            tbl.children[1].children[idx].children[8] = html.Td(formatToString_yoy(yoy_s3) if yoy_s3 else "", style=STYLE_TD)
        if len(row_s4):
            if profit_s4:
                yoy_s4 = (row_s4['NETPROFIT'].values[0] / profit_s4) - 1
            profit_s4 = row_s4['NETPROFIT'].values[0]
            tbl.children[1].children[idx].children[9] = html.Td(formatToString_profit(row_s4['NETPROFIT'].values[0]), style=STYLE_TD)
            tbl.children[1].children[idx].children[10] = html.Td(formatToString_yoy(yoy_s4) if yoy_s4 else "", style=STYLE_TD)

        if allvalid:
            if yearProfit:
                yearProfit_yoy = (sum((profit_s1, profit_s2, profit_s3, profit_s4)) / yearProfit) - 1
            yearProfit = row_s1['NETPROFIT'].values[0] + row_s2['NETPROFIT'].values[0] + row_s3['NETPROFIT'].values[0] + row_s4['NETPROFIT'].values[0]
            tbl.children[1].children[idx].children[1] = html.Td(formatToString_profit(yearProfit), style=STYLE_TD)
            tbl.children[1].children[idx].children[2] = html.Td(formatToString_yoy(yearProfit_yoy) if yearProfit_yoy else "", style=STYLE_TD)
        else:
            profitName, profitYoyName = "%d_profit_e" % year, "%d_profit_yoy" % year
            if profitName in stockConfig or profitYoyName in stockConfig:
                if profitName in stockConfig and profitYoyName not in stockConfig:
                    profit = stockConfig[profitName] * 100000000
                    profitYoy = (profit / yearProfit) - 1
                else:
                    profitYoy = float(stockConfig[profitYoyName]) / 100
                    profit = yearProfit * (1 + profitYoy)
                stockConfig[profitName] = profit
                stockConfig[profitYoyName] = profitYoy
                tbl.children[1].children[idx].children[1] = html.Td(formatToString_profit(profit), id="%s_%s_%d_profit_input" % (group, stockcode, year), style=STYLE_TD)
                tbl.children[1].children[idx].children[2] = html.Td(formatToString_yoy(profitYoy), style=STYLE_TD)

                # tbl.children[1].children[idx].children[1] = html.Td(dcc.Input(value=profit, type='number'), id="%s_%s_%d_profit_input" % (group, stockcode, year), style=STYLE_TD)
                # tbl.children[1].children[idx].children[2] = html.Td(dcc.Input(value=profitYoy, type='number'), style=STYLE_TD)
            else:
                profit = yearProfit
                profitYoy = 0
                stockConfig[profitName] = profit
                stockConfig[profitYoyName] = profitYoy
                tbl.children[1].children[idx].children[1] = html.Td(dcc.Input(value=yearProfit, type='number'), style=STYLE_TD)
                tbl.children[1].children[idx].children[2] = html.Td(dcc.Input(value='0', type='number'), style=STYLE_TD)
            yearProfit = profit

        if allvalid:
            tbl.children[1].children[idx].children[11] = html.Td(formatToString_profit(yearProfit), style=STYLE_TD)

        if yearProfit:
            marketValue_low = pe_low * yearProfit
            marketValue_medium = pe_medium * yearProfit
            marketValue_high = pe_high * yearProfit
            tbl.children[1].children[idx].children[12] = html.Td(formatToString_profit(marketValue_low), style=STYLE_TD)
            tbl.children[1].children[idx].children[13] = html.Td(formatToString_profit(marketValue_medium), style=STYLE_TD)
            tbl.children[1].children[idx].children[14] = html.Td(formatToString_profit(marketValue_high), style=STYLE_TD)

    @app.callback(
        Output("%s_%s_%d_profit_input" % (group, stockcode, year), "children"),
        Input("%s_%s_%d_profit_input" % (group, stockcode, year), "value")
    )
    def clicked(v):
        print("asdasd")
    return tbl



def createDataTable(group, stockcode, pe_low, pe_medium, pe_high):
    stockConfig = MARKET_VALUE_CONFIG_DICT[group][stockcode]

    profit_s1, profit_s2, profit_s3, profit_s4 = 0, 0, 0, 0
    yoy_s1, yoy_s2, yoy_s3, yoy_s4 = 0, 0, 0, 0
    yearProfit, yearProfit_yoy = 0, 0

    dataList = []
    for idx, year in enumerate(range(REPORT_YEAR_FROM, REPORT_YEAR_TO)):
        dataDict = {'年份': year}
        reportDates = reportDateList(year)

        row_s1 = LOCAL_STOCK_DICT[stockcode].profit.loc[lambda df:df['REPORT_DATE'] =='%s 00:00:00' % reportDates[0],:]
        row_s2 = LOCAL_STOCK_DICT[stockcode].profit.loc[lambda df:df['REPORT_DATE'] =='%s 00:00:00' % reportDates[1],:]
        row_s3 = LOCAL_STOCK_DICT[stockcode].profit.loc[lambda df:df['REPORT_DATE'] =='%s 00:00:00' % reportDates[2],:]
        row_s4 = LOCAL_STOCK_DICT[stockcode].profit.loc[lambda df:df['REPORT_DATE'] =='%s 00:00:00' % reportDates[3],:]
        allvalid = all((len(row_s1), len(row_s2), len(row_s3), len(row_s4)))

        if len(row_s1):
            yoy_s1 = ((row_s1['NETPROFIT'].values[0] / profit_s1) - 1) if profit_s1 else 0
            profit_s1 = row_s1['NETPROFIT'].values[0]
        else:
            profit_s1 = 0
            yoy_s1 = 0
        if len(row_s2):
            yoy_s2 = ((row_s2['NETPROFIT'].values[0] / profit_s2) - 1) if profit_s2 else 0
            profit_s2 = row_s2['NETPROFIT'].values[0]
        else:
            profit_s2 = 0
            yoy_s2 = 0
        if len(row_s3):
            yoy_s3 = ((row_s3['NETPROFIT'].values[0] / profit_s3) - 1) if profit_s3 else 0
            profit_s3 = row_s3['NETPROFIT'].values[0]
        else:
            profit_s3 = 0
            yoy_s3 = 0
        if len(row_s4):
            yoy_s4 = ((row_s4['NETPROFIT'].values[0] / profit_s4) - 1) if profit_s4 else 0
            profit_s4 = row_s4['NETPROFIT'].values[0]
        else:
            profit_s4 = 0
            yoy_s4 = 0

        if allvalid:
            if yearProfit:
                yearProfit_yoy = (sum((profit_s1, profit_s2, profit_s3, profit_s4)) / yearProfit) - 1
            yearProfit = row_s1['NETPROFIT'].values[0] + row_s2['NETPROFIT'].values[0] + row_s3['NETPROFIT'].values[0] + row_s4['NETPROFIT'].values[0]

            marketValue_low = pe_low * yearProfit
            marketValue_medium = pe_medium * yearProfit
            marketValue_high = pe_high * yearProfit

            dataDict.update({
                '预估净利润':yearProfit, '预估增长率(%)': yearProfit_yoy, 
                'Q1净利润': profit_s1, 'Q1单季同比(%)': yoy_s1, 'Q2净利润': profit_s2, 'Q2单季同比(%)': yoy_s2, 
                'Q3净利润': profit_s3, 'Q3单季同比(%)': yoy_s3, 'Q4净利润': profit_s4, 'Q4单季同比(%)': yoy_s4, 
                '年度净利润': yearProfit, '低估市值': marketValue_low, '合理市值': marketValue_medium, '高估市值': marketValue_high
            })
        else:
            profitName, profitYoyName = "%d_profit_e" % year, "%d_profit_yoy" % year
            if profitName in stockConfig or profitYoyName in stockConfig:
                if profitName in stockConfig and profitYoyName not in stockConfig:
                    profit = stockConfig[profitName]
                    profitYoy = (profit / yearProfit) - 1
                else:
                    profitYoy = float(stockConfig[profitYoyName])
                    profit = yearProfit * (1 + profitYoy)
                stockConfig[profitName] = profit
                stockConfig[profitYoyName] = profitYoy
            else:
                profit = yearProfit
                profitYoy = 0
                stockConfig[profitName] = profit
                stockConfig[profitYoyName] = profitYoy

            marketValue_low = pe_low * profit
            marketValue_medium = pe_medium * profit
            marketValue_high = pe_high * profit

            dataDict.update({
                '预估净利润':profit, '预估增长率(%)': profitYoy, 
                'Q1净利润': profit_s1, 'Q1单季同比(%)': yoy_s1, 'Q2净利润': profit_s2, 'Q2单季同比(%)': yoy_s2, 
                'Q3净利润': profit_s3, 'Q3单季同比(%)': yoy_s3, 'Q4净利润': profit_s4, 'Q4单季同比(%)': yoy_s4, 
                '年度净利润': sum((profit_s1, profit_s2, profit_s3, profit_s4)), '低估市值': marketValue_low, '合理市值': marketValue_medium, '高估市值': marketValue_high
            })
            yearProfit = profit
        dataList.append(dataDict)

    datatbl = dash_table.DataTable(
        columns=DATATABLE_TITLE,
        id="%s_%s_datatbl" % (group, stockcode),
        data=dataList,
        editable=True,
        style_cell={'height': 'auto', 'width': '80px'}
    )
    return datatbl



def createInfoForStock(group, stockcode):
    stockConfig = MARKET_VALUE_CONFIG_DICT[group][stockcode]
    pe_low, pe_medium, pe_high = stockConfig["pe_low"], stockConfig["pe_medium"], stockConfig["pe_high"]

    @app.callback(
        Output("%s_%s_pe" % (group, stockcode), "data"),
        Input('%s_%s_input_low_pe' % (group, stockcode), 'value'),
        Input('%s_%s_input_medium_pe' % (group, stockcode), 'value'),
        Input('%s_%s_input_high_pe' % (group, stockcode), 'value')
    )
    def savePEState(pe_low, pe_medium, pe_high):
        print("currentPE: %s  %d %d %d" % (stockcode, pe_low, pe_medium, pe_high))
        d = {"pe_low": pe_low, "pe_medium": pe_medium, "pe_high": pe_high}
        MARKET_VALUE_CONFIG_DICT[group][stockcode].update(d)
        return json.dumps(d)

    @app.callback(
        Output("%s_%s_table" % (group, stockcode), "children"),
        Input("%s_%s_pe" % (group, stockcode), "data")
    )
    def refreshMarketValue(jsonified_pe_data):
        data = json.loads(jsonified_pe_data)
        print(data)
        return createDataTable(group, stockcode, **data)

    print("%s   %s  %s  市值：%s亿  PE-TTM：%s" % (stockcode, LOCAL_STOCK_DICT[stockcode].code, LOCAL_STOCK_DICT[stockcode].name, LOCAL_STOCK_DICT[stockcode].market_value, LOCAL_STOCK_DICT[stockcode].pe_ttm))
    return html.Div(children=[
        html.H3("%s  %s  市值：%s亿  PE-TTM：%s" % (LOCAL_STOCK_DICT[stockcode].code, LOCAL_STOCK_DICT[stockcode].name, LOCAL_STOCK_DICT[stockcode].market_value, LOCAL_STOCK_DICT[stockcode].pe_ttm)),
        html.Div(children=[
            html.P("低估PE: ", style={'marginRight':'10px', "height": "min-content"}),
            dcc.Input(id="%s_%s_input_low_pe" % (group, stockcode), value=pe_low, type='number', placeholder=pe_low, style={'marginRight':'10px', "height": "min-content"}),
            html.P("合理PE: ", style={'marginRight':'10px', "height": "min-content"}),
            dcc.Input(id="%s_%s_input_medium_pe" % (group, stockcode), value=pe_medium, type='number', placeholder=pe_medium, style={'marginRight':'10px', "height": "min-content"}),
            html.P("高估PE: ", style={'marginRight':'10px', "height": "min-content"}),
            dcc.Input(id="%s_%s_input_high_pe" % (group, stockcode), value=pe_high, type='number', placeholder=pe_high, style={'marginRight':'10px', "height": "min-content"}),
            html.Button('Refresh', id='%s_%s_refresh_btn' % (group, stockcode), n_clicks=0, style={"height": "min-content"}),
        ], style={'display': 'flex', 'flex-direction': 'row', "align-items": "center"}),
        html.Div([], id="%s_%s_table" % (group, stockcode)),
        dcc.Store(id='%s_%s_pe' % (group, stockcode)),
        html.Hr(),
        html.Div(id="%s_%s_test" % (group, stockcode))
        ], id="%s_%s_container" % (group, stockcode))


def setupLayout():
    divContentList = [
        html.Button('SaveToConfigJson', id='save_to_json', n_clicks=0, style={"height": "min-content"}),
        html.Div([], id="save_to_json_output"),
    ]
    for group, groupInfo in MARKET_VALUE_CONFIG_DICT.items():
        divContentList.append(html.H1(group))
        for stockCode, stockConfig in groupInfo.items():
            print(stockCode)
            tbl = createInfoForStock(group, stockCode)
            divContentList.append(tbl)
    app.layout = html.Div(divContentList)

    # app.layout = html.Div([
    #     html.Button('SaveToConfigJson', id='save_to_json', n_clicks=0, style={"height": "min-content"}),
    #     html.Div([], id="save_to_json_output"),
    #     createDataTable("S1", "600519", 15, 30, 50)
    # ])


@app.callback(
    Output("save_to_json_output", "children"),
    Input("save_to_json", "n_clicks")
)
def saveToConfigJson(nclicks):
    print("click save_to_json")
    if len(MARKET_VALUE_CONFIG_DICT) == 0:
        return html.P("Save to json failed, dict is empty!")
    with open(CONFIG_FILENAME, "w") as f:
        json.dump(MARKET_VALUE_CONFIG_DICT, f, indent = 4)
    return html.P("Save to json succeed")



if __name__ == '__main__':
    generateHtml()
    setupLayout()
    app.run_server(host="0.0.0.0", debug=True)

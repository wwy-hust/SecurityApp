# -*- coding:utf-8 -*-
import akshare as ak
import pandas as pd
import numpy as np
import math
import os, sys
import openpyxl
import traceback

macro_china_lpr_df = ak.macro_china_lpr()
macro_china_lpr_df.columns = ["TRADE_DATE", "LPR_1Y利率(%)", "LPR_5Y利率(%)", "短期贷款利率:6个月至1年(含)(%)", "中长期贷款利率:5年以上(%)"]
macro_china_lpr_df.to_excel("economyData/LPR.xlsx")

macro_china_fdi_df = ak.macro_china_fdi()
macro_china_fdi_df.to_excel("economyData/外商直接投资数据.xlsx")

macro_china_shrzgm_df = ak.macro_china_shrzgm()
macro_china_shrzgm_df.to_excel("economyData/社会融资规模增量统计.xlsx")

macro_china_gdp_yearly_df = ak.macro_china_gdp_yearly()
macro_china_gdp_yearly_df.to_excel("economyData/中国GDP年率.xlsx")

macro_china_cpi_yearly_df = ak.macro_china_cpi_yearly()
macro_china_cpi_yearly_df.to_excel("economyData/中国CPI年率.xlsx")

macro_china_ppi_yearly_df = ak.macro_china_ppi_yearly()
macro_china_ppi_yearly_df.to_excel("economyData/中国PPI年率.xlsx")

macro_china_pmi_yearly_df = ak.macro_china_pmi_yearly()
macro_china_pmi_yearly_df.to_excel("economyData/官方制造业PMI.xlsx")

macro_china_cx_pmi_yearly_df = ak.macro_china_cx_pmi_yearly()
macro_china_cx_pmi_yearly_df.to_excel("economyData/财新制造业PMI.xlsx")

macro_china_cx_services_pmi_yearly_df = ak.macro_china_cx_services_pmi_yearly()
macro_china_cx_services_pmi_yearly_df.to_excel("economyData/财新服务业PMI.xlsx")

macro_china_non_man_pmi_df = ak.macro_china_non_man_pmi()
macro_china_non_man_pmi_df.to_excel("economyData/中国官方非制造业PMI.xlsx")

macro_china_fx_reserves_yearly_df = ak.macro_china_fx_reserves_yearly()
macro_china_fx_reserves_yearly_df.to_excel("economyData/外汇储备_亿美元.xlsx")

macro_china_m2_yearly_df = ak.macro_china_m2_yearly()
macro_china_m2_yearly_df.to_excel("economyData/M2货币供应年率.xlsx")

macro_china_new_house_price_df = ak.macro_china_new_house_price()
macro_china_new_house_price_df.to_excel("economyData/新房价指数.xlsx")

macro_china_enterprise_boom_index_df = ak.macro_china_enterprise_boom_index()
macro_china_enterprise_boom_index_df.to_excel("economyData/企业景气及企业家信心指数.xlsx")

macro_china_national_tax_receipts_df = ak.macro_china_national_tax_receipts()
macro_china_national_tax_receipts_df.to_excel("economyData/全国税收收入.xlsx")

macro_china_bank_financing_df = ak.macro_china_bank_financing()
macro_china_bank_financing_df.to_excel("economyData/银行理财产品发行数量.xlsx")

macro_china_insurance_income_df = ak.macro_china_insurance_income()
macro_china_insurance_income_df.to_excel("economyData/原保险保费收入.xlsx")

macro_china_mobile_number_df = ak.macro_china_mobile_number()
macro_china_mobile_number_df.to_excel("economyData/中国手机出货量.xlsx")

macro_china_energy_index_df = ak.macro_china_energy_index()
macro_china_energy_index_df.to_excel("economyData/中国能源指数.xlsx")

macro_china_commodity_price_index_df = ak.macro_china_commodity_price_index()
macro_china_commodity_price_index_df.to_excel("economyData/中国大宗商品价格.xlsx")

macro_global_sox_index_df = ak.macro_global_sox_index()
macro_global_sox_index_df.to_excel("economyData/费城半导体指数.xlsx")

macro_china_construction_price_index_df = ak.macro_china_construction_price_index()
macro_china_construction_price_index_df.to_excel("economyData/中国建材价格指数.xlsx")

macro_china_lpi_index_df = ak.macro_china_lpi_index()
macro_china_lpi_index_df.to_excel("economyData/中国物流景气指数.xlsx")

macro_china_gdzctz_df = ak.macro_china_gdzctz()
macro_china_gdzctz_df.to_excel("economyData/中国城镇固定资产投资.xlsx")

macro_china_czsr_df = ak.macro_china_czsr()
macro_china_czsr_df.to_excel("economyData/财政收入.xlsx")

macro_china_xfzxx_df = ak.macro_china_xfzxx()
macro_china_xfzxx_df.to_excel("economyData/消费者信心指数.xlsx")

macro_china_consumer_goods_retail_df = ak.macro_china_consumer_goods_retail()
macro_china_consumer_goods_retail_df.to_excel("economyData/社会消费品零售总额.xlsx")

macro_china_society_electricity_df = ak.macro_china_society_electricity()
macro_china_society_electricity_df.to_excel("economyData/全社会用电分类情况表.xlsx")

macro_china_society_traffic_volume_df = ak.macro_china_society_traffic_volume()
macro_china_society_traffic_volume_df.to_excel("economyData/全社会客货运输量.xlsx")

macro_china_passenger_load_factor_df = ak.macro_china_passenger_load_factor()
macro_china_passenger_load_factor_df.to_excel("economyData/民航客座率及载运率.xlsx")

macro_china_freight_index_df = ak.macro_china_freight_index()
macro_china_freight_index_df.to_excel("economyData/航贸运价指数.xlsx")

macro_china_central_bank_balance_df = ak.macro_china_central_bank_balance()
macro_china_central_bank_balance_df.to_excel("economyData/央行货币当局资产负债.xlsx")

macro_china_insurance_df = ak.macro_china_insurance()
macro_china_insurance_df.to_excel("economyData/保险业经营情况.xlsx")

macro_china_supply_of_money_df = ak.macro_china_supply_of_money()
macro_china_supply_of_money_df.to_excel("economyData/货币供应量.xlsx")

macro_china_foreign_exchange_gold_df = ak.macro_china_foreign_exchange_gold()
macro_china_foreign_exchange_gold_df.to_excel("economyData/央行黄金和外汇储备.xlsx")

macro_china_stock_market_cap_df = ak.macro_china_stock_market_cap()
macro_china_stock_market_cap_df.to_excel("economyData/全国股票交易统计表.xlsx")

macro_china_rmb_df = ak.macro_china_rmb()
macro_china_rmb_df.to_excel("economyData/人民币汇率中间价报告.xlsx")

macro_china_market_margin_sh_df = ak.macro_china_market_margin_sh()
macro_china_market_margin_sh_df.to_excel("economyData/上海融资融券报告.xlsx")

macro_usa_cpi_monthly_se = ak.macro_usa_cpi_monthly()
macro_usa_cpi_monthly_se.to_excel("economyData/美国CPI月率报告.xlsx")

macro_usa_core_cpi_monthly_se = ak.macro_usa_core_cpi_monthly()
macro_usa_core_cpi_monthly_se.to_excel("economyData/美国核心CPI月率报告.xlsx")

macro_usa_lmci_se = ak.macro_usa_lmci()
macro_usa_lmci_se.to_excel("economyData/美联储劳动力市场状况指数报告.xlsx")

macro_usa_unemployment_rate_se = ak.macro_usa_unemployment_rate()
macro_usa_unemployment_rate_se.to_excel("economyData/美国失业率报告.xlsx")

macro_usa_non_farm_se = ak.macro_usa_non_farm()
macro_usa_non_farm_se.to_excel("economyData/美国非农就业人数报告.xlsx")

macro_usa_adp_employment_se = ak.macro_usa_adp_employment()
macro_usa_adp_employment_se.to_excel("economyData/美国ADP就业人数报告.xlsx")

macro_usa_core_pce_price_se = ak.macro_usa_core_pce_price()
macro_usa_core_pce_price_se.to_excel("economyData/美国核心PCE物价指数年率报告.xlsx")

macro_usa_trade_balance_se = ak.macro_usa_trade_balance()
macro_usa_trade_balance_se.to_excel("economyData/美国贸易帐报告.xlsx")

macro_usa_current_account_se = ak.macro_usa_current_account()
macro_usa_current_account_se.to_excel("economyData/美国经常帐报告.xlsx")

macro_usa_ppi_se = ak.macro_usa_ppi()
macro_usa_ppi_se.to_excel("economyData/美国生产者物价指数(PPI)报告.xlsx")

macro_usa_core_ppi_se = ak.macro_usa_core_ppi()
macro_usa_core_ppi_se.to_excel("economyData/美国核心生产者物价指数(PPI)报告.xlsx")

macro_usa_pmi_se = ak.macro_usa_pmi()
macro_usa_pmi_se.to_excel("economyData/美国Markit制造业PMI初值报告.xlsx")

macro_usa_ism_pmi_se = ak.macro_usa_ism_pmi()
macro_usa_ism_pmi_se.to_excel("economyData/美国ISM制造业PMI报告.xlsx")

macro_usa_nahb_house_market_index_se = ak.macro_usa_nahb_house_market_index()
macro_usa_nahb_house_market_index_se.to_excel("economyData/美国NAHB房产市场指数报告.xlsx")

macro_usa_house_starts_se = ak.macro_usa_house_starts()
macro_usa_house_starts_se.to_excel("economyData/美国新屋开工总数年化报告.xlsx")

macro_usa_new_home_sales_se = ak.macro_usa_new_home_sales()
macro_usa_new_home_sales_se.to_excel("economyData/美国新屋销售总数年化报告.xlsx")

macro_usa_building_permits_se = ak.macro_usa_building_permits()
macro_usa_building_permits_se.to_excel("economyData/美国营建许可总数报告.xlsx")

macro_usa_house_price_index_se = ak.macro_usa_house_price_index()
macro_usa_house_price_index_se.to_excel("economyData/美国FHFA房价指数月率报告.xlsx")

macro_usa_nfib_small_business_se = ak.macro_usa_nfib_small_business()
macro_usa_nfib_small_business_se.to_excel("economyData/美国NFIB小型企业信心指数报告.xlsx")

macro_usa_initial_jobless_se = ak.macro_usa_initial_jobless()
macro_usa_initial_jobless_se.to_excel("economyData/美国初请失业金人数报告.xlsx")

macro_euro_gdp_yoy_df = ak.macro_euro_gdp_yoy()
macro_euro_gdp_yoy_df.to_excel("economyData/欧元区季度GDP年率报告.xlsx")

macro_euro_cpi_mom_df = ak.macro_euro_cpi_mom()
macro_euro_cpi_mom_df.to_excel("economyData/欧元区CPI月率报告.xlsx")

macro_euro_cpi_yoy_df = ak.macro_euro_cpi_yoy()
macro_euro_cpi_yoy_df.to_excel("economyData/欧元区CPI年率报告.xlsx")

macro_euro_ppi_mom_df = ak.macro_euro_ppi_mom()
macro_euro_ppi_mom_df.to_excel("economyData/欧元区PPI月率报告.xlsx")

macro_euro_unemployment_rate_mom_df = ak.macro_euro_unemployment_rate_mom()
macro_euro_unemployment_rate_mom_df.to_excel("economyData/欧元区失业率报告.xlsx")

macro_euro_manufacturing_pmi_df = ak.macro_euro_manufacturing_pmi()
macro_euro_manufacturing_pmi_df.to_excel("economyData/欧元区制造业PMI初值报告.xlsx")

macro_euro_services_pmi_df = ak.macro_euro_services_pmi()
macro_euro_services_pmi_df.to_excel("economyData/欧元区服务业PMI终值报告.xlsx")

macro_euro_zew_economic_sentiment_df = ak.macro_euro_zew_economic_sentiment()
macro_euro_zew_economic_sentiment_df.to_excel("economyData/欧元区ZEW经济景气指数报告.xlsx")

macro_cons_gold_df = ak.macro_cons_gold()
macro_cons_gold_df.to_excel("economyData/全球最大黄金ETF—SPDR_Gold_Trust_持仓报告.xlsx")

macro_cons_opec_month_df = ak.macro_cons_opec_month()
macro_cons_opec_month_df.to_excel("economyData/欧佩克报告.xlsx")

macro_euro_lme_holding_df = ak.macro_euro_lme_holding()
macro_euro_lme_holding_df.to_excel("economyData/伦敦金属交易所_持仓报告.xlsx")

macro_euro_lme_stock_df = ak.macro_euro_lme_stock()
macro_euro_lme_stock_df.to_excel("economyData/伦敦金属交易所_库存报告.xlsx")

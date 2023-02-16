# SecurityApp
个人用来更新仓位和估值的工具

数据来源为Akshare https://github.com/akfamily/akshare

支持A股、港股、美股、外汇。

## Requirement：

1. 安装Anaconda https://www.anaconda.com/
2. pip install akshare
3. pip install dash

## Useage：

更新仓位：
首先在 position.xlsx 中更新股票代码（Code）及数量（Num），关闭文档后执行下列脚本即可更新仓位。

python update_position.py

更新估值：
在 valueTrack.xlsx 中左侧一列填入股票代码执行下列脚本即可更新基础信息、及当前市值。

python track_market_value.py

或

python generate_market_value_html.py

## History：
2022.08.11 
1. 汇率增加默认值，akshare获取不到时取默认值进行汇率换算
2. pdframe中key同时支持英文与中文
3. 新增股债利差分位脚本interest_margin.py

2022.10.08
1. bugfix，修复StockInfo.py导致Proxy数据被覆盖的bug
2. 新增generate_market_value_html.py，基于ploty.Dash展示追踪的公司净利润和估值

2022.10.12
1. track_market_value.py 也自动更新季度净利润数据
2. bugfix，修复StockInfoProxy中当前市值不正确的问题

2023.02.08
1. bugfix，A股获取PE-TTM、MarketValue等数据失败情况的处理
2. 新增economy_data.py导出akshare中常用的宏观数据

2023.02.16
1. update_position.py增加计算仓位的功能。

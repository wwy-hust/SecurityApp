
# History

2024.06.26

1.  大部分数据来源改为FutuApi

2.  update\_position中增加一列股息率，可以统计全部仓位的加权平均股息率

2024.06.10

1.  重构，股票代码前面增加前缀代表股票分类，例如a. hk. us. cash.

2.  对于获取不到数据的标的，可以在StockInfoLibrary/UserDefinedStockInfoData.py中自定义名称和价格

2024.04.18

1.  新增可转债支持

2023.02.16

1.  update\_position.py增加计算仓位的功能。

2023.02.08

1.  bugfix，A股获取PE-TTM、MarketValue等数据失败情况的处理

2.  新增economy\_data.py导出akshare中常用的宏观数据

2022.10.12

1.  track\_market\_value.py 也自动更新季度净利润数据

2.  bugfix，修复StockInfoProxy中当前市值不正确的问题

2022.10.08

1.  bugfix，修复StockInfo.py导致Proxy数据被覆盖的bug

2.  新增generate\_market\_value\_html.py，基于ploty.Dash展示追踪的公司净利润和估值

2022.08.11

1.  汇率增加默认值，akshare获取不到时取默认值进行汇率换算

2.  pdframe中key同时支持英文与中文

3.  新增股债利差分位脚本interest\_margin.py


# SecurityApp

个人用来更新仓位和估值的工具

数据来源为FutuApi和Akshare <https://github.com/akfamily/akshare>

支持A股、港股、美股、外汇、可转债、ETF。

## Installation

1. 配置Python3环境，推荐直接安装Anaconda <https://www.anaconda.com/>

2. clone本仓库，安装依赖 pip install -r requirements.txt
> 依赖如下：
> akshare, futu-api

1. (可选，使用futu做数据源，更新更快) 安装futu OpenD https://openapi.futunn.com/futu-api-doc/opend/opend-intro.html

3.1 登录futu OpenD，默认端口是11111，如果端口有变化需要在`StockInfoClass/FutuApiDataHelper.py`中修改端口。

3.2 `StockInfoClass/Config.py`中修改数据源为`DataSourceType.FUTU`

## Useage

首先修改position.xlsx中的Code和Num字段，Code是证券的代码，Num是持有的数量，修改完毕后执行`python update_position.py`


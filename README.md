# SecurityApp
个人用来更新仓位和估值的工具

数据来源为Akshare https://github.com/akfamily/akshare

支持A股、港股、美股、外汇。

## Requirement：

1. 安装Anaconda https://www.anaconda.com/
2. pip install akshare

## Useage：

更新仓位：
首先在 position.xlsx 中更新股票代码（Code）及数量（Num），关闭文档后执行下列脚本即可更新仓位。

python update_position.py

更新估值：
在 valueTrack.xlsx 中左侧一列填入股票代码执行下列脚本即可更新基础信息、及当前市值。

python track_market_value.py
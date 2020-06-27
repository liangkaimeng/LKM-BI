#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : lkm

from RFM import get_data

data = get_data.data(r"D:\LKM\BI\Member_Analysis_RFM\Power BI Version\数据源.xlsx")

# 查看前十条数据
print(data.head(10))

# 查看数据的类型和缺失情况
print(data.info())
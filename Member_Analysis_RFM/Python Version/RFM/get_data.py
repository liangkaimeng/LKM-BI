#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : lkm

import pandas as pd

def data(file):
    return pd.read_excel(file)

# if __name__ == '__main__':
#     print(data(r"D:\LKM\BI\Member_Analysis_RFM\Power BI Version\数据源.xlsx"))
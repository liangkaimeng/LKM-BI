#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : lkm

import pandas as pd

class RFM_MODEL:
    def __init__(self):
        pass

    def model_r(self, data, strData, dataTime, customer):
        R = data.groupby(customer)[dataTime].max().reset_index()
        R['R'] = (pd.to_datetime(strData) - R[dataTime]).dt.days
        return R

    def model_f(self, data, dateLabel, dataTime, customer):
        data[dateLabel] = data[dataTime].astype(str).str[:10]
        F = data.groupby([customer, dateLabel])[dataTime].count().reset_index()
        F = F.groupby(customer)[dataTime].count().reset_index()
        F.columns = [customer, 'F']
        return F

    def model_m(self, data, sales, customer):
        M = data.groupby(customer)[sales].sum().reset_index()
        M.columns = [customer, 'S_Money']
        return M

    def rfm_target(self, data, strData, sales, customer, dateLabel, dataTime, r_bins, f_bins, m_bins):
        fm = pd.merge(self.model_m(data, sales, customer), self.model_f(data, dateLabel, dataTime, customer),
                      left_on=customer, right_on=customer, how='inner')
        fm['M'] = fm['S_Money'] / fm['F']
        rfm = pd.merge(self.model_r(data, strData, dataTime, customer), fm, left_on=customer,
                       right_on=customer, how='inner')

        rfm['R-SCORE'] = pd.cut(rfm['R'], bins=r_bins, labels=[5, 4, 3, 2, 1], right=False).astype(float)
        rfm['F-SCORE'] = pd.cut(rfm['F'], bins=f_bins, labels=[1, 2, 3, 4, 5], right=False).astype(float)
        rfm['M-SCORE'] = pd.cut(rfm['M'], bins=m_bins, labels=[1, 2, 3, 4, 5], right=False).astype(float)

        rfm['R_than_mean'] = ((rfm['R-SCORE'] > rfm['R-SCORE'].mean()) * 1).astype(str)
        rfm['F_than_mean'] = ((rfm['F-SCORE'] > rfm['F-SCORE'].mean()) * 1).astype(str)
        rfm['M_than_mean'] = ((rfm['M-SCORE'] > rfm['M-SCORE'].mean()) * 1).astype(str)

        rfm['人群数值'] = rfm['R_than_mean'] + rfm['F_than_mean'] + rfm['M_than_mean']
        rfm['人群标签'] = rfm['人群数值'].apply(self.transform_label)

        return rfm

    def transform_label(self, x):
        if x == '111':
            label = '重要价值客户'
        elif x == '110':
            label = '消费潜力客户'
        elif x == '101':
            label = '频次深耕客户'
        elif x == '100':
            label = '新客户'
        elif x == '011':
            label = '重要价值流失预警客户'
        elif x == '010':
            label = '一般客户'
        elif x == '001':
            label = '高消费唤回客户'
        elif x == '000':
            label = '流失客户'
        return label

    def Read_Data(self, file):
        return pd.read_excel(file)
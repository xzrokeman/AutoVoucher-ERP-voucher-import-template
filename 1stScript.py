#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import pandas as pd
from functools import reduce

wb = xlrd.open_workbook("D:\PyLessons\PyTest1.xlsx")#获取一个sheet对象
sheet1 = wb.sheets()[0]
nrows = sheet1.nrows

def GetRows(sheet1):
    N = []
    
    for x in range(nrows):
        N.append(sheet1.row_values(x))
    return N

S = GetRows(sheet1) #S即列表形式的费用明细单，作为分录首行的输入

def vouch(Entry):
    def genvouch(Entry):
        if ("6602002" in Entry[3]) or ("6602003" in Entry[3]):      #处理需要过应付职工薪酬的费用科目，这样的凭证会多出两行分录
            Entry1 = [Entry[0], Entry[1], Entry[2], Entry[3], Entry[4], 0.00]
            Entry2 = [Entry[0], Entry[1], Entry[2], "2211" + Entry[3][4:], 0.00, Entry[4]]
            Entry3 = [Entry[0], Entry[1], Entry[2], "2211" + Entry[3][4:], Entry[4], 0.00]
            Entry4 = [Entry[0], Entry[1], Entry[2], "1002001002", 0.00, Entry[4]]
            return Entry1, Entry2, Entry3, Entry4
        else:
            Entry1 = [Entry[0], Entry[1], Entry[2], Entry[3], Entry[4], 0.00]
            Entry2 = [Entry[0], Entry[1], Entry[2], "1002001002", 0.00, Entry[4]]
            return Entry1, Entry2
    voucher = genvouch(Entry)
    L = []
    for item in voucher:
        L.append(item)
    return L

X=[]
for Entry in S:
    X.append(vouch(Entry))

XX=reduce(lambda x,y: x+y,X)
XX
df = pd.DataFrame(XX)

writer = pd.ExcelWriter('D:\PyLessons\output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

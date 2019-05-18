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



def GenVouch(Entry1):
    Entry2 = [Entry1[0], Entry1[1], Entry1[2], "1002001002", 0.00, Entry1[4]]
    return Entry1,Entry2

def Vouch():
    Voucher = GenVouch(Entry1)
    L = []
    for item in Voucher:
        L.append(item)
X=[]
for Entry1 in S:
    X.append(L)

    
XX=reduce(lambda x,y: x+y,X)
XX
df = pd.DataFrame(XX)

writer = pd.ExcelWriter('D:\PyLessons\output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

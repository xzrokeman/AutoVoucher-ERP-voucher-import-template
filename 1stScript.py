#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import pandas as pd
from functools import reduce

wb = xlrd.open_workbook("D:\PyLessons\PyTest1.xlsx")#获取一个sheet对象
sheet1 = wb.sheets()[0]
nrows = sheet1.nrows#获取sheet的行数
#获取sheet中所有行
def GetRows(sheet1):
    N = []
    
    for x in range(nrows):
        N.append(sheet1.row_values(x))
    return N

S = GetRows(sheet1) #S即列表形式的费用明细单，作为分录首行的输入

#首行会计分录（也即是明细单中的一行）Entry1 = ["1", "2", "TrafficExpense", "6602008", 396.00, 0.00]，结构为
#【编号，附件数，摘要，科目编码，贷方金额】

def GenVouch(Entry1):#生成后续分录行，先只考虑最简单的费用业务，借费用贷银行
    Entry2 = [Entry1[0], Entry1[1], Entry1[2], "1002001002", 0.00, Entry1[4]]
    return Entry1,Entry2 #根据科目不同，可以用if语句做几个分支，如工资或福利费凭证可能有4行分录
#以上获取的会计凭证为一个tuple，元组中的每一个元素为一个list,结构参考Entry1，接下来将整个元组列表化：
def Vouch():
    Voucher = GenVouch(Entry1)
    L = []
    for item in Voucher:
        L.append(item)
X=[]
for Entry1 in S:
    X.append(L)
#列表化后的L是一个三重list:L本身是一个list,L中的每一个元素（会计凭证）是list,其中的每一个元素（分录行）仍然是list
#为了便于通过pandas生成“数据帧”（DataFrame）的数据结构并输出到excel(主要目的），需要将凭证级别的list合并，而
#python的list用加法就可以实现合并了，使用最高效的reduce函数即可完成
XX=reduce(lambda x,y: x+y,X)
XX
df = pd.DataFrame(XX)

writer = pd.ExcelWriter('D:\PyLessons\output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
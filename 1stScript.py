#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import pandas as pd
from functools import reduce

wb = xlrd.open_workbook("D:\PyLessons\PyTest1.xlsx")#��ȡһ��sheet����
sheet1 = wb.sheets()[0]
nrows = sheet1.nrows#��ȡsheet������
#��ȡsheet��������
def GetRows(sheet1):
    N = []
    
    for x in range(nrows):
        N.append(sheet1.row_values(x))
    return N

S = GetRows(sheet1) #S���б���ʽ�ķ�����ϸ������Ϊ��¼���е�����

#���л�Ʒ�¼��Ҳ������ϸ���е�һ�У�Entry1 = ["1", "2", "TrafficExpense", "6602008", 396.00, 0.00]���ṹΪ
#����ţ���������ժҪ����Ŀ���룬������

def GenVouch(Entry1):#���ɺ�����¼�У���ֻ������򵥵ķ���ҵ�񣬽���ô�����
    Entry2 = [Entry1[0], Entry1[1], Entry1[2], "1002001002", 0.00, Entry1[4]]
    return Entry1,Entry2 #���ݿ�Ŀ��ͬ��������if�����������֧���繤�ʻ�����ƾ֤������4�з�¼
#���ϻ�ȡ�Ļ��ƾ֤Ϊһ��tuple��Ԫ���е�ÿһ��Ԫ��Ϊһ��list,�ṹ�ο�Entry1��������������Ԫ���б���
def Vouch():
    Voucher = GenVouch(Entry1)
    L = []
    for item in Voucher:
        L.append(item)
X=[]
for Entry1 in S:
    X.append(L)
#�б����L��һ������list:L������һ��list,L�е�ÿһ��Ԫ�أ����ƾ֤����list,���е�ÿһ��Ԫ�أ���¼�У���Ȼ��list
#Ϊ�˱���ͨ��pandas���ɡ�����֡����DataFrame�������ݽṹ�������excel(��ҪĿ�ģ�����Ҫ��ƾ֤�����list�ϲ�����
#python��list�üӷ��Ϳ���ʵ�ֺϲ��ˣ�ʹ�����Ч��reduce�����������
XX=reduce(lambda x,y: x+y,X)
XX
df = pd.DataFrame(XX)

writer = pd.ExcelWriter('D:\PyLessons\output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
#!/usr/bin/env python3
# coding: utf-8
import pandas as pd
import numpy as np
"""
银行对账，事实上最直白的解决方案就是用sql中的join方法；
对应在pandas中，join的对应操作就是merge方法。
因为在一边表中可能存在重复值，因此merge之后需要两边去重，
这样才能保证勾兑后两边的记录是一对一的
勾兑确保一一对应，不能一一对应的全部抛出，再进行人工处理（未达）
搜遍谷歌和百度也见不到解决这类问题的代码，实则是因为...
...这只是一个在数据库领域早就用sql已经解决了的问题
sql不能解决的问题就在那些剩余的未能自动一一对应的记录里面
可能包含一些没有显著规律的摘要/编码，可能其中的多条合并可以和另一边的
多条合并后产生对应关系……现实世界中很难规范客户的行为(有的人就是不写摘要)，
因此对账，特别是收入和往来的对账会一直是pain in the ass
万幸的是这个简单的解决方案对于我来说已经足够了
建议放到notebook里方便一步一步理解，groupby是重点
当出现大量重复金额的时候怎么办？方法就是增加辅助列对重复值进行编号，
通过dataframe.groupby(['column_name']).cumcount()
形成
100   0
100   1
100   2
...
的形式，这样value+辅助列编号就成了参照，不再是“重复值”了，merge就可以实现“一一对应”
然后在merge的时候将辅助列名和值列名包含在on参数（一个序列）中传进去
"""
#读取日记账和银行对账单，生成dataframe
"""
table bank:
    I_id: int
    abstract: str
    amount: float
    ref: int

same for book
"""
book_xls = pd.read_excel(r"book.xlsx")
bank_xls = pd.read_excel(r"bank.xlsx")
book = pd.DataFrame(book_xls)
bank = pd.DataFrame(bank_xls)
#强行用编号列作为索引，pandas看到整数编号默认转换为int64类型（numpy dtype）
book.set_index('I_id', inplace = True)
bank.set_index('I_id', inplace = True)
#对于空值（NaN,numpy dtype）,全部填充为0方便后续处理
book.fillna(0, inplace = True)
bank.fillna(0, inplace = True)
#强制转换dataframe数据类型，这一步是很多数据处理的基础，除了统一类型便于运算外
#也有利于避免因类型检查带来的性能问题
book['ref']=book['ref'].astype('int64')
bank['ref']=bank['ref'].astype('int64')
#日记账和银行对账单借贷方向相反，调整成相同的便于后面处理
bank['amount'] = -1 * bank['amount']
#groupby!!!
book['g'] = book.groupby('amount').cumcount()
bank['g'] = bank.groupby('amount').cumcount()
#merge两个表，对账。https://stackoverflow.com/questions/47094551/merge-one-to-one-dataframe-in-pandas
book1=pd.merge(book,bank,on=['amount','g'],how='inner').drop('g',axis=1)
#根据index从源表中删去已经勾兑的记录
book_left = book.copy()
for ind in book1['ref_x'].values:
    book_left.drop(index = ind, axis = 1, inplace=True)
bank_left = bank.copy()
for ind in book1['ref_y'].values:
    bank_left.drop(index = ind, axis = 1, inplace=True)

#book1为已经勾兑的记录（2 in 1）
#book_left为日记账未勾兑项目
#bank_left为银行帐未勾兑项目
result = [book1, book_left, bank_left]

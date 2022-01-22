import pandas as pd
import numpy as np

t_gl = pd.read_excel("1117M.xlsx", sheet_name="sheet1", dtype={'项目名称': str, '项目编码': str, '客户编码': str}).fillna(0)[["科目编码", "科目名称", "项目名称", "项目编码", "客户编码", "客户名称", "方向_", "期末余额金额"]]
t_gl['期末余额金额'] = np.where(t_gl['方向_']=="借", -1 * t_gl['期末余额金额'], t_gl['期末余额金额'])

t_rr = pd.read_excel("M10R.xlsx", sheet_name="Sheet1").fillna(0)[["受案号", "收入", "增值税"]]# [["受案号", "申请方收入", "申请方增值税", "被申请方收入", "被申请方增值税", "收入", "增值税", "申请方", "被申请方"]]
# t_rr.filter()
t_rr['sett']=np.NaN
t_rr.fillna(0)

def settle(id):
    df_rec = t_gl.loc[(t_gl['项目名称']==t_rr.loc[id].受案号)].sort_values(by='期末余额金额')# ascending
    sett = -1*(t_rr.loc[id].收入+t_rr.loc[id].增值税)# the offset_amount = revenue + VAT
    if df_rec['期末余额金额'].sum() + sett >= 0:# exploiting list as a queue to do the Fifo job
        Q = df_rec["期末余额金额"].tolist()
        Le = len(Q)
        while Q[0] + sett < 0:
            sett = sett + Q[0]
            Q.pop(0)
        
        Q[0] = Q[0] + sett
        Q = [0*i for i in range(Le-len(Q))]+Q
        df_rec["期末余额金额"] = np.array(Q)# 1. Update the gl records after every settlement transaction
                                           # np.array is almost the default method of updating a column of values in pandas
        t_rr.loc[id,'sett'] = 1.0# 2. Mark the line items that has been successfully settled
                                 # Always update cell value using "df.loc[index, column_name]= value" style
    else:
        print("Error, please check")
    for id in df_rec.index.values:
        t_gl.loc[id, "期末余额金额"] = df_rec.loc[id, "期末余额金额"]
        print("Settled, please check the result")
        
for id in t_rr.index.values:
    settle(id)

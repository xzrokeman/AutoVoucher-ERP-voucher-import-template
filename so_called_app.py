#!/usr/bin/env python
# coding: utf-8
import streamlit as st

from decimal import *
from dataclasses import dataclass
from typing import Optional, List

# 首先计算仲裁费，分案件适用规则类型讨论
@dataclass
class Rate(object):
    start: Optional[float]
    end: Optional[float]
    rate: float
    base: float


# 普通程序处理费率表CaseType=1
handling_fee_rate = [
    Rate(None, 1000, 0, 100),
    Rate(1000, 50000, 0.05, 100),
    Rate(50000, 100000, 0.04, 2550),
    Rate(100000, 200000, 0.03, 4550),
    Rate(200000, 500000, 0.02, 7550),
    Rate(500000, 1000000, 0.01, 13550),
    Rate(1000000, None, 0.005, 18550),
]
# 普通程序受理费率表CaseType=1
acceptance_fee_rate = [
    Rate(None, 200000, 0, 8000),
    Rate(200000, 500000, 0.02, 8000),
    Rate(500000, 1000000, 0.015, 14000),
    Rate(1000000, 3000000, 0.005, 21500),
    Rate(3000000, 6000000, 0.0045, 31500),
    Rate(6000000, 10000000, 0.004, 45000),
    Rate(10000000, 20000000, 0.003, 61000),
    Rate(20000000, 40000000, 0.002, 91000),
    Rate(40000000, None, 0.0015, 131000),
]

# 国际、涉外或涉港澳台案件仲裁费率表CaseType=2
foreign_case_fee_rate = [
    Rate(None, 1000000, 0.035, 0),
    Rate(1000000, 5000000, 0.025, 35000),
    Rate(5000000, 10000000, 0.015, 135000),
    Rate(10000000, 50000000, 0.01, 210000),
    Rate(50000000, None, 0.0065, 610000),
]

# 申请其他仲裁规则仲裁费率表CaseType=3
other_arbitration_rule_fee_rate = [
    Rate(None, 1000000, 0.014, 0),
    Rate(1000000, 5000000, 0.01, 14000),
    Rate(5000000, 10000000, 0.006, 54000),
    Rate(10000000, 50000000, 0.004, 84000),
    Rate(50000000, None, 0.002, 244000),
]

# 金融案件受理费率表CaseType=4
financial_loan_arbitration_acceptance_fee_rate = [
    Rate(None, 1000, 0, 100),
    Rate(1000, 50000, 0.05, 100),
    Rate(50000, 100000, 0.04, 2550),
    Rate(100000, 200000, 0.03, 4550),
    Rate(200000, 500000, 0.02, 7550),
    Rate(500000, 1000000, 0.01, 13550),
    Rate(1000000, None, 0.005, 18550),
]

# 金融案件处理费率表CaseType=4
financial_loan_arbitration_handling_fee_rate = [
    Rate(None, 400000, 0, 5000),
    Rate(400000, 1000000, 0.008, 5000),
    Rate(1000000, 3000000, 0.005, 9800),
    Rate(3000000, 5000000, 0.004, 19800),
    Rate(5000000, 10000000, 0.003, 27800),
    Rate(10000000, 30000000, 0.002, 42800),
    Rate(30000000, 50000000, 0.0015, 82800),
    Rate(50000000, None, 0, 112800),
]

# 适用《联合国国际贸易法委员会仲裁规则》案件的费用因与争议金额没有直接联系，此处暂不考虑

arbitral_tribunal_remuneration_rate = [
    Rate(None, 20000, 0, 13200),
    Rate(20000, 50000, 0.385, 13200),
    Rate(50000, 100000, 0.275, 24750),
    Rate(100000, 150000, 0.231, 38500),
    Rate(150000, 200000, 0.187, 50050),
    Rate(200000, 250000, 0.176, 59400),
    Rate(250000, 300000, 0.165, 68200),
    Rate(300000, 400000, 0.143, 76450),
    Rate(400000, 500000, 0.132, 90750),
    Rate(500000, 1000000, 0.121, 103950),
    Rate(1000000, 10000000, 0.099, 164450),
    Rate(10000000, None, 0.033, 1055450),
]

# AID stands for "Amount in dispute"
def find_rate(rates: List[Rate], AID: float) -> Optional[Rate]:
    for r in rates:
        if (r.start is None or r.start < AID) and (r.end is None or r.end >= AID):
            return r
    raise Exception("Cannot find rate!")


def count_fee(AID: float, rates: List[Rate]) -> float:
    if find_rate(rates, AID).start == None:
        start = 0
    else:
        start = find_rate(rates, AID).start

    fee = (AID - start) * find_rate(rates, AID).rate + find_rate(rates, AID).base
    return fee


# 国内案件="1"
# 涉外案件="2"
# 其他规则案件="3"
# 金融案件="4"
def arbitration_fee(AID: float, CaseType: str) -> float:
    if CaseType == "1":
        acceptance_fee = count_fee(AID, acceptance_fee_rate)
        handling_fee = count_fee(AID, handling_fee_rate)
        arbitration_fee = acceptance_fee + handling_fee
        return arbitration_fee
    elif CaseType == "2":
        arbitration_fee = count_fee(AID, foreign_case_fee_rate)
        if arbitration_fee < 10000:
            arbitration_fee = 10000
        return arbitration_fee
    elif CaseType == "3":
        arbitration_fee = count_fee(AID, other_arbitration_rule_fee_rate)
        if arbitration_fee < 4000:
            arbitration_fee = 4000
        return arbitration_fee
    elif CaseType == "4":
        acceptance_fee = count_fee(AID, financial_loan_arbitration_acceptance_fee_rate)
        handling_fee = count_fee(AID, financial_loan_arbitration_handling_fee_rate)
        arbitration_fee = acceptance_fee + handling_fee
        return arbitration_fee
    else:
        raise Exception("Cannot find case type!")


# arbitration_fee(1000, "3")
def count_arbitral_tribunal_remuneration(
    arbitration_fee: float, rates: List[Rate]
) -> float:
    if find_rate(rates, arbitration_fee / 1.03).start == None:
        start = 0
    else:
        start = find_rate(rates, arbitration_fee / 1.03).start
    AT_remuneration = (arbitration_fee / 1.03 - start) * find_rate(
        rates, arbitration_fee / 1.03
    ).rate + find_rate(rates, arbitration_fee / 1.03).base
    return AT_remuneration


def my_decimal(x):
    return Decimal(x).quantize(Decimal("0.00"))


case_type = ["国内案件", "涉外案件", "其他规则案件", "金融案件"]
"""
# 仲裁费计算:
"""
number1 = st.number_input("争议金额")
option1 = st.selectbox("案件类型", case_type)
number2 = case_type.index(option1) + 1
number3 = count_arbitral_tribunal_remuneration(
    arbitration_fee(number1, str(number2)), arbitral_tribunal_remuneration_rate
)
expedited_procedure = st.checkbox("简易程序")

st.write("仲裁费金额为： ", my_decimal(arbitration_fee(number1, str(number2))))

if expedited_procedure:
    if number2 in (1, 2, 3):
        st.write("独任仲裁员报酬（含裁决稿酬）为： ", my_decimal(number3 * 0.7))
    else:
        st.write("独任仲裁员报酬（含裁决稿酬）为： ", my_decimal(number3 * 0.65))
else:
    if number2 == 4:
        st.write("首席仲裁员报酬（含裁决稿酬）为： ", my_decimal(0.58 * number3))
        if my_decimal(0.21 * number3) >= 4000:
            st.write("边裁报酬为： ", my_decimal(0.21 * number3))
        else:
            st.write("边裁报酬为： ", my_decimal(4000))
    else:
        if my_decimal(0.175 * number3) >= 6000:
            st.write("首席仲裁员报酬（含裁决书撰写）为： ", my_decimal(0.65 * number3))
            st.write("边裁报酬为： ", my_decimal(0.175 * number3))

        elif (my_decimal(0.65 * number3) >= 10000) and (
            my_decimal(0.175 * number3) <= 6000
        ):
            st.write("首席仲裁员报酬（含裁决书撰写）为： ", my_decimal(0.65 * number3))
            st.write("边裁报酬为： ", my_decimal(6000))
        else:
            st.write("首席仲裁员报酬（含裁决书撰写）为： ", my_decimal(10000))
            st.write("边裁报酬为： ", my_decimal(6000))

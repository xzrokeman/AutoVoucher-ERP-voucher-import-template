from functools import reduce
import re
from typing import List, Dict, Set, Tuple, Optional, Callable, Iterable


def CaseCode(string: str) -> str:#调整案号，接收参数必须为规范的案件案号，否则可能出现不可预测的错误
        
    def CasePrefix(string: str) -> str:
        if "医疗" in string:
            return "yl"
        elif "深仲涉外" in string:
            return "sw"
        elif "深仲" in string:
            return "sz"
        elif "深国仲" in string:
            return "gz"
        elif "SHEN" in string:
            return ""
        else:
            return "#NOT A CASE"
            
    def CaseNum(string: str) -> str:
        if len(reduce(lambda x, y: x + y, re.findall(r"\d+\.?\d*",string))) < 5:
            return ""
        else:
            numbers = str(reduce(lambda x, y: x + y, re.findall(r"\d+\.?\d*",string)))
            if len(numbers) < 8:
                numbers = numbers[0:4]+"0"*(8-len(numbers))+numbers[4:]
                return numbers
            else:
                return numbers[0:8]

    if CasePrefix(string) == "#NOT A CASE":
        return string
    else:
        return CasePrefix(string) + str(CaseNum(string))

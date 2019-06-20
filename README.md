# AutoVoucher-ERP-voucher-import-template-
## Practicing python to excel techniques.
## 出发点
主要是为了根据银行流水生成简单的会计凭证导入模板（仅针对"大量、简单、重复"的付现费用类业务）。  
对于一个新手（主职是会计）来说最关注的不是代码质量（顶用最重要），节省（做账）时间，减少人工失误才是主要目的。  
这里的所有方法都是ERP早已实现的功能，因为资源限制没法通过采购来实现，单位的开发力量主要不用于支持财务，所以自力更生、特别擅长半自动处理成为了必备素质-_-#  
凭证生成规则其实是主流ERP都有的功能，客观原因导致现在只能用一款20多年前架构的老爷软件做账，为了保护视力……  

1. 已经实现最简单的费用根据流水（from Excel）生成两行的凭证（借费用贷银行）并追加到一个凭证序时簿（to Excel）；
2. 针对不同的分录科目生成多行后续分录（如需要走中间科目“应付职工薪酬”的情形），这一块儿现在是通过不同分支写死分录来实现的，因为还没有想清楚构建一个什么框架来反映这类业务的实质。先利用pandas和xslxwriter对表格的操作做一些简单的预处理，达到目的即可；
3. 无论是通过原生Python还是通过SQLAlchemy来定义上述两个类都比较繁琐，偶然看到了attrs, dataclasses库的介绍，所以做了一些改进；由于Python的类可以很方便地字典化，所以总体思路调整为：
    i. 运用@attrs或@dataclasses定义类
    ii. 将JournalEntry类属性字典化（vars），利用pandas生成DataFrame
    iii. 后续数据库操作可以考虑使用SQLAlchemy
    iiii. 考虑为批量excel导入银行日记账写一个方法（20190620）

## Todo:

1. 自动补充现金流量字段（主表项目编码、附表项目编码、借方金额、贷方金额）；
2. 拟将费用明细行作为一个类'class JournalEntry'，费用明细的属性（编号，摘要，费用类型，金额，辅助核算项）作为参数传入一个类方法生成若干凭证分录行'class VoucherEntry'，凭证分录行直接取（编号，摘要），会计科目编码作为一个枚举类，对应不同的费用类型。明细金额传给凭证分录，并根据费用类型指导不同实例的不同属性值（各分录行的借、贷金额）；  

```python
class JournalEntry  
class VoucherEntry
```  

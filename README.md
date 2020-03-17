# Python scripts for accounting
## What I know about accounting and programming
The profession of accounting is all about recognition, measuring, recording and reporting. And all above can be summarized as proper classification of business transactions. To classify the transactions we need Accounting Standards or Taxonomy(as they called it in XBRL). Basically these are rules that book-keeping and reporting must compliant with. In greater sense, the rules include not only the standards, but processes performed daily as well(in the realm of internal control). As long as there are rules(most of them are very simple), there are situations programming could step in. ERPs have been around for quite a long time, yet they leave many problems unsolved. However, with few lines of code, my life as an accountant is becoming much easier.

What I have learned from accounting practice is that accountants are way too behind what was decribed in an "Intermediate Accounting" text book. Accountant is nothing about management if you spend all day entering the entries, so bear in mind to let others or a machine to do the basics for you.
## The aim of this repo
为了将手头的核算工作完全自动化而不依赖于任何特定的ERP产品

目前已完成的：1.单据转换规则（根据业务单据生产成会计凭证）；2.银行对账；3.批量新增核算项目（直接改数据库）

提上日程的：1.自动报表（标准格式表及图表）；2.出纳日记账（用django实现）

长期目标：1.数据同步（从业务系统获取新的业务信息并同步到ERP基础资料中）；2.整合工具包中的所有功能，形成一套文档；3.财务数据对接XBRL

这里的所有方法都是ERP早已实现的功能，因为资源限制没法通过采购来实现，单位的开发力量主要不用于支持财务，所以自力更生、特别擅长半自动处理成为了必备素质-_-#  

2020-3-13

银行对账问题有了一个当前所掌握技能条件下的最优解：pandas的groupby和merge方法。这个问题在sql下早已得到解决，即两张表根据一个或多个字段实现记录的一一对应。

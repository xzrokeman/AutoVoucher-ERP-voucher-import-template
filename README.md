# Python scripts for accounting
## What I know about accounting and programming
The profession of accounting is all about recognition, measuring, recording and reporting. And all above can be summarized as proper classification of business transactions. To classify the transactions we need Accounting Standards or Taxonomy(as they called it in XBRL). Basically these are rules that book-keeping and reporting must compliant with. In greater sense, the rules include not only the standards, but processes performed daily as well(in the realm of internal control).   
As long as there are rules(most of them are very simple) in a process, there is a place for programming. ERPs have been around for quite a long time, yet they leave many problems unsolved for it is too hard for traditional developers to follow the changing pace of the real world management needs. However, with few lines of code, my life as an accountant is becoming much easier. Accountants are of stronger capability on understanding and designing business rules under this particular scenario.  

What I have learned from accounting practice is that accountants are way too behind what was decribed in an "Intermediate Accounting" text book. Accountant is nothing about management if you spend all day entering the entries, so bear in mind to let others or a machine to do the basics for you.
## The aim of this repo
为了将手头的核算工作完全自动化而不依赖于任何特定的ERP产品

目前已完成的：1.单据转换规则（根据业务单据生产成会计凭证）；2.银行对账；3.批量新增核算项目（直接改数据库）

提上日程的：1.自动报表（标准格式表及图表）；2.出纳日记账（用django实现）

长期目标：1.数据同步（从业务系统获取新的业务信息并同步到ERP基础资料中）；2.整合工具包中的所有功能，形成一套文档；3.财务数据对接XBRL

这里的所有方法都是ERP早已实现的功能，因为资源限制没法通过采购来实现，单位的开发力量主要不用于支持财务，所以自力更生、特别擅长半自动处理成为了必备素质-_-#  

2020-3-13

银行对账问题有了一个当前所掌握技能条件下的最优解：pandas的groupby和merge方法。这个问题在sql下早已得到解决，即两张表根据一个或多个字段实现记录的一一对应。PS:pandas的merge_asof方法提供了模糊匹配的特性。比如按照交易发生时间匹配，可以手动设置容许的时间差，在这个delta_time范围内都可以实现匹配，超出则不能。  
  
  2022-1-24  
时隔差不多两年终于补上了使用频率较高的收入核销部分，为生成分录扫清了最后的障碍。原本认为可能有多对一，一对多，多对多多种情形，写到一半才发现多对多最终还得转换为一对多或者多对一来处理，所谓多对多完全就是个伪命题。由此可见`Divide & Conquer`是有前提的，分类本身是为了简化问题，不当的分类则适得其反。`Matching`的过程中顺带把明细冲销的信息取出来或者标记好，就足够生成分录了。

  2022-7-31  
调通了金蝶EAS凭证接口，包括且不限于凭证引入，凭证查询，凭证删除等等。基本扫清了纯python环境自动做账的主要障碍。

  2022-11-13  
写完了内网下载的一个初级方案，没有上多线程，没有完善下载后的文件处理，仅仅堪堪能降低一下年底的工作强度。  

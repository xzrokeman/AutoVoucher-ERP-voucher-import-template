from zeep import Client # zeep -V 4.1.0
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.xsd import *
from zeep import helpers
from zeep import wsdl
#optional: using logging module to record the xml sent and received
'''
import logging.config
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
        'zeep.Client': {
            'level': 'DEBUG', 
            'propagate': True, 
            'handlers': ['console'],
        }
    }
})
'''


transport = Transport(cache=SqliteCache(r"D:\easWsdlCache\wsdlCache.db"))
#wsdl file location: ~deployedIP~:[port number]/ormrpc/services/
client = Client(r'http://192.168.126.6:6890/ormrpc/services/EASLogin?wsdl', transport=transport)
'''
    金蝶EAS8.6
    @param userName 用户名	String
  	@param password 密码	String
    @param slnName eas		String #default to "eas"
    @param dcName 数据中心	String #in my case "t220412"
    @param language 语言	String #简体中文="L2" 繁体中文="L3"
    @param dbType 数据库类型	int #SQLSever=0 Oracle=1 DB2=2
    @param authPattern(String) 验证方式 #默认 "BaseDB" ; 其他认证方式KEY可从easAuthPatterns.xml中获取String
'''
result = client.service.login("user", "password", "eas", "t220412","L2", 1, "BaseDB", 0)
# type(result)-->zeep.objects.WSContext $Web Service Context, that's literally the echo from the server

transport = Transport(cache=SqliteCache(r"D:\Pylessons\CaseManager\easWsdlCache\wsdlCache.db"))
#wsdl file location: ~deployedIP~:[port number]/ormrpc/services/
client1 = Client(r'http://192.168.126.6:6890/ormrpc/services/WSWSVoucher?wsdl', transport=transport)
WSWSVoucher = client1.get_type('ns0:WSWSVoucher')#('ns1:ArrayOf_tns1_WSWSVoucher')#
params_ = WSWSVoucher()
for i in params_:
    params_[i] = SkipValue
    
def fill_form(param, line):
    for k, v in line.items():
        param[k] = v
    return param

lin_1 = {
    "companyNumber": "S01", 
    "bookedDate": "2022-1-1",
    "bizDate": "2022-1-1", 
    "periodYear": 2022, 
    "periodNumber": 1, 
    "voucherType": "记", 
    "voucherNumber": "S010002",
    "entrySeq": 1, 
    "voucherAbstract": "test", 
    "accountNumber": "6602.006", 
    "currencyNumber": "BB01", 
    "entryDC": 1,
    "originalAmount": 600.00, 
    "debitAmount": 600.00, 
    "creator": "user"
    }
lin_2 = {
    "companyNumber": "S01", 
    "bookedDate": "2022-1-1",
    "bizDate": "2022-1-1", 
    "periodYear": 2022, 
    "periodNumber": 1, 
    "voucherType": "记", 
    "voucherNumber": "S010002",
    "entrySeq": 2, 
    "voucherAbstract": "test", 
    "accountNumber": "1002", 
    "currencyNumber": "BB01", 
    "entryDC": 0,
    "originalAmount": 600.00, 
    "creditAmount": 600.00, 
    "creator": "user", 
    "asstSeq": 1,
    "asstActType1": "银行账户", 
    "asstActNumber1": "1002999002",
    "assistAbstract": "test"
    }

vouchCols_1 = fill_form(WSWSVoucher(),lin_1)
for i in vouchCols_1:
    if vouchCols_1[i] == None:
        vouchCols_1[i] = SkipValue
vouchCols_2 = fill_form(WSWSVoucher(),lin_2)
for i in vouchCols_2:
    if vouchCols_2[i] == None:
        vouchCols_2[i] = SkipValue
        
#client1.namespaces
mptyplaceholder = client1.get_type('ns1:ArrayOf_tns1_WSWSVoucher')
voucher = emptyplaceholder([])
voucher.append(vouchCols_1)
voucher.append(vouchCols_2)

with client1.settings(raw_response=True):
        response = client1.service.importVoucher(
        voucher, #vouchCols
        1,       #isTempSave
        0,       #isVerify
        0        #hasCashFlow
        )
        assert response.status_code == 200
        assert response.content
'''
<wsdl:operation name="importVoucher" parameterOrder="voucherCols isVerify isImpCashflow">
<wsdl:input message="impl:importVoucherRequest" name="importVoucherRequest"> </wsdl:input>
<wsdl:output message="impl:importVoucherResponse" name="importVoucherResponse"> </wsdl:output>
<wsdl:fault message="impl:WSInvokeException" name="WSInvokeException"> </wsdl:fault>
</wsdl:operation>
<wsdl:operation name="importVoucher" parameterOrder="voucherCols isTempSave isVerify hasCashflow">
<wsdl:input message="impl:importVoucherRequest1" name="importVoucherRequest1"> </wsdl:input>
<wsdl:output message="impl:importVoucherResponse1" name="importVoucherResponse1"> </wsdl:output>
<wsdl:fault message="impl:WSInvokeException" name="WSInvokeException"> </wsdl:fault>
</wsdl:operation>
'''
# for python does not support overloading like java, zeep automatically chose the latter method as the default "importVoucher" method
# there are workaround and discuss on zeep-github-issues

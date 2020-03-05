from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


from_addr = input("From: ")
password = input("Password: ")
to_addr = input("To: ")
smtp_server = input("SMTP server: ")

msg = MIMEText(
    "<html><body><p style='margin-top: 0' align='center'><div>发送时间：2019-10-16 11:50:35</div><div style='text-align:center;font-size:2em;'>十月--工资发放条</div></p><table border='1' cellspacing='0' bordercolordark='#ffffff' bordercolorlight='#800000'><tr bgcolor='lightblue'><td nowrap>人员编号</td><td nowrap>姓名</td><td nowrap>薪级</td><td nowrap>岗位工资</td><td nowrap>绩效工资</td><td nowrap>生活津贴</td><td nowrap>办案报酬</td><td nowrap>加班费</td><td nowrap>交通补助</td><td nowrap>独生子女费</td><td nowrap>补发工资</td><td nowrap>应发合计</td><td nowrap>代扣养老保险</td><td nowrap>代扣医疗保险</td><td nowrap>代扣住房公积金</td><td nowrap>代扣年金</td><td nowrap>代扣统筹医疗</td><td nowrap>代扣房租</td><td nowrap>代扣工会费</td><td nowrap>代扣税</td><td nowrap>税后补扣</td><td nowrap>扣款合计</td><td nowrap>实发合计</td></tr><tr><td nowrap>0087&nbsp;</td><td nowrap>张三&nbsp;</td><td nowrap>12&nbsp;</td><td nowrap>11,508.00&nbsp;</td><td nowrap>2,060.00&nbsp;</td><td nowrap>500.00&nbsp;</td><td nowrap>&nbsp;</td><td nowrap>&nbsp;</td><td nowrap>&nbsp;</td><td nowrap>&nbsp;</td><td nowrap>&nbsp;</td><td nowrap>14,068.00&nbsp;</td><td nowrap>920.64&nbsp;</td><td nowrap>230.16&nbsp;</td><td nowrap>2,190.12&nbsp;</td><td nowrap>10.00&nbsp;</td><td nowrap>&nbsp;</td><td nowrap>&nbsp;</td><td nowrap>30.00&nbsp;</td><td nowrap>165.45&nbsp;</td><td nowrap>&nbsp;</td><td nowrap>3,546.37&nbsp;</td><td nowrap>10,521.63&nbsp;</td></tr></table></body></html>",
    "html",
    "utf-8",
)
msg["From"] = _format_addr("Python爱好者 <%s>" % from_addr)
msg["To"] = _format_addr("管理员 <%s>" % to_addr)
msg["Subject"] = Header("工资条", "utf-8").encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

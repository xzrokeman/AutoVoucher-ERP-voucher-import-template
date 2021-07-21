import os, re, datetime
os.chdir(r"D:\\Pylessons\\20210625行政专项会议议题")
path_tuple=os.walk(os.getcwd(), topdown=True, onerror=None, followlinks=False)
#cwd= next(path_tuple)[0], next(path_tuple)[1]
#print(cwd, agenda)
cwd = os.getcwd()
meetingDate=re.search(r'\d{8}',cwd).group()

def dateInfo(mtDate):
    Yr = mtDate[:4]
    Mt = mtDate[4:6]
    D = mtDate[6:8]
    wkDay = dict(zip([x for x in range(1,8)], ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]))
    return {'year': int(Yr), 'month': int(Mt), 'day': int(D), 'weekday': wkDay[datetime.datetime.strptime(mtDate,"%Y%m%d").weekday()+1]}

agenda = next(path_tuple)[1]
#print(cwd, agenda, dateInfo(meetingDate))
#---------------------------------------------------------
#实验性功能，使用jinja2及相关库实现自动生成会议通知
from docxtpl import DocxTemplate #该库依赖jinja2
def agendaFormatter(ag):
    return ag.replace("《","<").replace("》",">").replace("议题","").replace("：关于","、研究《关于").replace("（汇报","》（汇报")

doc = DocxTemplate(r"D:\\Pylessons\\20210625行政专项会议议题\\t_template.docx")
enum = ['agenda'+str(i+1) for i in range(len(agenda))]
t_agenda = [agendaFormatter(i[1:]) for i in agenda]

context = dict({'x_agenda' : t_agenda}, **dateInfo(meetingDate))
#print(context)
doc.render(context)
doc.save(r"D:\\Pylessons\\20210625行政专项会议议题\\generated_doc.docx")

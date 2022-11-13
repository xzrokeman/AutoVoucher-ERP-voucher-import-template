# python 3.9.1
# selenium 4.6.0
# chromedriver 96.4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
# 打开浏览器
PATH = r"D:\Pylessons\scraper\chromedirver.exe"
driver = webdriver.Chrome(PATH)
actions = ActionChains(driver)
sleep(3)
#打开网页
driver.get("http://192.168.xxx.xxx/welcome/login")
sleep(2)
# 登录账号
try:
    username = WebDriverWait(driver, 0.5).until(
        EC.presence_of_element_located((By.ID, "code")))
    password = WebDriverWait(driver, 0.5).until(
        EC.presence_of_element_located((By.ID, "password")))
    username.send_keys("$username$")
    password.send_keys("$password$")
finally:
    buttons = driver.find_elements(by=By.TAG_NAME, value='input')
    for button in buttons:
        if button.accessible_name == '登录':
            button.send_keys(Keys.RETURN)
#driver.refresh()
sleep(2)
# 定位左侧导航frame并切换,HTML5以前支持的frame根据frameset的排布来配置页面布局
# 一个HTML下面有多个frameset，每个frameset有一个或多个frame，
# 以完成siderbar或者top navigation一类的布局。在selenium中frame和iframe被相同对待
# 一个frame/iframe代表一个单独的html文件（域），因此需要切换（switch_to）
frame = driver.find_element(By.ID, 'leftFrame')
driver.switch_to.frame(frame)
# driver.switch_to.default_content()

#点击跳转至所需功能页面
award_query = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.XPATH, '//td[text()="**书金额统计"]'))
)
award_query = driver.find_element(By.XPATH, '//td[text()="**书金额统计"]')
award_query.click()
sleep(1)
#重新定位mainFrame并切换
driver.switch_to.default_content()
main_frame = driver.find_element(By.ID, 'mainFrame')
driver.switch_to.frame(main_frame)
# 输入案号列表----------------------------------------------------------------------------
case_list = []

# 输入案号并查询/下载---------------------------------------------------------------------
# 由于该网站属于非HTML5的远古项目，frame在每次查询完成后会刷新，因此下一次下载需要重新获取元素
# 140个文件下载需要大约12分钟，如果更大量下载需要考虑上多线程
# 对于这个项目而言，文件排序也很重要
for i in case_list:
    case_code = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '//input[@id="hant_search_1_c_t_111"]')))
    submit = driver.find_element(By.XPATH, '//input[@type="submit"]')
    case_code.send_keys(i)
    submit.click()
    driver.find_element(By.XPATH, '//input[@value="下载"]').click()
    sleep(5)
# 关闭浏览器
sleep(10)
driver.quit()

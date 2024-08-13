import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 加载页面设置信息
def load_config():
    url = " /page/loadConfig"
    response = requests.get(url)
    print(response.text)


# 检查状态
def check_status():
    dr = ""
    url = f"https://portal.csu.edu.cn/drcom/chkstatus?callback={dr}"
    response = requests.get(url)
    print(response.text)


# 在线数据
def online_data(username, password):
    url = f"https://portal.csu.edu.cn:802/eportal/portal/Custom/online_data?username={username}&password={password}"
    response = requests.get(url)
    print(response.text)


# 登录认证
def login(username, password, type):
    net_types = {
        "中国电信": "telecomn",
        "中国移动": "cmccn",
        "中国联通": "unicomn",
        "校园网": "",
    }
    user_account = username + "@" + net_types[type]
    print("登陆账户：", user_account)
    url = f"https://portal.csu.edu.cn:802/eportal/portal/login?user_account={user_account}&user_password={password}"
    response = requests.get(url)
    if "已达上限" not in str(response.text): 
        return True
    else:    
        print(response.text)
        return False

# 解绑
def unbind(username):
    url = f"https://portal.csu.edu.cn:802/eportal/portal/mac/unbind?user_account={username}"
    response = requests.get(url)
    print(response.text)


# 退出
def logout():
    url = "https://portal.csu.edu.cn:802/eportal/portal/logout"
    response = requests.get(url)
    print(response.text)


def offline_one(account, password):
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    driver.get("http://202.197.54.218:4000/Self/login")
    driver.find_element(By.ID, "account").send_keys(account)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(
        By.CSS_SELECTOR, "#loginSet > div > div > form > div:nth-child(5) > button"
    ).click()
    # do whatever you want
    driver.get('http://202.197.54.218:4000/Self/dashboard')
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#OnlineLisBig > tbody > tr > td:nth-child(8) > a").click()
    time.sleep(2)
    
    driver.quit()
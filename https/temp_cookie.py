import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class UserInfo:
    def __init__(self, account, password):
        self.account = account
        self.password = password


class GetLoginDashboard:
    def __init__(self, userinfo):
        self.urls = {
            "login": "http://202.197.54.218:4000/Self/login",
            "dashboard": "http://202.197.54.218:4000/Self/dashboard",
            "onlineList": "http://202.197.54.218:4000/Self/dashboard/getOnlineList",
            "offline": "http://202.197.54.218:4000/Self/dashboard/tooffline",
        }
        self.userinfo = userinfo
        self.session = requests.Session()
        self.driver = webdriver.Chrome()
        self.cookies = {}

    def login(self):
        self.driver.get(self.urls["login"])
        username = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "account"))
        )
        # username = self.driver.find_element(By.ID, "account")
        username.send_keys(self.userinfo.account)
        password = self.driver.find_element(By.ID, "password")
        password.send_keys(self.userinfo.password)

        password.send_keys(Keys.RETURN)
        self.cookies = self.driver.get_cookies()[0]

    def get_dashboard(self):
        if self.cookies == {}:
            self.login()
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "cookie": self.cookies["name"] + "=" + self.cookies["value"],
            "host": "202.197.54.218:4000",
            "pragma": "no-cache",
            "proxy-connection": "keep-alive",
            "referer": "http://202.197.54.218:4000/Self/login/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }
        self.session.headers.update(headers)
        response = self.session.get(url=self.urls["dashboard"])

        with open("https/dashboard.html", "w") as f:
            f.write(response.text)

    def is_connected(self):
        try:
            # 尝试访问一个可靠的外部URL
            response = requests.get(
                "https://www.bilibili.com/",
                timeout=5,
                headers={
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
                },
            )
            # 如果状态码是200，表示请求成功
            return response.status_code == 200
        except requests.ConnectionError:
            # 捕获网络连接错误
            return False

    def adjust_online(self):
        if self.is_connected():
            print("already online")
            return
        else:
            self.offline_one()

    def offline_one(self):
        res = self.session.get(url=self.urls["onlineList"])
        online_list = res.json()
        if len(online_list) < 2:
            print(f"this is {len(online_list)} online devices")
            return

        statistics = {"#移动终端": [], "#PC": []}

        for device in online_list:
            statistics[device["terminalType"]].append(device["sessionId"])

        if len(statistics["#PC"]) == len(statistics["#移动终端"]):
            print("remove pc first")
            ret = self.session.get(
                url=self.urls["offline"], params={"sessionid": statistics["#PC"][0]}
            )
            if ret.json()["success"]:
                print("offline success")
            else:
                print("offline failed")
            return
        else:
            more_part = (
                statistics["#PC"]
                if len(statistics["#PC"]) > len(statistics["#移动终端"])
                else statistics["#移动终端"]
            )
            print("remove the more part")
            ret = self.session.get(
                url=self.urls["offline"], params={"sessionid": more_part[0]}
            )
        return

    def __del__(self):
        self.driver.quit()


import sys
import os

# 获取上级目录的路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# 将上级目录添加到sys.path
sys.path.append(parent_dir)
from self_info import account, password

if __name__ == "__main__":
    me = UserInfo(account=account, password=password)
    try_scrape = GetLoginDashboard(me)
    try_scrape.get_dashboard()
    try_scrape.adjust_online()

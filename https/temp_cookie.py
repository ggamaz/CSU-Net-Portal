import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UserInfo:
    def __init__(self, account, password):
        self.account = account
        self.password = password


class GetLoginDashboard:
    def __init__(self, userinfo):
        self.urls = {
            "login": "http://202.197.54.218:4000/Self/login",
            "dashboard": "http://202.197.54.218:4000/Self/dashboard",
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
        response = self.session.get(self.urls["dashboard"])
        with open("https/dashboard.html", "w") as f:
            f.write(response.text)

    def __del__(self):
        self.driver.quit()


if __name__ == "__main__":
    me = UserInfo("account", "password")
    try_scrape = GetLoginDashboard(me)
    try_scrape.get_dashboard()

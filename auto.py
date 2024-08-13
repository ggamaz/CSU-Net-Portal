import time
from portal import login, unbind, logout, offline_one


if __name__ == "__main__":

    # 配置
    username = '' #'8123456789' # 学号
    password = '' # 密码
    type = '中国联通' # 中国移动、中国联通、中国电信、校园网

    # 先解绑后自动登录
    unbind(username=username)
    logout()
    while login(username=username, password=password, type=type) == False:
        offline_one(username, password)
        time.sleep(1)
    print('login successfully!!')
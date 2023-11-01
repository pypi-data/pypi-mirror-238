import configparser
import logging
import time
import os

import requests

config = configparser.ConfigParser()


def timestamp():
    return int(time.time() * 1000)


class YunXiao:

    def __init__(self, configfile: str = "yunxiao_config.ini"):

        self.configfile = configfile

        # 如果没有初始化配置文件，抛出异常并终止程序
        if not os.path.exists(self.configfile):
            config['AUTH'] = {
                'phone': 'your_phone',
                'password': 'your_password',
                'token': '',
                'cookie': ''
            }
            with open(configfile, 'w') as f:
                config.write(f)
            logging.error(f"请访问 {configfile} 配置你的用户名和密码。")
            raise Exception("未初始化配置文件。请访问 {configfile} 配置你的用户名和密码。")

        # 读取配置文件
        config.read(self.configfile)
        self.token = config['AUTH']['token']
        self.cookie = config['AUTH']['cookie']
        self.user = config['AUTH']['phone']
        self.pwd = config['AUTH']['password']

        # 未填写配置时
        if self.user == "your_phone" or self.pwd == "your_password":
            logging.error(f"请访问 {configfile} 配置你的用户名和密码。")
            raise Exception("未初始化配置文件。请访问 {configfile} 配置你的用户名和密码。")

        # 初始化 token：为空则刷新一次。
        if not self.token or self.cookie:
            self.renew_auth()
            # self.renew_token()

        # # 初始化 cooke：为空则刷新一次。
        # if not self.cookie:
        #     self.renew_cookie()

    # 刷新 token
    def renew_auth(self):
        """
        刷新 token.tmp 配置中存储的 token
        """

        s = requests.Session()
        s.headers.update({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                        'like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76'})

        applogin = s.post(
                url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/loginByPhonePwd",
                json={"_t_": timestamp(), "password": self.pwd, "phone": self.user, "userType": 1}
            ).json()["data"]["token"]

        x3_authentication = s.get(
                url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/businessLogin",
                headers={"x3-authentication": applogin},
                params={"_t_": timestamp()}
            ).json()["data"]["token"]

        # 刷新 cookie

        weblogin = s.post(
            url="https://yunxiao.xiaogj.com/api/ua/login/password",
            params={"productCode": 1, "terminalType": 2, "userType": 1, "channel": "undefined"},
            json={"_t_": timestamp(), "clientId": "x3_prd", "password": self.pwd, "username": self.user,
                  "redirectUri": "https://yunxiao.xiaogj.com/web/teacher/#/home/0",
                  "errUri": "https://yunxiao.xiaogj.com/web/simple/#/login-error"},
            allow_redirects=False
        )

        weboauth2 = s.get(url=weblogin.json()["data"], allow_redirects=False)
        webcode = s.get(url=weboauth2.headers["location"], allow_redirects=False)
        webtoken = s.get(url=webcode.headers["location"], allow_redirects=False)

        cookie = f'UASESSIONID={weblogin.cookies.get("UASESSIONID")}; SCSESSIONID={webtoken.cookies.get("SCSESSIONID")}'

        s.close()

        self.token = x3_authentication
        self.cookie = cookie

        config.read(self.configfile)
        config['AUTH']['token'] = x3_authentication
        config['AUTH']['cookie'] = cookie

        with open(self.configfile, 'w') as f:
            config.write(f)

        logging.info("登录成功")

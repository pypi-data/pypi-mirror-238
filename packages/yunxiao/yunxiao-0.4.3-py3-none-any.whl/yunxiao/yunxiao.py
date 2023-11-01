import configparser
import logging
import httpx
import time
import os

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
        if not self.token:
            self.renew_token()

        # 初始化 cooke：为空则刷新一次。
        if not self.cookie:
            self.renew_cookie()

    # 刷新 token
    def renew_token(self):
        """
        刷新 token.tmp 配置中存储的 token
        """

        with httpx.Client(http2=True) as client:
            mid_token = client.post(
                url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/loginByPhonePwd",
                json={
                    "_t_": timestamp(),
                    "password": self.pwd,
                    "phone": self.user,
                    "userType": 1
                }
            ).json()["data"]["token"]

            token = client.get(
                url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/businessLogin",
                headers={"x3-authentication": mid_token},
                params={"_t_": timestamp()}
            ).json()["data"]["token"]

            config.read(self.configfile)
            config['AUTH']['token'] = token
            self.token = token
            with open(self.configfile, 'w') as f:
                config.write(f)

            logging.info("成功刷新 YUNXIAO_OAUTH_TOKEN")

    # 刷新 cookie
    def renew_cookie(self):
        """
        刷新 cookie.tmp 配置中存储的 cookie
        """
        # logging.debug("开始刷新 Cookie")
        with httpx.Client(http2=True, follow_redirects=False) as client:
            res = client.post(
                url="https://yunxiao.xiaogj.com/api/ua/login/password",
                params={
                    "productCode": 1,
                    "terminalType": 2,
                    "userType": 1,
                    "channel": "undefined"
                },
                json={
                    "_t_": timestamp(),
                    "clientId": "x3_prd",
                    "password": self.pwd,
                    "username": self.user,
                    "redirectUri": "https://yunxiao.xiaogj.com/web/teacher/#/home/0",
                    "errUri": "https://yunxiao.xiaogj.com/web/simple/#/login-error"
                }
            )

            res1 = client.get(url=res.json()["data"])

            cookie1 = "UASESSIONID=" + res.cookies["UASESSIONID"]
            cookie2 = "SCSESSIONID=" + res1.cookies["SCSESSIONID"]
            headers = {"cookie": cookie1 + "; " + cookie2}

            res2 = client.get(url=res1.headers["location"], headers=headers)

            res3 = client.get(url=res2.headers["location"], headers=headers)

            cookie3 = "SCSESSIONID=" + res3.cookies["SCSESSIONID"]

            cookie = cookie1 + "; " + cookie3

            config.read(self.configfile)
            config['AUTH']['cookie'] = cookie
            self.cookie = cookie
            with open(self.configfile, 'w') as f:
                config.write(f)

            logging.info("成功刷新 YUNXIAO_OAUTH_COOKIE")

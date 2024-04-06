import wenku8.data
from wenku8.user import data
import requests
from bs4 import BeautifulSoup
from typing import Any


class User:
    id = int()
    username = ''
    password = ''
    email = ''
    cookie = dict()
    promotion_link = str()
    nick = str()
    gender_type = ['保密', '男', '女']
    gender_id = 0

    def __init__(self, username='', password=''):
        self.username = username
        self.password = password

    def login(self) -> dict:
        """
        返回用户登录cookies
        :return cookies:
        """

        res = {
            "status": False,
            "info": "未知错误",
            "cookies": ""
        }

        login_url = wenku8.data.url + data.login_path
        cookies = {}

        session = requests.session()
        result = session.post(
            login_url,
            data={
                'username': self.username,
                "password": self.password,
                'usecookie': '315360000',
                'action': 'login',
                'submit': '%26%23160%3B%B5%C7%26%23160%3B%26%23160%3B%C2%BC%26%23160%3B'
            },
            headers=wenku8.data.header
        )
        # result.encoding = 'gbk'
        # print(result.text)
        text = result.text.encode('iso-8859-1').decode('gbk')
        if text.find('该用户不存在') != -1:
            res["info"] = "该用户不存在"
            return res
        if text.find("错误") != -1:
            res["info"] = "密码错误"
            return res
        for i, j in result.cookies.items():
            cookies[i] = j
        self.cookie = cookies
        # print(cookies)
        res["status"] = True
        res["info"] = "登录成功"
        res["user"] = user.__dict__
        return res

    def register(self) -> dict:
        """

        :return json{
            status
            info
        }:
        """
        res = {
            "status": False,
            "info": "未知错误"
        }
        # 检查用户名
        register_username_check_url = wenku8.data.url + data.username_check
        register_username_check_url = register_username_check_url.format(self.username)
        response = requests.get(
            url=register_username_check_url,
            headers=wenku8.data.header,
            timeout=10
        )
        if response.text.find('已注册') != -1:
            res["info"] = "该用户名已被注册"
            return res
        # 检查邮箱
        if self.email == '':
            res["info"] = "email未填写"
            return res
        register_email_check_url = wenku8.data.url + data.email_check
        register_email_check_url = register_email_check_url.format(self.email)
        response = requests.get(
            url=register_email_check_url,
            headers=wenku8.data.header,
            timeout=10
        )
        if response.text.find('格式错误') != -1:
            res["info"] = "email格式错误"
            return res
        if response.text.find('已注册') != -1:
            res["info"] = "email已被注册"
            return res
        # 注册
        register_url = wenku8.data.url + data.register_path
        response = requests.post(
            url=register_url,
            data={
                'username': self.username,
                'password': self.password,
                'repassword': self.password,
                'email': self.email,
                'sex': 0,
                "qq": "",
                "url": "",
                "action": "newuser",
                'submit': "%CC%E1+%BD%BB"
            },
            headers=wenku8.data.header
        )
        text = response.text.encode('iso-8859-1').decode('gbk')
        # print(text)
        if text.find('成功') != -1:
            res["info"] = "注册成功"
            res["status"] = True
        return res

    def check_cookie(self) -> bool:
        userinfo_url = wenku8.data.url + data.userinfo_path
        response = requests.get(
            url=userinfo_url,
            headers=wenku8.data.header,
            cookies=self.cookie,
            timeout=10,
            allow_redirects=False
        )
        if response.status_code != 200:
            return False
        return True

    def get_user_info(self) -> dict:
        res = {
            "status": False,
            "info": "未知错误",
            "user": None
        }
        if not self.check_cookie():
            res["info"] = "登录失败"
            return res
        userinfo_url = wenku8.data.url + data.userinfo_path
        response = requests.get(
            url=userinfo_url,
            headers=wenku8.data.header,
            cookies=self.cookie,
            timeout=10,
            allow_redirects=False
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', id='centerm')
        for i in content:
            content = [i.strip() for i in i.text.split('\n') if i.strip() != '']
            break
        for i, j in zip(content, range(0, len(content))):
            if i == '用户ID：':
                self.id = int(content[j + 1])
            elif i == '用户名：':
                self.username = content[j + 1]
            elif i == '昵称：':
                self.nick = content[j + 1]
            elif i == '性别：':
                self.gender_id = [i for i, x in enumerate(self.gender_type) if x == content[j + 1]][0]
            elif i == '推广链接：':
                self.promotion_link = content[j + 1]
        res["status"] = True
        res["info"] = "获取用户信息成功"
        res["user"] = self.__dict__

        return res


if __name__ == '__main__':
    # mqnu000 111111
    user = User()
    user.cookie = {
        "PHPSESSID": "c9d891f02890f49764254b173d7293ea",
        "jieqiUserInfo": "jieqiUserId%3D1423150%2CjieqiUserName%3Dmqnu000%2CjieqiUserGroup%3D3%2CjieqiUserVip%3D0%2CjieqiUserPassword%3D96e79218965eb72c92a549dd5a330112%2CjieqiUserName_un%3Dmqnu000%2CjieqiUserHonor_un%3D%26%23x65B0%3B%26%23x624B%3B%26%23x4E0A%3B%26%23x8DEF%3B%2CjieqiUserGroupName_un%3D%26%23x666E%3B%26%23x901A%3B%26%23x4F1A%3B%26%23x5458%3B%2CjieqiUserLogin%3D1712316462",
        "jieqiVisitInfo": "jieqiUserLogin%3D1712316462%2CjieqiUserId%3D1423150"
    }
    print(user.get_user_info())

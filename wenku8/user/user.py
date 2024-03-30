import wenku8.data
import data
import requests
from typing import Any


class User:
    username = ''
    password = ''
    email = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self) -> dict:
        """
        返回用户登录cookies
        :return cookies:
        """
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
        for i, j in result.cookies.items():
            cookies[i] = j
        # print(cookies)
        return cookies

    def register_info(self, email):
        self.email = email

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
            url=register_username_check_url,
            headers=wenku8.data.header,
            timeout=10
        )
        if response.text.find('格式错误') != -1:
            res["info"] = "email格式错误"
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
        with open('res.html', 'wb') as f:
            f.write(response.content)
        if response.text.find('成功'):
            res["info"] = "注册成功"
            res["status"] = True
        return res


if __name__ == '__main__':
    user = User('mqnu00', '111111')
    user.register_info('mqnu00@mqnu.com')
    print(user.register())

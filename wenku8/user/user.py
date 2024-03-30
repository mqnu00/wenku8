import wenku8.data
import data
import requests


class User:
    username = ''
    password = ''

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


    def register(self):
        pass



if __name__ == '__main__':
    user = User('mqnu', '0117mqnu')
    user.login()

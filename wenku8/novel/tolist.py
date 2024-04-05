import json
import re

import requests
from wenku8.novel.novel import Novel
from wenku8.user.user import User
from wenku8.novel import data
import wenku8.data
from bs4 import BeautifulSoup


class TopList:

    novel_list = list()
    type_id = int()
    type_name = str()
    user = User()
    total_page = int()

    def __init__(self, user: User=None, type_id: int=None):
        self.user = user
        self.type_id = type_id
        pass

    def get_all_list_type(self):
        toplist_url = wenku8.data.url + data.toplist_path
        toplist_url = toplist_url.format(data.toplist_type_en[0], 1)
        headers = wenku8.data.header
        response = requests.get(
            url=toplist_url,
            headers=wenku8.data.header,
            cookies=self.user.cookie,
            timeout=10
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        all_list_type = soup.find('ul', class_='ulcenter')
        res = []
        for i in all_list_type:
            text = i.text.split('\xa0')
            if len(text) > 1:
                res.append(text[0])
                res.append(text[-1])
        return res


    def get_info(self):
        pass


    def get_list(self):
        res = {
            "status": False,
            "info": "未知错误",
            "toplist": None
        }
        self.type_name = data.toplist_type_ch[self.type_id]
        toplist_url = wenku8.data.url + data.toplist_path
        toplist_url = toplist_url.format(data.toplist_type_en[self.type_id])
        response = requests.get(
            url=toplist_url,
            headers=wenku8.data.header,
            cookies=self.user.cookie,
            timeout=10
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        novel_list = soup.find('td')
        for cnt, content in zip(range(0, len(novel_list)), novel_list):
            if cnt % 2 == 0:
                continue
            novel_id = re.findall("\d+", content.a.get('href'))[0]
            novel = Novel(novel_id)
            novel.get_info()
            self.novel_list.append(novel)
        res["status"] = True
        res["info"] = "获取小说列表成功"
        # res["toplist"] = self.parser()
        print(res)

    def parser(self):
        res = {
            "type_id": self.type_id,
            "type_name": self.type_name,
            "novel_list": list()
        }
        for i in self.novel_list:
            res["novel_list"].append(i.__dict__)
        return res


if __name__ == '__main__':
    user = User()
    user.cookie = {
        "PHPSESSID": "c9d891f02890f49764254b173d7293ea",
        "jieqiUserInfo": "jieqiUserId%3D1423150%2CjieqiUserName%3Dmqnu000%2CjieqiUserGroup%3D3%2CjieqiUserVip%3D0%2CjieqiUserPassword%3D96e79218965eb72c92a549dd5a330112%2CjieqiUserName_un%3Dmqnu000%2CjieqiUserHonor_un%3D%26%23x65B0%3B%26%23x624B%3B%26%23x4E0A%3B%26%23x8DEF%3B%2CjieqiUserGroupName_un%3D%26%23x666E%3B%26%23x901A%3B%26%23x4F1A%3B%26%23x5458%3B%2CjieqiUserLogin%3D1712316462",
        "jieqiVisitInfo": "jieqiUserLogin%3D1712316462%2CjieqiUserId%3D1423150"
    }
    toplist = TopList(user, 0)
    toplist.get_list()

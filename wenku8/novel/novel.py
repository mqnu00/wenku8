import pprint
import urllib.parse

import requests
from wenku8.novel import data
from wenku8.util.util import encode_base64, xml_to_dict
import wenku8.data
from bs4 import BeautifulSoup
import json
import re


class Novel:
    id = int()
    name = str()
    author = str()
    description = str()
    pic_url = str()
    catalog = dict()
    status = str()
    update_time = str()
    all_length = str()
    # 每日点击数
    DayHitsCount = int()
    # 总收藏数
    FavCount = int()
    # 总推荐数
    PushCount = int()
    # 总点击数
    TotalHitsCount = int()

    def __init__(self, id: int = None):
        self.id = id

    def get_ident(self):
        # 访问小说主页
        novel_info_url = wenku8.data.url + data.info_path
        novel_info_url = novel_info_url.format(self.id)
        response = requests.get(
            url=novel_info_url,
            headers=wenku8.data.header,
            timeout=10
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        catalog_url = soup.find_all('a')
        for i in catalog_url:
            if i.text == '小说目录':
                catalog_url = wenku8.data.url + i['href']
                break
        return catalog_url.split('/')[4]

    def get_info(self) -> dict:

        res = {
            "status": False,
            "info": "未知错误",
            "novel": None
        }

        novel_info_url = wenku8.data.url + data.info_path
        novel_info_url = novel_info_url.format(self.id)
        response = requests.get(
            url=novel_info_url,
            headers=wenku8.data.header,
            timeout=10,
            allow_redirects=False
        )

        soup = BeautifulSoup(response.content, 'html.parser')

        # 判断错误
        error_tag = soup.find('div', class_='blocktitle')
        error_tag = error_tag.text
        if error_tag.find('错误') != -1:
            error_info = soup.find('div', class_='blockcontent')
            res["info"] = error_info.text.split('\n')[1]
            return res

        content = soup.find_all('tr')[2]
        content = [i for i in content.text.split('\n') if i.strip() != '']
        for i, j in enumerate(content):
            if i == 2:
                self.status = j.split('：')[1]
            elif i == 3:
                self.update_time = j.split('：')[1]
            elif i == 4:
                self.all_length = j.split('：')[1]

        # 获取小说简介
        novel_desc = soup.find_all('span')
        for i in range(0, len(novel_desc)):
            if str(novel_desc[i]).find('内容简介') != -1:
                #             print(i)
                self.description = novel_desc[i + 1].text
                break

        # 获取小说名和作者
        info_list = soup.find('title').text.split('-')
        # print(novel_desc)
        self.name = info_list[0].strip()
        self.author = info_list[1].strip()

        # 获取小说封面
        pic_url = str(soup.find_all('img')[1])
        pic_url = pic_url[pic_url.find("src") + 5:pic_url.find("jpg") + 3]
        self.pic_url = pic_url

        # 获取小说目录
        # self.get_catalog()

        # 获取小说推荐数据
        detail_url = data.detail_path
        detail_post = data.detail_post.format(self.id)
        response = requests.post(
            url=detail_url,
            data={
                "request": encode_base64(detail_post)
            },
            headers=wenku8.data.header
        )
        metadata = xml_to_dict(response.text)
        for i in metadata['metadata']['data']:
            if i['@name'] == 'DayHitsCount':
                self.DayHitsCount = int(i['@value'])
            elif i['@name'] == 'TotalHitsCount':
                self.TotalHitsCount = int(i['@value'])
            elif i['@name'] == 'PushCount':
                self.PushCount = int(i['@value'])
            elif i['@name'] == 'FavCount':
                self.FavCount = int(i['@value'])

        res["status"] = True
        res["info"] = "获取小说信息成功"
        res["novel"] = self.__dict__

        return res

    # 获取小说目录
    def get_catalog(self) -> dict:
        catalog = {
            "volume": str(),
            "chapter": list()
        }
        chapter = {
            "name": str(),
            "novel_id": int(),
            "chapter_id": int()
        }
        res = list()
        catalog_url = wenku8.data.url + data.catalog_path
        catalog_url = catalog_url.format(self.get_ident(), self.id)
        response = requests.get(
            url=catalog_url,
            headers=wenku8.data.header,
            timeout=10
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find_all('td')
        for i in content:
            if str(i).find('colspan') != -1:
                if catalog["volume"] != '':
                    res.append(catalog)
                    catalog = {
                        "volume": str(),
                        "chapter": list()
                    }
                catalog["volume"] = i.text

            elif i.a:
                chapter = {
                    "name": i.text,
                    "novel_id": self.id,
                    "chapter_id": re.findall("\d+", i.a.get('href'))[0]
                }
                catalog["chapter"].append(chapter)
            else:
                pass
        res.append(catalog)
        self.catalog = res
        return self.get_info()

    # 搜索小说
    def search(self, content: str, cookie: dict, page: int = 1):

        res = {
            "status": True,
            "info": "成功",
            "res": {
                "total_page": int(),
                "novel_list": list()
            }
        }

        search_url = wenku8.data.url + data.search_path
        search_url = search_url.format(
            str(content.encode(encoding='gb2312')).split('\'')[1].replace('\\x', '%').upper(),
            page
        )
        response = requests.post(
            url=search_url,
            headers=wenku8.data.header,
            cookies=cookie,
            timeout=10,
            allow_redirects=False
        )
        if response.status_code == 302:
            novel_list = [response.headers.get('Location').split('/')[-1].split('.')[0]]
            total_page = 1
        else:
            print(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            total_page = soup.find('em', id='pagestats').text.split('/')[-1]
            raw = soup.findAll('a')
            novel_list = []
            for i in raw:
                try:
                    link = str(i['href'])
                    raw = link.split('/')
                    if len(raw) > 2 and raw[1] == 'book':
                        novel_list.append(raw[2].split('.')[0])
                except KeyError:
                    pass
        res["res"]["total_page"] = total_page
        res["res"]["novel_list"] = novel_list
        return res


if __name__ == '__main__':
    novel = Novel()
    print(novel.search(
        # %BC%D3
        content='人',
        cookie={
            "PHPSESSID": "c9d891f02890f49764254b173d7293ea",
            "jieqiUserInfo": "jieqiUserId%3D1423150%2CjieqiUserName%3Dmqnu000%2CjieqiUserGroup%3D3%2CjieqiUserVip%3D0%2CjieqiUserPassword%3D96e79218965eb72c92a549dd5a330112%2CjieqiUserName_un%3Dmqnu000%2CjieqiUserHonor_un%3D%26%23x65B0%3B%26%23x624B%3B%26%23x4E0A%3B%26%23x8DEF%3B%2CjieqiUserGroupName_un%3D%26%23x666E%3B%26%23x901A%3B%26%23x4F1A%3B%26%23x5458%3B%2CjieqiUserLogin%3D1712316462",
            "jieqiVisitInfo": "jieqiUserLogin%3D1712316462%2CjieqiUserId%3D1423150"
        }
    ))

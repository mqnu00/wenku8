import requests
from wenku8.novel import data
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

    def __init__(self, id):
        self.id = id
        pass

    def get_info(self) -> dict:

        res = {
            "status": False,
            "info": "未知错误",
            "novel": None
        }

        if self.id == 0:
            res["info"] = "小说id缺失"

        novel_info_url = wenku8.data.url + data.info_path
        novel_info_url = novel_info_url.format(self.id)
        response = requests.get(
            url=novel_info_url,
            headers=wenku8.data.header,
            timeout=10
        )

        soup = BeautifulSoup(response.content, 'html.parser')

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
        catalog_url = catalog_url.format(self.id)
        print(catalog_url)
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


if __name__ == '__main__':
    novel = Novel()
    novel.id = 1973
    res = novel.get_catalog()
    print(res)

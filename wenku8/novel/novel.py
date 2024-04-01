import requests
from wenku8.novel import data
import wenku8.data
from bs4 import BeautifulSoup
import json


class Novel:
    id = int()
    name = str()
    author = str()
    description = str()
    pic_url = str()

    def __init__(self):
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

        res["status"] = True
        res["info"] = "获取小说信息成功"
        res["novel"] = json.dumps(self.__dict__, ensure_ascii=False)

        return res


if __name__ == '__main__':

    novel = Novel()
    novel.id = 1973
    print(novel.get_info())
import requests
import wenku8.data
from wenku8.novel import data
from bs4 import BeautifulSoup


class Chapter:

    novel_id = int()
    chapter_id = int()
    name = str()
    content = str()

    def __init__(self, novel_id, chapter_id):

        self.novel_id = novel_id
        self.chapter_id = chapter_id

    def get_content(self):
        chapter_url = wenku8.data.url + data.chapter_path
        chapter_url = chapter_url.format(self.novel_id, self.chapter_id)
        response = requests.get(
            url=chapter_url,
            headers=wenku8.data.header,
            timeout=10
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('div', id='title')
        self.name = title.text
        content = soup.find('div', id='content')
        self.content = content.text
        return self.__dict__


if __name__ == '__main__':
    chapter = Chapter(1973, '69567')
    chapter.get_content()
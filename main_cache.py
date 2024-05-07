from flask import Flask, request

from wenku8.novel.chapter import Chapter
from wenku8.novel.novel import Novel
from wenku8.novel.tolist import TopList
from wenku8.user.user import User
from cache import Cache

app = Flask(__name__)
cache = Cache(
    app=app,
    config={
    'CACHE_TYPE': 'simple',
    'REFRESH_TYPE': 'LFU',
    'ENABLE_TTL': True,
    'CACHE_THRESHOLD': 5,
    'CACHE_DEFAULT_TIMEOUT': 3
    }
)



@app.route('/login/', methods=['POST'])
def login():
    register_data = request.form
    user = User(register_data['username'], register_data['password'])
    return user.login()


@app.route('/register/', methods=['POST'])
def register():
    register_data = request.form
    user = User(register_data['username'], register_data['password'])
    user.email = register_data['email']
    return user.register()


@app.route('/user/detail/', methods=['POST'])
def userinfo():
    cookie = request.json
    user = User()
    user.cookie = cookie
    return user.get_user_info()


@app.route('/book/<int:id>/', methods=['GET'])
@cache.cached()
def get_novel_info(id):
    novel = Novel(id)
    return novel.get_info()


@app.route('/book/catalog/<int:id>/', methods=['GET'])
def get_novel_catalog(id):
    novel = Novel(id)
    return novel.get_catalog()


@app.route('/book/<int:novel_id>/<int:chapter_id>/', methods=['GET'])
def get_novel_chapter(novel_id, chapter_id):
    chapter = Chapter(novel_id, chapter_id)
    return chapter.get_content()


# 返回书籍列表类型
@app.route('/toplist/type/', methods=['GET'])
def get_toplist_type():
    toplist = TopList()
    return toplist.get_all_list_type()


# 返回书籍列表
@app.route('/toplist/', methods=['POST'])
def get_toplist():
    request_data = request.json
    toplist = TopList()
    toplist.user.cookie = request_data.get("cookie")
    toplist.type_id = request_data.get("type_id")
    toplist.request_page = request_data.get("request_page")
    return toplist.get_list()


if __name__ == "__main__":
    app.run(port=5000, host="127.0.0.1", debug=True)

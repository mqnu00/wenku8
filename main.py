from flask import Flask, request
from wenku8.user.user import User
from wenku8.novel.novel import Novel
from wenku8.novel.chapter import Chapter

app = Flask(__name__)


@app.route('/login/', methods=['POST'])
def login():
    register_data = request.form
    user = User(register_data['username'], register_data['password'])
    return user.login()


@app.route('/register/', methods=['POST'])
def register():
    register_data = request.form
    user = User(register_data['username'], register_data['password'])
    user.register_info(register_data['email'])
    return user.register()


@app.route('/book/<int:id>/', methods=['GET'])
def get_novel_info(id):
    novel = Novel()
    novel.id = id
    return novel.get_info()


@app.route('/book/catalog/<int:id>/', methods=['GET'])
def get_novel_catalog(id):
    novel = Novel()
    novel.id = id
    return novel.get_catalog()


@app.route('/book/<int:novel_id>/<int:chapter_id>/', methods=['GET'])
def get_novel_chapter(novel_id, chapter_id):
    print(novel_id, chapter_id)
    chapter = Chapter(novel_id, chapter_id)
    return chapter.get_content()


if __name__ == "__main__":
    app.run(port=5000, host="127.0.0.1", debug=True)

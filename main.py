from flask import Flask, request
from wenku8.user.user import User

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


if __name__ == "__main__":
    app.run(port=5000, host="127.0.0.1", debug=True)

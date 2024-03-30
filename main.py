from flask import Flask, request
from wenku8.user.user import User

app = Flask(__name__)


@app.route('/login/', methods=['POST'])
def index():
    register_data = request.form
    print(register_data)
    user = User(register_data['username'], register_data['password'])
    return user.login()


if __name__ == "__main__":
    app.run(port=5000, host="127.0.0.1", debug=True)

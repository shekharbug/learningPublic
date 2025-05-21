from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return "This is index page"

@app.route('/hello')
def hello():
    return "this is hello world"

@app.route('/search/')
def searching_users():
    return f'Searching for users'

@app.route('/search/<username>')
def get_user_info(username):
    return f'Username : {escape(username)}'


if __name__ == '__main__':
    app.run(debug=True)
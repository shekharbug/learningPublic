from flask import Flask, request, url_for, redirect
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "This is main page"

@app.route('/users/<username>', methods=['GET', 'POST'])
def get_user_info(username):
    return user_info(username)

def user_info(username):
    current_date = datetime.now()
    print(f'{username} current date: {current_date}')
    time.sleep(2)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
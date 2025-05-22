from flask import Flask, request, url_for, redirect
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "This is main page"

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
    # return "helping for login"

def show_the_login_form():
    return 'Show login form'

def do_the_login():
    return 'posting username and password'


if __name__ == '__main__':
    app.run(debug=True)
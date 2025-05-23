#!/usr/bin/env python3
#####################################################################
# filename  : testApp.py
# Author    : Shekhar
# Created   : 22-May-2025
# Version   : 1.0
# Description: 
# Reference Link: 
# History   : 
#####################################################################
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os # For generating a secret key
from db.dbOps import dbOps

app = Flask(__name__)
app.secret_key = os.urandom(24) 
USERS = {"admin": "admin123"}

@app.route('/')
def index():
    # If the user is already logged in, redirect to dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username') # Use .get() for safer access
        password = request.form.get('password')
        print(f'{username}')

        # Basic credential validation
        if username in USERS and USERS[username] == password:
            # Store username in session upon successful login
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            # Render the template again, potentially with the username pre-filled
            return render_template('login.html', username=username)
    
    # For GET requests, just render the login form
    return render_template('login.html')

def is_session_exists():
    # print(session.keys())
    if 'username' not in session:
        flash('Please log in to access this page.', 'info')
        return False
    return True

@app.route('/dashboard')
def dashboard():
    # Protect this route: only accessible if user is logged in
    if not is_session_exists():
        return redirect(url_for('login'))
    data = dbuser.show_all_users()
    return render_template('dashboard.html', data=data)

@app.route('/logout')
def logout():
    # Remove username from session
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/insert', methods=['GET', 'POST'])
def insert_user():
    if not is_session_exists():
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form.get('name') # Use .get() for safer access
        email = request.form.get('email')
        print(f'{username} {email}')
        dbuser.create_user(username=username, email=email)
        return  redirect(url_for('dashboard'))
    else:
        return render_template('insert.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if not is_session_exists():
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form.get('name') # Use .get() for safer access
        dbuser.delete_user(username=username)
        return redirect(url_for('dashboard'))
    else:
        return render_template('delete.html')


if __name__ == '__main__':
    dbuser = dbOps()
    app.run(debug=True, host='0.0.0.0', port=5000)
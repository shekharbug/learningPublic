import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session
from pyCode.dbOps import dbOps

# --- Configuration ---
app = Flask(__name__)
# IMPORTANT: Use a strong secret key in production
app.secret_key = 'your_super_secret_key_for_session_management' 
DATABASE = 'employee_manager.db'

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        userpwd = request.form['password']
        log.info(f'login user: {username}')
        if dbuser.validate_admin_password(username, userpwd):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
        
    log.info('Done with authentication')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    log.info('i m in dasbhord')
    sqlcmd = "select * from emp"
    emp_info = dbuser.run_sql(sqlcmd=sqlcmd, output=True)
    return render_template('dashboard.html', items=emp_info)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    log.debug('logout successful')
    return redirect(url_for('login'))

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    log.debug('in add user page')
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        emp_id = request.form['emp_id']
        emp_name = request.form['emp_name']
        salary = request.form['salary']
        join_date = request.form['join_date']
        data = (emp_id, emp_name, salary, join_date)
        for t_value in data:
            if not t_value:
                log.info('null value not allowed')
                return render_template('adduser.html')
        sqlcmd = "insert into emp values (?, ?, ?, ?)"
        dbuser.run_sql(sqlcmd=sqlcmd, commit=True, bind_var=data)
        log.info('Add user successful')
        return redirect(url_for('dashboard'))
    return render_template('adduser.html')

@app.route('/deluser', methods=['GET', 'POST'])
def deluser():
    log.debug('in add user deluser')
    return render_template('dashboard.html')

@app.route('/updateuser', methods=['GET', 'POST'])
def updateuser():
    log.debug('in add user updateuser')
    return render_template('dashboard.html')

if __name__ == '__main__':
    log = dbOps._set_logging()
    dbuser = dbOps()
    # Run the app
    app.run(debug=True)


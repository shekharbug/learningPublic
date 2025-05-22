from datetime import datetime
import mysql.connector as connector
from mysql.connector import Error

class dbOps:

    def __init__(self, dbname=None, dbhost=None, dbport=None, dbuser=None, dbpass=None):
        if not dbhost:
            self.dbhost = 'localhost'
        if not dbport:
            self.dbport = 3306
        if not dbuser:
            self.dbuser = 'app_user'
        if not dbname:
            self.dbname = 'my_app_db'
        if not dbpass:
            self.dbpass = 'app_password'
        self._db_connect()

    def _db_connect(self):
        self.connection = connector.connect(
            host = self.dbhost,
            database = self.dbname,
            user = self.dbuser,
            password = self.dbpass,
            port = self.dbport
        )
        self.sqlcursor = self.connection.cursor()
        # return sqlcursor
    

    def db_connection_close(self):
        self.connection.close()

    def run_sql(self, sqlsmt, commit=False, output=False):
        self.sqlcursor.execute(sqlsmt)
        output = self.sqlcursor.fetchall()
        if output:
            print(output)
        if commit:
            self.connection.commit()
            return True
        return output

    def is_user_exists(self, username):
        sqlsmt = f"select name, email from users where name='{username}'"
        return self.run_sql(sqlsmt, output=True)

    def create_user(self, username, email=None, age=None):
        print(f'checking user: {username}')
        user_found = self.is_user_exists(username=username)
        if len(user_found) >= 1:
            print(f'User {username} already exists')
            return True
        if not email:
            email = f"{username}@gamil.com"
        if not age:
            age = 32
        sqlsmt = f"insert into users (name, email, age) values('{username}', '{email}', '{age}')"
        self.run_sql(sqlsmt=sqlsmt, commit=True)
        self.is_user_exists(username=username)

    def delete_user(self, username):
        print(f'checking user: {username}')
        user_found = self.is_user_exists(username=username)
        if len(user_found) == 0:
            return f'User {username} already not exists'
        sqlsmt = f"delete from users where name='{username}'"
        self.run_sql(sqlsmt=sqlsmt, commit=True)
        return True

    def show_all_users(self):
        sqlsmt = "select id, name, email from users"
        return self.run_sql(sqlsmt, output=True) 
    




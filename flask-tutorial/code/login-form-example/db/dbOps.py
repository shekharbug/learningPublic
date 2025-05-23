#!/usr/bin/env python3
#####################################################################
# filename  : dbOps.py
# Author    : Shekhar
# Created   : 22-May-2025
# Version   : 1.0
# Description: 
# Reference Link: 
# History   : 
#####################################################################

from datetime import datetime
import mysql.connector as connector
from mysql.connector import Error
import os

class dbOps:

    def __init__(self, dbname=None, dbhost=None, dbport=None, dbuser=None, dbpass=None):
        if not dbhost:
            self.dbhost = os.environ.get('MYSQL_HOST', 'localhost')
        if not dbport:
            self.dbport = os.environ.get('MYSQL_PORT', '3306')
        if not dbuser:
            self.dbuser = os.environ.get('MYSQL_USER', 'app_user')
        if not dbname:
            self.dbname = os.environ.get('MYSQL_DATABASE', 'my_app_db')
        if not dbpass:
            self.dbpass = os.environ.get('MYSQL_PASSWORD', 'app_password')

    def __db_connect(self):
        connection = connector.connect(
            host = self.dbhost,
            database = self.dbname,
            user = self.dbuser,
            password = self.dbpass,
            port = self.dbport
        )
        return connection
    
    def db_connection_close(self):
        self.connection.close()

    def run_sql(self, sqlsmt, commit=False, output=False):
        with self.__db_connect() as connection:
            if connection and connection.is_connected():
                sqlcursor = connection.cursor()
                sqlcursor.execute(sqlsmt)
            if commit:
                connection.commit()
                return True
            output = sqlcursor.fetchall()
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
    

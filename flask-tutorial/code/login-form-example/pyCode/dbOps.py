#!/usr/bin/env python3
#####################################################################
# filename  : dbOps.py
# Author    : Shekhar
# Created   : 03-Dec-2025
# Version   : 1.0
# Description: 
# Reference Link: 
# History   : 
#####################################################################
import logging
import os
import sys
import sqlite3
from typing import Optional
import hashlib


class dbOps:

    def __init__(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        self.dbfile = os.path.join(current_dir, 'emp.db')
        # print(log)
        self.log = logging.getLogger()
        self.log.info('this is from class')
        self.is_db_open = False
        self.log.info(f'db file: {self.dbfile}')
        self.__create_table()


    def run_sql(self, sqlcmd, commit: bool = False, output: bool = False, sqlmany: bool=False, script: bool=False, bind_var: Optional[type] = None) -> list:
        """_summary_

        Args:
            sqlcmd (_type_): _description_
            commit (bool, optional): _description_. Defaults to False.
            output (bool, optional): _description_. Defaults to False.
            sqlmany (bool, optional): _description_. Defaults to False.
            script (bool, optional): _description_. Defaults to False.
            bind_var (tuple, optional): _description_. Defaults to None.

        Returns:
            list: list of sqloutput
        """
        sqlout = []
        self.log.info(f'sql command: {sqlcmd}')
        try:
            db = sqlite3.connect(self.dbfile)
            sql = db.cursor()

            if bind_var:
                if sqlmany:
                    sqlexec = sql.executemany(sqlcmd, bind_var)
                elif script:
                    sqlexec = sql.executescript(sqlcmd, bind_var)
                else:
                    sqlexec = sql.execute(sqlcmd, bind_var)
            else:
                if sqlmany:
                    sqlexec = sql.executemany(sqlcmd)
                elif script:
                    sqlexec = sql.executescript(sqlcmd)
                else:
                    sqlexec = sql.execute(sqlcmd)
            
            if output:
                sqlout = sqlexec.fetchall()
            
            if commit:
                db.commit()
            db.close()
        except Exception as e:
            print(f'Error found {e}')
            self.log.exception(e)
            sys.exit(1)
        return sqlout
    
    def __create_table(self) -> None:
        """create initial table
        """
        sqlcmd = """
            create table if not exists emp(
                id number,
                name,
                salary,
                join_date
            );

            create table if not exists auth(
                user,
                password
            );
        """
        self.run_sql(sqlcmd=sqlcmd, script=True)
        self.__create_admin_user()

    def __create_admin_user(self) -> None:
        """ Create admin user"""
        # check if user already exists.
        sqlcmd = "select user, password from auth"
        sqlout = self.run_sql(sqlcmd=sqlcmd, output=True)
        if len(sqlout) >= 1:
            self.log.debug('user already exists')
            return False
        
        userpwd = hashlib.sha256(b'admin').hexdigest()
        self.log.debug(f'initial password : {userpwd}')
        sqlcmd = "insert into auth values ('admin', ?)"
        self.run_sql(sqlcmd=sqlcmd, commit=True, bind_var=(userpwd,))
        return True
    
    def validate_admin_password(self, user: str, userpwd: str) -> bool:
        """validate admin password

        Args:
            user (str): username
            userpwd (str): user password

        Returns:
            bool: true if user validated
        """
        if user != 'admin':
            self.log.info(f'user: {user} is not admin user')
            return False
    
        self.log.debug(f'username: {user} password: {userpwd}')
        sqlcmd = "select user, password from auth where user=?"
        sqlout = self.run_sql(sqlcmd=sqlcmd, output=True, bind_var=(user,))
        self.log.debug(sqlout)
    
        for t_user, t_userpwd in sqlout:
            userpwd = bytes(userpwd, "utf-8")
            hashvalue = hashlib.sha256(userpwd).hexdigest()
            if t_userpwd == hashvalue:
                self.log.info('authentication successfull')
                print('authentication successfull')
                return True
        self.log.error('authentication : failed')
        return False



    @staticmethod
    def _set_logging(loglevel: int = 10) -> logging:
        """Setting log level
        Args:
            loglevel (int, optional): _description_. Defaults to 10.

        Returns:
            logging: _description_
        """
        logger = logging.getLogger()
        format = logging.Formatter('%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')
        logger.setLevel(loglevel)
        ch = logging.StreamHandler()
        ch.setFormatter(format)
        ch.setLevel(loglevel)
        logger.addHandler(ch)
        return logger
            
if __name__ == '__main__':
    log = dbOps._set_logging()
    dbuser = dbOps()
    dbuser.validate_admin_password('shekhar', 'admin')

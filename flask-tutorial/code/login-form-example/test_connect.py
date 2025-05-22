from db.dbOps import dbOps

if __name__ == '__main__':
    dbuser = dbOps()
    # dbuser.is_user_exists('shekhar')
    dbuser.create_user(username='rakhi')
    dbuser.create_user(username='shekhar')
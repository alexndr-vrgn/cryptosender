import pymysql.cursors
from configs.config_for_cryptobot import config as cfg

con = pymysql.connect(host=cfg.db_host,
                      user=cfg.db_user,
                      password=cfg.db_pass,
                      database=cfg.db_db,
                      cursorclass=pymysql.cursors.DictCursor)


def fetchdata(col):
    result = None
    try:
        with con.cursor() as cursor:
            sql = "SELECT `" + col + "` FROM `users_choice`"
            cursor.execute(sql)
            result = cursor.fetchone()
    except Exception as _ex:
        print(f'[INFO 1]: {_ex}')
    return result


def singup_user(user_id: int, user_name: str):
    try:
        with con.cursor() as cursor:
            sql = "INSERT INTO `users_choice` (`user_id`, `username`, `tokens`, `currency`, `period`) " \
                      "VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (user_id, user_name, '', '', 0))
        con.commit()
        result = 'Success'
    except Exception as _ex:
        print(f'[INFO 2]: {_ex}')
        result = 'Fail'
    return result


def update_data(col, change_list, user_id):
    try:
        with con.cursor() as cursor:
            sql = "UPDATE `users_choice` SET `" + col + "` = %s WHERE `user_id` = %s"
            cursor.execute(sql, (change_list, user_id))
        con.commit()
        result = 'Succes'
    except Exception as _ex:
        print(f'[INFO 3]: {_ex}')
        result = 'Fail'
    return result


def fetchone(col: str, user_id: int):
    result = None
    try:
        with con.cursor() as cursor:
            sql = "SELECT `" + col + "` FROM `users_choice` WHERE `user_id` = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
    except Exception as _ex:
        print(f'[INFO 4]: {_ex}')
    return result


def fetchall(user_id: int):
    result = None
    try:
        with con.cursor() as cursor:
            sql = "SELECT * FROM `users_choice` WHERE `user_id` = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
    except Exception as _ex:
        print(f'[INFO 5]: {_ex}')
    return result


def fetchme():
    result = None
    try:
        with con.cursor() as cursor:
            sql = "SELECT * FROM `users_choice`"
            cursor.execute(sql)
            result = cursor.fetchall()
    except Exception as _ex:
        print(f'[INFO 6]: {_ex}')
    return result
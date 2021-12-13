from datetime import datetime
from configs.config_for_cryptobot import config as cfg
from modules import request, prettify
import telebot
import time
import pymysql.cursors
import schedule

b = telebot.TeleBot(cfg.API_TOKEN)

con = pymysql.connect(host=cfg.db_host,
                      user=cfg.db_user,
                      password=cfg.db_pass,
                      database=cfg.db_db,
                      cursorclass=pymysql.cursors.DictCursor)


def ts():
    timestamp = datetime.now().strftime('%H:%M:%S')
    return timestamp

# Сделать функцию запроса данных у базы данных [fetchone]!
# Изменить первый запрос при регистрации.


@b.message_handler(commands=['start'])
def welcome_user(m):
    my_firstName = b.get_me()
    b.send_message(m.chat.id, f'Привет, меня зовут {my_firstName}!\nЯ создан для того, чтобы помочь тебе собирать '
                             f'информацию об интересующих монетах.\n\n Для начала тебе нужно настроить меня. Тебе '
                             f'предстоит выбрать необходимые монеты, валюту конвертации, а также как часто ты хочешь'
                             f'получать уведомления.')
    time.sleep(3)
    b.send_message(m.chat.id, 'Чтобы начать настройку выбери "/settings" в меню.')
    try:
        with con.cursor() as cursor:
            sql = "SELECT `user_id` FROM `users_choice`"
            cursor.execute(sql)
            result = cursor.fetchone()
        if result is None:
            with con.cursor() as cursor:
                sql = "INSERT INTO `users_choice` (`user_id`, `username`, `tokens`, `currency`, `period`) " \
                      "VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (m.from_user.id, m.from_user.first_name, '', '', 0))
            con.commit()
            print(ts() + ' [INFO]: Пользователь успешно добавлен!')
        elif result['user_id'] == m.from_user.id:
            print(ts() + ' [INFO]: Пользователь существует!')
        else:
            ex_ = 'Произошла ошибка во время выполнения запроса.'
            print(ts() + ' [INFO]: ' + ex_)
            b.send_message(m.chat.id, f'{ex_} Повторите попытку позже.')
    except Exception as _ex:
        print(ts() + f'[INFO 1]: Ошибка {_ex}')


@b.message_handler(commands=['settings'])
def initialise_settings(m):
    b.send_message(m.chat.id, 'Итак... Приступим!')
    time.sleep(2)
    b.send_message(m.chat.id, 'Загрузка...')
    time.sleep(2)
    b.edit_message_text('Напиши первую монету, которыю ты бы хотел добавить в избранное. Если она есть в моей базе'
                        'Я добавлю её автоматически.')
    b.register_next_step_handler(m, search_coin)


def search_coin(m):
    user_request = m.text
    if user_request.lower() == 'exit':
        # Сделать проверку добавленных монет.
        pass
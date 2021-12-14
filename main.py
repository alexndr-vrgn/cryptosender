from datetime import datetime
from configs.config_for_cryptobot import config as cfg
from modules import request, prettify, fetchone
import telebot
import time
import schedule

b = telebot.TeleBot(cfg.API_TOKEN)




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
    response_to_db = fetchone.fetchdata('user_id')
    if response_to_db is None:
        result = fetchone.singup_user(m.from_user.id, m.from_user.first_name)
        if result == 'Success':
            print('[INFO]: Пользователь успешно зарегистрирован!')
        elif result == 'Fail':
            print('[INFO]: Ошибка регистрации пользователя!')
        else:
            print('[INFO]: Ошибка -- повторите запрос позже!')
    elif response_to_db == m.from_user.id:
        print('[INFO]: Пользователь существует!')
    else:
        ex_ = 'Произошла ошибка во время выполнения запроса.'
        print(ts() + ' [INFO]: ' + ex_)
        b.send_message(m.chat.id, f'{ex_} Повторите попытку позже.')


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
        if fetchone.fetchone('tokens', m.from_user.id) is None or fetchone.fetchone('tokens', m.from_user.id)['tokens'] == 0:
            b.send_message(m.chat.id, "Очень жаль, что ты не добавил монеты. Возможно это произошло из-за ошибки.")
            time.sleep(1)
            b.send_message(m.chat.id, "Тебе придётся начать настройку(/settings) заново.")
        else:
            b.send_message(m.chat.id, "Отлично, монеты успешно добавлены!")
            time.sleep(1)
            b.send_message(m.chat.id, "Теперь выбери как часто ты хочешь получать уведомление.")
            time.sleep(1)
            b.send_message(m.chat.id, "Выбери временной диапазон:", reply_markup=gen_time_markup())
    else:
        for x in request.get_coin_names():
            if user_request == x['symbol'] or m.text.upper() == x['symbol']:
                slug = x['slug']
                req = fetchone.fetchone('tokens', m.from_user.id)['tokens']
                if req == '':
                    change_list = slug
                else:
                    fUser =

                fetchone.update_data('', change_list, m.from_user.id)
            else:
                b.send_message(m.chat.id, "Данная монета не найдена. Возможно её ранг слишком низок.")
                time.sleep(1)
                b.send_message(m.chat.id, "Попробуй ввести другую монету.")
        b.register_next_step_handler(m, search_coin)
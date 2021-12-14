from datetime import datetime
from configs.config_for_cryptobot import config as cfg
from modules import request, prettify, fetchone
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
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
        yourTokens = []
        for x in request.get_coin_names():
            if user_request == x['symbol'] or m.text.upper() == x['symbol']:
                slug = x['slug']
                req = fetchone.fetchone('tokens', m.from_user.id)['tokens']
                if req == '':
                    change_list = slug
                    b.send_message(m.chat.id, "Добавил монету " + user_request + " в Избранное.")
                else:
                    change_list = req + ',' + slug
                    for el in req:
                        if el == x['slug']:
                            uToken = x['symbol']
                            yourTokens.append(uToken)
                    b.send_message(m.chat.id, "Монеты в Избранном:\n" + ", ".join(yourTokens))
                    b.send_message(m.chat.id, 'Чтобы завершить добавление монет в избранное, напиши "exit"')
                fetchone.update_data('tokens', change_list, m.from_user.id)
            else:
                b.send_message(m.chat.id, "Данная монета не найдена. Возможно её ранг слишком низок.")
                time.sleep(1)
                b.send_message(m.chat.id, "Попробуй ввести другую монету.")
        b.register_next_step_handler(m, search_coin)


def gen_time_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("1 час", callback_data="time_1"),
               InlineKeyboardButton("6 часов", callback_data="time_6"),
               InlineKeyboardButton("12 часов", callback_data="time_12"),
               InlineKeyboardButton("24 часа", callback_data="time_24"))
    return markup


def gen_curr_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("USD", callback_data="curr_usd"),
               InlineKeyboardButton("BTC", callback_data="curr_btc"))
    return markup


@b.callback_query_handler(func=lambda call: True)
def callback_query_handle(call):
    user_id = call.from_user.id
    cid = call.message.chat.id
    col1 = 'period'
    col2 = 'currency'
    if call.data == 'time_1':
        timing = '1'
        fetchone.update_data(col1, timing, user_id)
        b.send_message(cid, "Отлично! Я буду присылать тебе уведомления каждый час!")
        b.edit_message_reply_markup(cid, message_id=call.message.message_id-1, reply_markup=None)
    elif call.data == 'time_6':
        timing = '6'
        fetchone.update_data(col1, timing, user_id)
        b.send_message(cid, "Отлично! Я буду присылать тебе уведомления каждые 6 часов!")
        b.edit_message_reply_markup(cid, message_id=call.message.message_id-1, reply_markup=None)
    elif call.data == 'time_12':
        timing = '12'
        fetchone.update_data(col1, timing, user_id)
        b.send_message(cid, "Отлично! Я буду присылать тебе уведомления каждые 6 часов!")
        b.edit_message_reply_markup(cid, message_id=call.message.message_id-1, reply_markup=None)
    elif call.data == 'time_24':
        timing = '24'
        fetchone.update_data(col1, timing, user_id)
        b.send_message(cid, "Отлично! Я буду присылать тебе уведомления каждые 6 часов!")
        b.edit_message_reply_markup(cid, message_id=call.message.message_id-1, reply_markup=None)
    b.send_message(cid, "Теперь выбери валюту в который будешь получать информацию:", reply_markup=gen_curr_markup())
    if call.data == 'curr_usd':
        curr = 'USD'
        fetchone.update_data(col2, curr, user_id)
        b.send_message(cid, "Сейчас я отправлю тебе первую информацию. С этого времени начнётся отсчёт.")
        b.edit_message_reply_markup(cid, message_id=call.message.message_id-1, reply_markup=None)
        sender(cid)
    elif call.data == 'curr_btc':
        curr = 'BTC'
        fetchone.update_data(col2, curr, user_id)
        b.send_message(cid, "Сейчас я отправлю тебе первую информацию. С этого времени начнётся отсчёт.")
        b.edit_message_reply_markup(cid, message_id=call.message.message_id-1, reply_markup=None)
        sender(cid)


def sender(chat_id):
    dataFromDb = fetchone.fetchall(chat_id)
    message = prettify.prettify(request.do_request(dataFromDb['tokens'], dataFromDb['currency']), dataFromDb['currency'])
    b.send_message(chat_id, '\n'.join(message))


def scheduler():
    dbData = fetchone.fetchme()
    for element in dbData:
        timing = element['period']
        user_id = element['user_id']
        schedule.every(timing).do(sender, user_id)
        while True:
            schedule.run_pending()
            time.sleep(1)


def send_one_message():
    b.send_message(1003228113, 'Здарова пидр, мы начинаем!')


@b.message_handler(commands=['rush'])
def rush_message(m):
    sender(m.chat.id)


scheduler()
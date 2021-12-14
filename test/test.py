import requests
from pprint import pprint
from fake_useragent import UserAgent
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from cryptosender.modules import fetchone
from configs.config_for_cryptobot import config as cfg

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
ua = UserAgent()


def do_request(slug, currency):
    answ = None
    parameters = {
        'slug': slug,
        'convert': currency
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': cfg.CMC_API
    }
    session = Session()
    session.headers.update(headers)

    try:
        r = session.get(url, params=parameters)
        answ = json.loads(r.text)
    except (ConnectionError, Timeout, TooManyRedirects) as _ex:
        print(f'[INFO]: Ошибка -- {_ex}')
    return answ


def prettify(request, curr):
    output = []
    for el in request['data'].items():
        symbol = el[1]['symbol']
        if curr == 'usd':
            price = str(round(el[1]['quote'][curr.upper()]['price'], 2)) + '$'
        else:
            price = str(el[1]['quote'][curr.upper()]['price']) + ' BTC'
        percent1H = round(el[1]['quote'][curr.upper()]['percent_change_1h'], 1)
        if percent1H > 0:
            percent1H = '+' + str(round(el[1]['quote'][curr.upper()]['percent_change_1h'], 1))
        percent24H = round(el[1]['quote'][curr.upper()]['percent_change_24h'], 1)
        if percent24H > 0:
            percent24H = "+" + str(round(el[1]['quote'][curr.upper()]['percent_change_24h'], 1))

        cap = str(round(el[1]['quote']['USD']['market_cap'], 1)) + '$'
        a = f'{symbol}: {price} ({percent1H}%) [{percent24H}%]\n Капитализация {symbol}: {cap}\n'
        output.append(a)
    return output


def first_sign():
    response_to_db = fetchone.fetchme()
    # if response_to_db is None or response_to_db[0]['user_id'] != m.from_user.id:
    #     result = fetchone.singup_user(m.from_user.id, m.from_user.first_name)
    #     if result == 'Success':
    #         print('[INFO]: Пользователь успешно зарегистрирован!')
    #     elif result == 'Fail':
    #         print('[INFO]: Ошибка регистрации пользователя!')
    #     else:
    #         print('[INFO]: Ошибка -- повторите запрос позже!')
    # elif response_to_db[0]['user_id'] == m.from_user.id:
    #     print('[INFO]: Пользователь существует!')
    # else:
    #     ex_ = 'Произошла ошибка во время выполнения запроса.'
    #     print(ts() + ' [INFO]: ' + ex_)
    #     b.send_message(m.chat.id, f'{ex_} Повторите попытку позже.')

first_sign()
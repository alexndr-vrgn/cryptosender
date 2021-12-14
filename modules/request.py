import requests
from fake_useragent import UserAgent
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
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


def get_coin_names():
    answer = []
    global response
    coins_url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=200&' \
                'sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false'
    header = { 'user-agent': f'{ua.random}'}
    try:
        r = requests.get(coins_url, headers=header)
        response = json.loads(r.text)
    except Exception as _ex:
        print(f'[INFO]: Ошибка -- {_ex}')
    for el in response['data']['cryptoCurrencyList']:
        topCoins = dict({el['symbol']: el['slug']})
        answer.append(topCoins)
    return answer
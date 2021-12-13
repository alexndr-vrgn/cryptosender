from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from configs.config_for_cryptobot import config as cfg

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


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

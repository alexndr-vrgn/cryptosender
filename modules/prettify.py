import babel.numbers as bn


def prettify(request, curr):
    output = []
    for el in request['data'][1].items():
        symbol = el['symbol']
        if curr == 'usd':
            price = bn.format_currency(round(el['quote'][curr.upper()]['price'], 2), 'USD', locale='en_US') + '$'
        else:
            price = el['quote'][curr.upper()]['price'] + ' BTC'
        percent1H = round(el['quote'][curr.upper()]['percent_change_1h'], 1)
        if percent1H < 0:
            percent1H = '+' + round(el['quote'][curr.upper()]['percent_change_1h'], 1)
        percent24H = round(el['quote'][curr.upper()]['percent_change_24h'], 1)
        if percent24H < 0:
            percent24H = "+" + round(el['quote'][curr.upper()]['percent_change_24h'], 1)

        cap = bn.format_currency(round(el['quote']['USD']['market_cap'], 1), 'USD', locale='en_US') + '$'
        a = f'{symbol}: {price} ({percent1H}%) [{percent24H}%]\n Капитализация {symbol}: {cap}\n'
        output.append(a)
    return output

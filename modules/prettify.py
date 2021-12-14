import babel.numbers as bn


def prettify(request, curr):
    output = []
    for el in request['data'].items():
        symbol = el[1]['symbol']
        if curr == 'usd' or curr == 'usd'.upper():
            price = str(bn.format_currency(round(el[1]['quote'][curr.upper()]['price'], 2), 'USD', locale='en_US')) + '$'
        else:
            price = str(el[1]['quote'][curr.upper()]['price']) + ' BTC'
        percent1H = round(el[1]['quote'][curr.upper()]['percent_change_1h'], 1)
        if percent1H > 0:
            percent1H = '+' + str(round(el[1]['quote'][curr.upper()]['percent_change_1h'], 1))
        percent24H = round(el[1]['quote'][curr.upper()]['percent_change_24h'], 1)
        if percent24H > 0:
            percent24H = "+" + str(round(el[1]['quote'][curr.upper()]['percent_change_24h'], 1))

        cap = str(bn.format_currency(round(el[1]['quote']['USD']['market_cap'], 0), 'USD', locale='en_US')) + '$'
        a = f'{symbol}: {price} ({percent1H}%) [{percent24H}%]\nКапитализация {symbol}: {cap}\n'
        output.append(a)
    return output

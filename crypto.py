import re
from decimal import Decimal

import discord
from pycoingecko import CoinGeckoAPI

import config


def symbol_generator(message):
    regex = "p\s(.+)+(\w\w\w)"
    symbol = re.search(regex, message).group(1)
    if symbol == 'eth':
        return 'ethereum'
    if symbol == 'btc':
        return 'bitcoin'
    if symbol == 'azero':
        return 'aleph-zero'
    if symbol == 'kas':
        return 'kaspa'
    if symbol == 'trtl':
        return 'turtlecoin'
    if symbol == 'lunc':
        return 'terra-luna'
    if symbol == 'luna':
        return 'terra-luna-2'
    if symbol == 'bcc':
        return 'bitconnect'
    if symbol == 'sol':
        return 'solana'
    else:
        return symbol


def price_normalize(price):
    if price >= float(10000):
        return "%0.1f" % price
    if float(1) <= price < float(10000):
        return "%0.2f" % price
    if float(0.1) <= price < float(1):
        return "%0.4f" % price
    if float(0.001) <= price < float(0.1):
        return "%0.6f" % price
    if float(0.00001) < price <= float(0.001):
        return "%0.8f" % price
    if float(0.0000001) < price < float(0.00001):
        return "%0.12f" % price
    else:
        return Decimal("%0.20f" % price).normalize()


def coingecko(message):
    cg = CoinGeckoAPI()
    regex = re.compile('p\s(.+)+(\w\w\w)')
    config.currency = re.search(regex, message).group(2)
    config.coin = symbol_generator(message)
    try:
        data = cg.get_coin_by_id(id=config.coin)
    except ValueError:
        return f'No such coin.'
    config.thumbnail = data['image']['thumb']
    try:
        price = data['market_data']['current_price'][config.currency]
    except KeyError:
        return f'No such currency.'
    config.price_in_usd = price_normalize(data['market_data']['current_price']['usd'])
    change = float(
        ("%0.2f" % (data['market_data']['price_change_percentage_24h_in_currency'][config.currency])).rstrip('0'))
    return f'{config.coin.upper()}\n'f'{price_normalize(price)} {config.currency.upper()} :green_square:+{change}%' if change > float(
        0) else f'{config.coin.upper()}\n{price_normalize(price)} {config.currency.upper()} :red_square:{change}%'


def real_time_price(message) -> str:
    p_message = message.lower()
    return coingecko(p_message)


async def response(message, user_message, username):
    answer = real_time_price(user_message)
    p = re.compile("(.+)\n(((.+(\.\d+|)))\s(\w\w\w))\s(.+)([\+|\-]\d+\.\d+\%)")
    if answer == 'No such coin.':
        embedVar = discord.Embed(title=f'Hi {username}, use format <cryptocurrency>+<currency> eg:',
                                 description=f'iotausd\niotabtc\nethereum-classicusd\nethereum-classicbtc',
                                 color=0x00ff00)
        await message.channel.send(embed=embedVar)
    if answer == 'No such currency.':
        embedVar = discord.Embed(title=f'Hi {username}, use format <cryptocurrency>+<currency> eg:',
                                 description=f'iotausd\niotabtc\nethereum-classicusd\nethereum-classicbtc',
                                 color=0x00ff00)
        await message.channel.send(embed=embedVar)
    else:
        result = p.search(answer)
    if result.group(6) != 'USD':
        versus = f'={config.price_in_usd}USD\ndata from coingecko'
    else:
        versus = "data from coingecko"
    embedVar = discord.Embed(title=f'{result.group(0)}', description=versus, color=0x00ff00)
    embedVar.set_thumbnail(url=config.thumbnail)
    await message.channel.send(embed=embedVar)


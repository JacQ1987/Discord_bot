import os

import discord

import convert
import crypto
import math_equations
import movie
import question
import search_engine
import texttospeech
import time_den
import translate
import weather


def run_discord_bot():

    token = os.environ['TOKEN']
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content.lower())
        channel = str(message.channel)
        

        if user_message == '!help':
            print(f'{username} said: {user_message} on {channel}')
            embedVar = discord.Embed(title=f'COMMANDS AVAILABALE:', description=f'', color=0xb43dc6).add_field(name='__**P <CRYPTO><CURRENCY>**__', value=f'**Lists crypto currency trading pairs from Coingecko.**\np iotausd\np iotaeur\np ethereum-classicusd\np ethererum-classiceur', inline=False).add_field(name='__**WEATHER <LOCATION>,<COUNTRY CODE(optional)>**__', value=f'**Real time weather information with temperature, humidity, min and max temp range.**\nweather singapore\nweather leuven\nweather denmark,DK', inline=False).add_field(name='__**FORECAST <LOCATION>,<COUNTRY CODE(optional)>**__', value=f'**Provides weather forecast for the next 5 days.**\nforecast singapore\nforecast leuven\nforecast denmark,dk', inline=False).add_field(name=f'__**Q <QUESTION>**__', value=f"**Query's the bot for answers to all kinds of questions. Answers may be in the form of a website or a direct answer.**\nq how long is average penis\nq population denmark", inline=False).add_field(name='__**G <QUERY>**__', value=f"**Lists Google's top 5 search results for a given query.**\ng iota\ng leonardo decaprio", inline=False).add_field(name='__**CONVERT <NUMBER><UNIT> TO <UNIT>**__', value=f'**Converts units**\nconvert 56km/h to miles/h\nconvert 6 lightyears to km\nconvert 6 inch to cm', inline=False).add_field(name='__**MOVIE <MOVIE NAME>**__', value=f"**Plot, runtime, ratings, year, director's name, casts names.**\nmovie shawshank redemption\nmovie avengers endgame\nmovie room in rome", inline=False).add_field(name='__**TIME <LOCATION>**__', value=f'**Provies the time in a particular location.**\ntime singapore\ntime leuven\ntime denmark,dk', inline=False).add_field(name='__**TRANSLATE <TEXT>**__', value=f'**Translates short texts to english. Sometimes more than one translation will be provided.**\ntranslate 去你妈的\ntranslate חַנְפָן\ntranslate Schlimste', inline=False).add_field(name='__**M <MATH equation>**__', value=f'**Solves math equations.**\nm 1+1\nm 5Log6Cos4', inline=False)
            await message.author.send(embed=embedVar)

        if user_message[0:2] == f'p ':
            print(f'{username} said: {user_message} on {channel}')
            await crypto.response(message, user_message, username)

        if user_message[0:8] == 'weather ':
            print(f'{username} said: {user_message} on {channel}')
            await weather.weather_response(message, user_message)

        if user_message[0:8] == 'forecast':
            print(f'{username} said: {user_message} on {channel}')
            await weather.forecast_response(message, user_message)

        if user_message[0:2] == 'g ':
            print(f'{username} said: {user_message} on {channel}')
            await search_engine.response(message, user_message, username)

        if user_message[0:2] == 'q ':
            print(f'{username} said: {user_message} on {channel}')
            await question.response(message, user_message)

        if user_message[0:8] == 'convert ':
            print(f'{username} said: {user_message} on {channel}')
            await convert.response(message, user_message)

        if user_message[0:5] == 'time ':
            print(f'{username} said: {user_message} on {channel}')
            await time_den.response(message, user_message)

        if user_message[0:2] == 'm ':
            print(f'{username} said: {user_message} on {channel}')
            await math_equations.response(message, user_message, username)

        if user_message[0:5] == 'movie':
            print(f'{username} said: {user_message} on {channel}')
            await movie.response(message, user_message, username)

        if user_message[0:10] == 'translate ':
            print(f'{username} said: {user_message} on {channel}')
            await translate.response(message, user_message)

        if user_message[0:4] == 'tts ':
            print(f'{username} said: {user_message} on {channel}')
            await texttospeech.response(message, user_message)


    client.run(token)

import re

import discord

import config
import scrape


def search(user_message):
    user_message = user_message.replace(" ", "+")
    url = f"https://www.google.com/search?q={user_message}&num=40"
    ans = scrape.google_output(url, 'div', config.google_search_class)
    return ans

async def response(message, user_message, username):
    try:
        regex_google = '(g)\s(.+)'
        answer = search(re.search(regex_google, user_message).group(2))
        embedVar = discord.Embed(title=f'Hi {username}, here are your top 5 search results for "{re.search(regex_google, user_message).group(2)}"', color=0xb43dc6).add_field(name=f'{answer[0][0]}', value=f'{answer[1][0]}', inline=False).add_field(name=f'{answer[0][1]}', value=f'{answer[1][1]}', inline=False).add_field(name=f'{answer[0][2]}', value=f'{answer[1][2]}', inline=False).add_field(name=f'{answer[0][3]}', value=f'{answer[1][3]}', inline=False).add_field(name=f'{answer[0][4]}', value=f'{answer[1][4]}', inline=False)
        await message.channel.send(embed=embedVar)
    except Exception as e:
        print(e)
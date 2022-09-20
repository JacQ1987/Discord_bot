import re

import discord
from imdb import Cinemagoer

import config
import scrape


def get_title_code(user_message):
    user_message = user_message.replace(" ", "+")
    url = f"https://www.google.com/search?q=IMDB+{user_message}"
    title_code = scrape.google_output(url, "div", config.movie_class)
    return title_code

def get_director(movie_directors):
    director_string = ', '.join(str(e) for e in movie_directors)
    # print(director_string)
    return director_string



def get_cast(movie_casts):
    cast_string = ', '.join(str(e) for e in movie_casts[0:10])
    # print(cast_string)
    return cast_string

def imdb(user_message):
    ia = Cinemagoer()
    code=get_title_code(user_message)
    movie_url = f'https://www.imdb.com/title/tt{code}/'
    movie_main_code = ia.get_movie_main(code)
    try:
        movie_name = movie_main_code['data']['localized title']
    except Exception:
        movie_name = "Movie mame unavailable"
    try:
        movie_plot = movie_main_code['data']['plot outline']
    except Exception:
        movie_plot = "No plot data available."
    try:
        movie_runtimes = f"{movie_main_code['data']['runtimes'][0]} min"
    except Exception:
        movie_runtimes = "No runtime data available"
    try:
        movie_cover_url = movie_main_code['data']['cover url']
    except Exception:
        movie_cover_url = ""
    try:
        movie_year = movie_main_code['data']['year']
    except Exception:
        movie_year = "No year data available"
    try:
        movie_ratings = f"{movie_main_code['data']['rating']}/10"
    except Exception:
        movie_ratings = "No rating data available."
    try:
        movie_director = get_director(movie_main_code['data']['director'])
    except Exception:
        movie_director = "No director data available."
    try:
        movie_casts = get_cast(movie_main_code['data']['cast'])
    except Exception:
        movie_casts = "No cast data available."
    return movie_runtimes, movie_cover_url, movie_year, movie_ratings, movie_director, movie_casts, movie_plot[0:250], movie_name, movie_url

async def response(message, user_message, username):
    try:
        regex_movie = '(movie)\s(.+)'
        answer = imdb(re.search(regex_movie, user_message).group(2))
        embedVar = discord.Embed(title=f'{answer[7].upper()}', description=f'{answer[6]}[...]', url=answer[8], color=0xb43dc6).add_field(name='Runtime:', value=f'{answer[0]}', inline=False).add_field(name='Rating:', value=f'{answer[3]}', inline=False).add_field(name='Year:', value=f'{answer[2]}', inline=False).add_field(name='Director(s):', value=f'{answer[4]}', inline=False).add_field(name='Casts:', value=f'{answer[5]}', inline=False)
        embedVar.set_thumbnail(url=answer[1])
        await message.channel.send(embed=embedVar)
    except Exception:
        embedVar = discord.Embed(title="Please input a valid argument.", color=0xb43dc6)
        await message.channel.send(embed=embedVar)
import json
import os
import re

import discord
import requests


def get_weather(user_message):
    # print(user_message)
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_message}&units=metric&appid="
                     f"{os.environ['OPEN_WEATHER_API_TOKEN']}")
    f = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={user_message}&units=metric&appid="
                     f"{os.environ['OPEN_WEATHER_API_TOKEN']}")
    data = r.text
    weather_data = json.loads(data)
    try:
      if weather_data["cod"] == "404":
        print('in 404 weather')
        title = f'There is no such place:'
        description = f'{user_message}'
        return title, description
    except Exception as e:
      print(e)
    title = f"Current weather for {weather_data['name']},{weather_data['sys']['country']}:flag_{(weather_data['sys']['country']).lower()}::"
    description = f"{(weather_data['weather'][0]['description']).capitalize()}.\n" \
                  f"Current temperature is {weather_data['main']['temp']}°C but feels like {weather_data['main']['feels_like']}°C " \
                  f"with {weather_data['main']['humidity']}% humidity.\n" \
                  f"Temperature range from {weather_data['main']['temp_min']}°C to {weather_data['main']['temp_max']}°C."
    return title, description


def get_forecast(user_message):
    f = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={user_message}&units=metric&appid="
                     f"{os.environ['OPEN_WEATHER_API_TOKEN']}")
    f_data = f.text
    weather_data = json.loads(f_data)
    if weather_data["cod"] == "404":
        title = f'There is no such place:'
        description = f'{user_message}'
        print(title, description)
        return title, description
    # pprint(weather_data)
    time_list = []
    temp_list = []
    weather_list = []
    city = weather_data['city']['name']
    country = weather_data['city']['country']
    # print(f"{weather_data['city']['coord']['lat']},{weather_data['city']['coord']['lon']}")
    try:
        for i in range(0,40):
            if i in (0,8,16,24,32):
                time = (weather_data['list'][i]['dt_txt']).split(' ')
                temp = weather_data['list'][i]['main']['temp']
                weather = weather_data['list'][i]['weather'][0]['description']
                # print(time, temp, weather)
                time_list.append(time)
                temp_list.append(temp)
                weather_list.append(weather)
            else:
                pass
    except Exception as e:
        print(e)

    title = f"{city}, {country}:flag_{country.lower()}:"
    return title, time_list, temp_list, weather_list

async def weather_response(message, user_message):
    try:
        regex = '(weather)\s(.+)'
        response = get_weather(re.search(regex, user_message).group(2))
        embedVar = discord.Embed(title=response[0], description=response[1], color=0x3D85C6)
        await message.channel.send(embed=embedVar)
    except Exception as e:
        print(e)


async def forecast_response(message, user_message):
    try:
        regex = '(forecast)\s(.+)'
        response = get_forecast(re.search(regex, user_message).group(2))
        embedVar = discord.Embed(title=response[0], color=0x3D85C6)\
            .add_field(name=f'{response[1][0][0]}', value=f'{response[2][0]}°C with {response[3][0]}', inline=False)\
            .add_field(name=f'{response[1][1][0]}', value=f'{response[2][1]}°C with {response[3][1]}', inline=False)\
            .add_field(name=f'{response[1][2][0]}', value=f'{response[2][2]}°C with {response[3][2]}', inline=False)\
            .add_field(name=f'{response[1][3][0]}', value=f'{response[2][3]}°C with {response[3][3]}', inline=False)\
            .add_field(name=f'{response[1][4][0]}', value=f'{response[2][4]}°C with {response[3][4]}', inline=False)
        await message.channel.send(embed=embedVar)
    except Exception as e:
        print(e)
    pass

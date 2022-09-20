import re

import config
import scrape


def time(user_message):
    url = f'https://www.google.com/search?q=time+{user_message.replace(" ", "+")}'
    ans = scrape.google_output(url, 'div', config.time_class)
    if ans == None:
        ans = f'Please input a valid place.'
    return ans

async def response(message, user_message):
    try:
        print('in time')
        regex_google = '(time)\s(.+)'
        answer = time(re.search(regex_google, user_message).group(2))
        await message.channel.send(f'```py\n{answer}```')
    except Exception as e:
        print(e)
import re

import config
import scrape


def convert(user_message):
    url = f'https://www.google.com/search?q=convert+{user_message.replace(" ", "+")}'
    answer = scrape.google_output(url, 'div', config.convert_id)
    return answer

async def response(message, user_message):
    try:
        regex = '(convert)\s(.+)'
        answer = convert(re.search(regex, user_message).group(2))
        await message.channel.send(f'```py\n{answer}```')
    except Exception as e:
        print(e)
import re

import config
import scrape


def math_ans(user_message, username):
    url = f'https://www.google.com/search?q={user_message.replace("+", "%2B")}'
    answer = scrape.google_output(url, "div", config.math_class)
    return answer


async def response(message, user_message, username):
    try:
        regex_google = '(m)\s(.+)'
        answer = math_ans(re.search(regex_google, user_message).group(2), username)
        await message.channel.send(f'```py\n{answer}```')
    except Exception:
        await message.channel.send(f'```py\nPlease enter a valid mathematical equation. Eg. 1+1, 5Log6```')
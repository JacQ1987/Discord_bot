import re

import discord

import config
import scrape


def question_ans(user_message):
  url = f'https://www.google.com/search?q={user_message.replace(" ", "+")}'
  ans = scrape.google_output(url, 'div', config.google_ans_class_1)
  return ans


async def response(message, user_message):
  try:
    regex_google = '(q)\s(.+)'
    answer = question_ans(re.search(regex_google, user_message).group(2))
    print(answer)
    if "https" in answer[0]:
      await message.channel.send(answer[0])
    else:
      # embedVar = discord.Embed(title=answer[0], color=0xb43dc6)
      await message.channel.send(f'```py\n{answer[0]}```')
  except Exception:
    embedVar = discord.Embed(title="I don't know the answer to that", color=0xb43dc6)
    await message.channel.send(embed=embedVar)



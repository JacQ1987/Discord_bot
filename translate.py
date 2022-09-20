import re

from bs4 import BeautifulSoup as bs
from google.cloud import translate_v2 as translate


def get_translation(text, input_lang, output_lang):
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=output_lang, source_language=input_lang)
    return bs(result["translatedText"], 'html.parser').text.capitalize()


def code_converter(lang):
    if lang == "zh-cn" or lang == "chinese" or lang == "mandarin" or lang == "chinese simplified":
        lang = "zh-CN"
    return lang


def language_code(lang):
    lang = code_converter(lang)
    translate_client = translate.Client()
    results = translate_client.get_languages()
    lang = [s['language'] for s in results if (s['name'] == lang.capitalize())] or [s['language'] for s in results if (s['language'] == lang)]
    if not lang:
        lang = ['']
        return lang[0]
    return lang[0]


async def response(message, user_message):
    regex = 'translate\s(.+)'
    error_message = f'```Please enter in the following syntax:\n' \
                    f'"(t\T)ranslate (string) -(output language)"\n' \
                    f'or\n' \
                    f'"(t\T)ranslate (string) (input language)-(output language)"```'
    try:
        user_message = re.match(regex, user_message).group(1)
    except Exception:
        await message.channel.send(error_message)
    subregex = '(.+)\s\+(\w+)|(.+)\s(\w+)\+(\w+)'
    regex_list = []
    try:
        for i in range(1, re.compile(subregex).groups + 1):
            regex_list.append(re.match(subregex, user_message).group(i))
        if (source_text := regex_list[2]):
            try:
                await message.channel.send(f'```{get_translation(source_text, language_code(regex_list[3]), language_code(regex_list[4]))}```')
            except Exception:
                await message.channel.send(error_message)
        else:
            await message.channel.send(f'```{get_translation(regex_list[0], "", language_code(regex_list[1]))}```')
    except Exception:
        try:
            await message.channel.send(f'```{get_translation(user_message, "", "en")}```')
        except Exception:
            await message.channel.send(message.channel.send(error_message))





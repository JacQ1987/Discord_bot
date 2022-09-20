import os
import re

import discord
from bs4 import BeautifulSoup as bs
from google.cloud import translate_v2 as translate


def get_translation(text, output_lang):
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=output_lang)
    return bs(result["translatedText"], 'html.parser').text, bs(result["detectedSourceLanguage"], 'html.parser').text


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
        lang = ''
        return lang
    return lang[0]

def text_to_speech(text, output_lang):
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    print(synthesis_input)

    voice = texttospeech.VoiceSelectionParams(
        language_code=output_lang, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(f"output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file "output.mp3"')

async def response(message, user_message):

    lang = None
    regex = 'tts\s(.+)'
    user_message = re.match(regex, user_message).group(1)
    sub_regex = '(.+)\s\+(.+)'
    try:
        sub_regex = '(.+)\s\+(.+)'
        lang = language_code(re.match(sub_regex, user_message).group(2))
    except Exception as e:
        print(e)
    if lang != None:
        text = get_translation(re.match(sub_regex, user_message).group(1), lang)[0]
        text_to_speech(text, lang)
    else:
        print('in else')
        lang = get_translation(user_message, 'en')[1]
        text = get_translation(user_message, lang)[0]
        text_to_speech(text, lang)

    await message.channel.send(file=discord.File(r'/home/jackpeh/output.mp3'))
    file_path = f'/home/jackpeh/output.mp3'
    os.remove(file_path)



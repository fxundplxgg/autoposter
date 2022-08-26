from datetime import datetime
import re
from urllib.parse import urlparse
import time
from config import FROM_CHANNELS, TO_CHANNELS, RUN_TITLE, LINK_FOR_REPL, EXCEPT_LINKS
from subprocess import call
import logging

try:
    from telethon import TelegramClient, events
    from colorama import Fore, Style
except:
    print("Установка нужных библиотек!")
    logging.debug("Установка нужных библиотек!")
    call(['pip3', 'install', 'telethon', 'colorama'])

credits = "Made By " + Fore.LIGHTRED_EX + Style.BRIGHT + "FXUNDPLXGG" + Fore.RESET + Style.NORMAL + '\n'

api_id = 6087612
api_hash = '1148dcdf0ec9b2e68e97b0fa104f14a4'
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s | %(message)s', datefmt='%I:%M:%S')

if RUN_TITLE:
    for ch in credits:
        time.sleep(0.03)
        print(ch, end='', flush=True)

client = TelegramClient('post', api_id, api_hash)
client.start()

print("Автопостер запущен!")

def get_current_time():
    return datetime.now().time().strftime("%H:%M:%S")

def repl_link(text, link_from, link_to):
    return text.replace(link_from, link_to)

def get_lnks_from_text(text):
    res = re.findall("(https?://\S+)", text)
    return res

@client.on(events.NewMessage(FROM_CHANNELS))
async def main(event):
    msg = event.message
    print(f"{get_current_time()} | Новый пост на канале {event.sender.title}!")

    print(f"{get_current_time()} | Замена ссылок!")

    if len(get_lnks_from_text(msg.message)) > 0:
        for link in get_lnks_from_text(msg.message):
            url = urlparse(link)
            url = url.scheme + "://" + url.netloc + "/"

            if url in EXCEPT_LINKS:
                for channel in TO_CHANNELS:
                    ch_entity = await client.get_entity(channel)

                    msg.message = repl_link(msg.message, link, LINK_FOR_REPL)

                    print(f"{get_current_time()} | Отправка поста на канал {ch_entity.title}!")
            
                    await client.send_message(ch_entity, msg)
    else:
        for channel in TO_CHANNELS:
                ch_entity = await client.get_entity(channel)
                print(f"{get_current_time()} | Отправка поста на канал {ch_entity.title}!")
                await client.send_message(ch_entity, msg)


client.run_until_disconnected()
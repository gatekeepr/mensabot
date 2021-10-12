# -*- coding: utf-8 -*-

import telegram
from telegram.ext import Updater
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import configparser
import schedule
import time

config = configparser.ConfigParser()
config.read("config.ini")

def timedMessage():
    simple = True
    text = (
        "Hauptmensa:"
        + "\n"
        + query(simple, haupt)
    )
    # print(text)
    bot.sendMessage(chat_id='@luhmensa', text=text)

# query the latest mensa plan for given url and specified information content
def query(simple, url):

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    seperator = "K:"
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (
        line.strip()
        for line in text.splitlines()
        if line.lstrip().startswith("#") or line.lstrip().startswith(">")
    )

    # remove everything in paranthesis
    if simple:
        lines = (re.sub("[\(\[].*?[\)\]]", "", line) for line in lines)

    # remove prices
    if simple:
        lines = (line.split(seperator, 1)[0] for line in lines)

    # rejoin the single lines to a complete string with backspaces
    text = "\n".join(lines)
    return text


# insert telegram bot token here
updater = Updater(config.get("DEFAULT", "telegram_token"))
bot = telegram.Bot(config.get("DEFAULT", "telegram_token"))
# mensa urls
haupt = config.get("DEFAULT", "hauptmensa_url")
markt = config.get("DEFAULT", "marktstand_url")

schedule.every().day.at("08:00").do(timedMessage)
timedMessage()

while(1):
    schedule.run_pending()
    time.sleep(60)
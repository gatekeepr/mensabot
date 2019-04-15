# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import urllib, re
from bs4 import BeautifulSoup
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

#query the latest mensa plan for given url and specified information content
def query(simple, url):

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html , features="html.parser")
    seperator = 'K:'
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines() if line.lstrip().startswith("#") or line.lstrip().startswith(">"))

    # remove everything in paranthesis
    if simple:
        lines = (re.sub("[\(\[].*?[\)\]]", "", line) for line in lines)

    # remove prices
    if simple:
        lines = (line.split(seperator, 1)[0] for line in lines)

    # rejoin the single lines to a complete string with backspaces
    text = '\n'.join(lines)

    return text

#trimmed version of the plan
def simple(bot, update):

    simple = True
    text = 'Hauptmensa:' + '\n' + query(simple, haupt) + '\n' + '\n' + 'Marktstand:' + '\n' + query(simple, markt)
    update.message.reply_text(text)

#full version including allergic notices
def full(bot, update):

    simple = False
    text = 'Hauptmensa:' + '\n' + query(simple, haupt) + '\n' + '\n' + 'Marktstand:' + '\n' + query(simple, markt)
    update.message.reply_text(text)

#only query the allergic information
def allergic(bot, update):
    url = haupt
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html , features="html.parser")
    seperator = 'K:'
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines() if not line.lstrip().startswith("#") and not line.lstrip().startswith(">"))

    # rejoin the single lines to a complete string with backspaces
    text = '\n'.join(lines)

    update.message.reply_text(text)

#insert telegram bot token here
updater = Updater(config.get('DEFAULT' , 'telegram_token'))

#mensa urls
haupt = config.get('DEFAULT' , 'hauptmensa_url')
markt = config.get('DEFAULT' , 'marktstand_url')

updater.dispatcher.add_handler(CommandHandler('simple', simple))
updater.dispatcher.add_handler(CommandHandler('full', full))
updater.dispatcher.add_handler(CommandHandler('allergic', allergic))

updater.start_polling()
updater.idle()

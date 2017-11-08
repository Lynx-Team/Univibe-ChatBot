import json
import requests
import time
import re
from enum import Enum
import urllib

from additionalCommand import unknownMessage, hiMessage, helpMessage
from subCommand import subMessage
from startCommand import startMessage
from sendCommand import sendMessage
from showTableCommand import showTableMessage

from dbconfig import cnxn

# Prod - "416840082:AAEtRo9zN67iYCu9rt815OIMohIdwmCPbbo"
# Test - "495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM"
TOKEN = "495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


class Command(Enum):
    HI = 1
    HELP = 2
    SUB = 3
    SEND = 4
    DEFINE = 5
    START = 6
    MYSUBS = 7
    MYNOT = 8
    KICK = 9
    SUBOUT = 10
    UNKNOWN = 11
    SHOWTABLE = 12


answerTable = {Command.HI: hiMessage, Command.UNKNOWN: unknownMessage, Command.HELP: helpMessage,
               Command.SUB: subMessage, Command.SEND: sendMessage, Command.START: startMessage,
               Command.SHOWTABLE: showTableMessage}

mod = "s"

import telebot
from telebot import types
bot = telebot.TeleBot("495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM")


@bot.message_handler(commands=["start"])
def cmd_start(message):
    # Создаем клавиатуру и каждую из кнопок (по 2 в ряд)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    url_button = types.InlineKeyboardButton(text="URL", url="https://ya.ru")
    callback_button = types.InlineKeyboardButton(text="Callback", callback_data="test")
    switch_button = types.InlineKeyboardButton(text="Switch", switch_inline_query="Telegram")
    keyboard.add(url_button, callback_button, switch_button)
    bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)

def handleMessage(text, userName):
    if (re.match(r'(.*п.*вет|ку|hi|хай|здра.*те)', text, flags=(re.IGNORECASE | re.MULTILINE))):
        return answerTable[Command.HI]()
    elif (re.match(r'^\s*(/help|help)\s*$', text)):
        return answerTable[Command.HELP]()
    elif (re.match(r'^\s*(/sub|sub)', text)):
        return answerTable[Command.SUB](text)
    elif (re.match(r'^\s*(send|/send).*$', text)):
        return answerTable[Command.SEND](userName, text)
    elif (re.match(r'^/start$',text)):
        return answerTable[Command.START]()
    elif (re.match(r'^(/st|st)$', text)):
        return answerTable[Command.SHOWTABLE](mod)
    else:
        return answerTable[Command.UNKNOWN]()

def createAnswer(updates):
    answerText = handleMessage(updates["message"]["text"])
    chat = updates["message"]["chat"]["id"]
    sendMessage(answerText, chat)

def sendMessage(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    getUrl(url)




# TEST FUNCTIONS

def getUrl(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def getJson(url):
    content = getUrl(url)
    js = json.loads(content)
    return js


def getUpdates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = getJson(url)
    return js


def createAnswerTest(updates):
    for update in updates["result"]:
        text = handleMessage(update["message"]["text"], update["message"]["chat"]["username"])
        chat = update["message"]["chat"]["id"]
        sendMessage(text, chat)


def getLastUpdateId(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)



def newUser(result):
    if (len(result) == 0):
        return

    result = result[0]

    first_name = result['message']['chat']['first_name']
    chat_id = result['message']['chat']['id']

    print(first_name, chat_id)

    # cursor = cnxn.cursor()
    # cursor.execute("SELECT * FROM teachers")
    #where dusers.user_login = N '" + first_name + "'")


    # if (not cursor.fetchone()):
    #     cursor.execute(
    #         "INSERT INTO dusers(user_login, user_password, last_news_id) values ('" + first_name + "', 'password', null)")
    #     cursor.commit()
    #
    # print(result)


def main():
    last_update_id = None
    # cursor = cnxn.cursor()
    # cursor.execute("SELECT * FROM teachers")
    # cursor.commit()
    #return

    cursor = cnxn.cursor()
    cursor.execute("SELECT username FROM AspNetUsers")

    row = cursor.fetchone()
    while row:
        print(str(row))
        row = cursor.fetchone()

    #return

    while True:
        updates = getUpdates(last_update_id)

        result = updates['result']
        #newUser(result)
        if len(result) > 0:
            last_update_id = getLastUpdateId(updates) + 1
            createAnswerTest(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    bot.polling(none_stop=True)

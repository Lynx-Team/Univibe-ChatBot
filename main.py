import json
import requests
import time
import re
from enum import Enum
import urllib
import random

import pyodbc

# Prod - "416840082:AAEtRo9zN67iYCu9rt815OIMohIdwmCPbbo"
# Test - "495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM"
TOKEN = "495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

server = 'univibe.database.windows.net'
database = 'UnivibeDB'
username = 'univibe'
password = 'Slasten32'
driver = '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


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

HiMEssages = ["И тебе привет", "Привет, чем могу помочь?", "Здравствуй"]

def hiMessage():
    return HiMEssages[random.randint(0,len(HiMEssages) - 1)]

def teacherFreeMessage(userName, userMessage):
    return "@" + userName + ":\n" + userMessage

def subMessage(userName):
    return "Вы подписались на " + userName


def helpMessage():
    return "/sub - Подписаться на рассылку пользователя \n /send \"Сообщение\" -  Отправить сообщение своим подписчикам"


def unknownMessage():
    return "Прости, я тебя не понял. Попробуй ввести команду точнее или узнай что я могу с помощью команды /help"


answerTable = {Command.HI: hiMessage(), Command.UNKNOWN: unknownMessage(), Command.HELP: helpMessage(),
               Command.SUB: subMessage, Command.SEND: teacherFreeMessage}


def handleMessage(text, userName):
    if (re.match(r'.*п.*вет', text, flags=(re.IGNORECASE | re.MULTILINE))):
        return answerTable[Command.HI]

    elif (re.match(r'^\s*(/help|help)\s*$', text)):
        return answerTable[Command.HELP]

    elif (re.match(r'^\s*(/sub|sub)', text)):
        userText = re.findall(r'sub\s*(.*)\s*$', text)
        if(userName[0] == ""):
            return "Вы должны ввести логин пользователя после команды sub"
        return answerTable[Command.SUB](userText[0])

    elif (re.match(r'^\s*send|/send.*$', text)):
        userText = re.findall(r'.*send\s+(.*)$', text)
        if (userText[0] == ""):
            return "Вы должны ввести сообщние после команды send"
        return answerTable[Command.SEND](userName, userText[0])
    else:
        return answerTable[Command.UNKNOWN]


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
    print(result)

    first_name = result['message']['chat']['first_name']
    chat_id = result['message']['chat']['id']

    print(first_name, chat_id)

    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM teachers")
    #where dusers.user_login = N '" + first_name + "'")


    if (not cursor.fetchone()):
        cursor.execute(
            "INSERT INTO dusers(user_login, user_password, last_news_id) values ('" + first_name + "', 'password', null)")
        cursor.commit()

    print(result)


def main():
    last_update_id = None
    # cursor = cnxn.cursor()
    # cursor.execute("SELECT * FROM teachers")
    # cursor.commit()
    #return

    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM teachers")

    row = cursor.fetchone()
    while row:
        print (str(row))
        row = cursor.fetchone()

    #return

    while True:
        updates = getUpdates(last_update_id)

        result = updates['result']
        #newUser(result)

        if len(result) > 0:
            last_update_id = getLastUpdateId(updates) + 1
            createAnswerTest(updates)
        time.sleep(0)

if __name__ == '__main__':
    main()
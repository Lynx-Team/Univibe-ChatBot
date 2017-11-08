import json
import requests
import time
import re
from enum import Enum
import urllib
import pyodbc

# Prod - "416840082:AAEtRo9zN67iYCu9rt815OIMohIdwmCPbbo"
# Test - "495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM"
TOKEN = "495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

server = 'univibe.database.windows.net'
database = 'UnivibeDB'
username = 'univibe'
password = 'Slasten32'
driver = '{SQL Server}'
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


class Command(Enum):
    HI = 1
    HELP = 2
    SUB = 3
    FREE = 4
    UNKNOWN = 5


def hiMessage():
    return "И тебе привет"


def teacherFreeMessage(userName):
    return "Преподователь " + userName + " готов вас принять"


def subMessage(userName):
    return "Вы подписались на " + userName


def helpMessage():
    return "/sub - подписаться на преподавателя \n /free - сказать о том что вы готовы принять"


def unknownMessage():
    return "Прости, я тебя не понял. Попробуй ввести команду точнее или узнай что я могу с помощью команды /help"


answerTable = {Command.HI: hiMessage(), Command.UNKNOWN: unknownMessage(), Command.HELP: helpMessage(),
               Command.SUB: subMessage, Command.FREE: teacherFreeMessage}


def handleMessage(text):
    if (re.match(r'.*П.*вет', text)):
        return answerTable[Command.HI]
    elif (re.match(r'^\s*(/help|help)\s*$', text)):
        return answerTable[Command.HELP]
    elif (re.match(r'^\s*(/sub|sub)', text)):
        userName = re.findall(r'sub\s*(.*)\s*$', text)
        return answerTable[Command.SUB](userName[0])
    elif (re.match(r'^\s*free|/free\s*$', text)):
        return answerTable[Command.FREE]("Какой-то")
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
        text = handleMessage(update["message"]["text"])
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
    cursor.execute("SELECT * FROM dusers where dusers.user_login = N'" + first_name + "'")

    if (not cursor.fetchone()):
        cursor.execute(
            "INSERT INTO dusers(user_login, user_password, last_news_id) values ('" + first_name + "', 'password', null)")
        cursor.commit()

    print(result)


def main():
    last_update_id = None
    # cursor = cnxn.cursor()
    # cursor.execute("Delete FROM dusers where dusers.id > 0")
    # cursor.commit()
    # return

    # cursor = cnxn.cursor()
    # cursor.execute("SELECT * FROM dusers")

    # row = cursor.fetchone()
    # while row:
    #     print (str(row))
    #     row = cursor.fetchone()

    # return

    while True:
        updates = getUpdates(last_update_id)

        result = updates['result']
        newUser(result)

        if len(result) > 0:
            last_update_id = getLastUpdateId(updates) + 1
            createAnswerTest(updates)
        time.sleep(0)
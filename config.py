import pyodbc
import telebot
from telebot import types

server = 'univibe.database.windows.net'
database = 'UnivibeDB'
username = 'univibe'
password = 'Slasten32'

driver = '{ODBC Driver 13 for SQL Server}'
import pyodbc
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

PATH_TO_API = 'http://univibeweb.azurewebsites.net/TelegramAccount/'


# Prod - "416840082:AAEtRo9zN67iYCu9rt815OIMohIdwmCPbbo"
# Test - "495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM"
TOKEN = "453267913:AAHqhlRIoOjG74uM0ugXZjRXtD8lSQmJbhA"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

ENTER_FIO = "Введите ФИО."

WHATLESSON = "Какая у меня пара?"
PROFILE = "Профиль"
SEND = "Отправить сообщение"

CHANGEMOD = "Изменить режим"
MYSP = "Мои подписки"
MYSPS = "Мои подписчики"
BACK = "Назад"

SUB = "Подписаться"

TTABLE = "Расписание преподавателя"
TSTUDENT = "Расписание Cтудента"

bot = telebot.TeleBot(TOKEN)
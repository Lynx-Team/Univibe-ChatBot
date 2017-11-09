import json
import time
import re
import copy
from enum import Enum
import urllib
from urllib.request import urlopen
from authFile import *
from urllib.parse import urlencode, quote
import requests
import datetime
from config import *
from whatLesson import *
import requests

views = []
global currentKeyBoard

def chekView(keyboard):
    if (len(views) == 0):
        views.append(keyboard)
        return
    if (views[len(views) - 1] != keyboard):
        print("ok")
        views.append(keyboard)

mod = 's'

@bot.message_handler(commands=["start"])
def start_state(message):
    print(message)

    print(message.chat.id)

    # cursor = cnxn.cursor()
    # res = requests.get(PATH_TO_API + )
    # cursor.execute("SELECT * from UnivibeDB.TelegramAccounts")
    # row = cursor.fetchone()
    #
    # while row:
    #     print(str(row))
    #     row = cursor.fetchone()

    #def startMessage(userId):
    isReg = urlopen(PATH_TO_API + 'IsRegistered/' + str(message.chat.id)).read().decode('utf-8')

    if (isReg == 'false'):
        print("kek")
        addNewUserId(message.chat.id)
        bot.send_message(message.chat.id, "Давайте познакомимся, придумайте свой логин и введите")
        print(message)







    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=WHATLESSON))
    keyboard.row_width = 2
    keyboard.add(types.KeyboardButton(text=PROFILE), types.KeyboardButton(text=SEND))

    chekView(keyboard)

    bot.send_message(message.chat.id, "Возможные действия:", reply_markup=keyboard)

@bot.message_handler(regexp=PROFILE)
def profile(message):
    print(message)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=CHANGEMOD))
    keyboard.row_width = 2
    keyboard.add(types.KeyboardButton(text=MYSP), types.KeyboardButton(text=MYSPS))
    keyboard.row_width = 1
    keyboard.add(types.KeyboardButton(text=BACK))

    chekView(keyboard)

    bot.send_message(message.chat.id, "Возможные действия:", reply_markup=keyboard)

@bot.message_handler(regexp=CHANGEMOD)
def profile(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=TTABLE), types.KeyboardButton(text=TSTUDENT))
    keyboard.row_width = 1
    keyboard.add(types.KeyboardButton(text=BACK))

    chekView(keyboard)

    bot.send_message(message.chat.id, "Выбирите режим просмотра расписания", reply_markup=keyboard)

@bot.message_handler(regexp=MYSP)
def profile(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=SUB), types.KeyboardButton(text=BACK))
    chekView(keyboard)
    bot.send_message(message.chat.id, "Возможные функции:", reply_markup=keyboard)

@bot.message_handler(regexp=BACK)
def profile(message):
    if(len(views) > 1):
        views.pop()
        bot.send_message(message.chat.id, "Назад", reply_markup=views[len(views) - 1])
    else:
        bot.send_message(message.chat.id, "Упс! Ошибка... Перезагрузите бота")

@bot.message_handler(regexp=TSTUDENT)
def profile(message):
    global mod
    mod = 's'
    bot.send_message(message.chat.id, "Теперь вы просматриваете расписание в режиме режиме студента")

@bot.message_handler(regexp=WHATLESSON)
def profile(message):
    bot.send_message(message.chat.id, sayAboutLesson(mod))

@bot.message_handler(regexp=TTABLE)
def profile(message):
    global mod
    mod = 't'
    bot.send_message(message.chat.id, "Теперь вы просматриваете расписание в режиме преподователя")


if __name__ == '__main__':
    global bot_state
    bot_state = 'none'
    bot.polling()
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
from sendCommand import *
from subCommand import subscribe_com
import requests

views = []
global currentKeyBoard
bot_state = 'none'

def chekView(keyboard):
    if (len(views) == 0):
        views.append(keyboard)
        return
    if (views[len(views) - 1] != keyboard):
        print("ok")
        views.append(keyboard)

mod = 's'

def default_btns(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=WHATLESSON))
    keyboard.row_width = 2
    keyboard.add(types.KeyboardButton(text=PROFILE), types.KeyboardButton(text=SEND))

    chekView(keyboard)

    bot.send_message(message.chat.id, "Возможные действия:", reply_markup=keyboard)

@bot.message_handler(regexp='^[^/].*')
def any_text(message):
    global bot_state

    if bot_state == 'sub':
        bot_state = 'none'
        subscribe_com(message)
    elif bot_state == 'send':
        sendMessage(message.text, message.chat.id, bot)
    elif bot_state == 'reg':
        bot_state = 'none'
        addNewUserId(message)
        default_btns(message)
    elif message.text == PROFILE:
        profile(message)
    elif message.text == CHANGEMOD:
        change_mod(message)
    elif message.text == MYSP:
        show_subscriptions(message)
    elif message.text == BACK:
        back(message)
    elif message.text == SUB:
        subscribe(message)
    elif message.text == TSTUDENT:
        profile_st(message)
    elif message.text == WHATLESSON:
        what_lesson(message)
    elif message.text == TTABLE:
        profile_tch(message)
    elif message.text == SEND:
        send_Mess(message)

@bot.message_handler(commands=["start"])
def start_state(message):
    global bot_state
    isReg = urlopen(PATH_TO_API + 'IsRegistered/' + str(message.chat.id)).read().decode('utf-8')

    if (isReg == 'false'):
        bot.send_message(message.chat.id, "Давайте познакомимся, придумайте свой логин и введите")
        bot_state = 'reg'
    else:
        default_btns(message)

def profile(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=CHANGEMOD))
    keyboard.row_width = 2
    keyboard.add(types.KeyboardButton(text=MYSP), types.KeyboardButton(text=MYSPS))
    keyboard.row_width = 1
    keyboard.add(types.KeyboardButton(text=BACK))

    chekView(keyboard)

    bot.send_message(message.chat.id, "Возможные действия:", reply_markup=keyboard)

def change_mod(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=TTABLE), types.KeyboardButton(text=TSTUDENT))
    keyboard.row_width = 1
    keyboard.add(types.KeyboardButton(text=BACK))

    chekView(keyboard)

    bot.send_message(message.chat.id, "Выбирите режим просмотра расписания", reply_markup=keyboard)

def show_subscriptions(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=SUB), types.KeyboardButton(text=BACK))
    chekView(keyboard)
    bot.send_message(message.chat.id, "Возможные функции:", reply_markup=keyboard)

def back(message):
    if(len(views) > 1):
        views.pop()
        bot.send_message(message.chat.id, "Назад", reply_markup=views[len(views) - 1])
    else:
        bot.send_message(message.chat.id, "Упс! Ошибка... Перезагрузите бота")

def subscribe(message):
    global bot_state
    bot_state = 'sub'
    bot.send_message(message.chat.id, "Введите логин пользователя, на которого вы хотите подписаться.")

def send_Mess(message):
    global bot_state
    bot_state = 'send'
    bot.send_message(message.chat.id, "Введите сообщение для рассылки")

def profile_st(message):
    global mod
    mod = 's'
    bot.send_message(message.chat.id, "Теперь вы просматриваете расписание в режиме режиме студента")

def what_lesson(message):
    bot.send_message(message.chat.id, sayAboutLesson(mod))

def profile_tch(message):
    global mod
    mod = 't'
    bot.send_message(message.chat.id, "Теперь вы просматриваете расписание в режиме преподователя")

bot.polling()
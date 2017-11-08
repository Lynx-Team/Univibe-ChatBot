import json
import time
import re
import copy
from enum import Enum
import urllib
import telebot
from telebot import types
from urllib.request import urlopen
from urllib.parse import urlencode, quote
import requests
from dbconfig import PATH_TO_API

from additionalCommand import unknownMessage, hiMessage, helpMessage
from subCommand import subMessage
from startCommand import startMessage
from sendCommand import sendMessage
from showTableCommand import showTableMessage

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

def whatLesson():
    return "Алгебра"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(regexp='^[^/].*')
def any_text(message):
    global bot_state
    if bot_state == 'fio':
        bot_state = 'none'
        requests.get(PATH_TO_API + 'SetFIO/' + str(message.chat.id) + '/' + message.text)
        start_state(message)

def start_state(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    global pervKeyBoard
    global currentKeyBoard

    keyboard.add(types.KeyboardButton(text=WHATLESSON))
    keyboard.row_width = 2
    keyboard.add(types.KeyboardButton(text=PROFILE), types.KeyboardButton(text=SEND))
    currentKeyBoard = keyboard
    pervKeyBoard = keyboard

    bot.send_message(message.chat.id, "Возможные действия:", reply_markup=keyboard)

@bot.message_handler(commands=["start"])
def mainMenu(message):
    global bot_state
    if startMessage(message.chat.id):
        bot_state = 'fio'
        bot.send_message(message.chat.id, "Введите свои ФИО.")
    else:
        start_state(message)

@bot.message_handler(regexp=PROFILE)
def profile(message):
    global pervKeyBoard
    global currentKeyBoard
    print(message)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=CHANGEMOD))
    keyboard.row_width = 2
    keyboard.add(types.KeyboardButton(text=MYSP), types.KeyboardButton(text=MYSPS))
    keyboard.row_width = 1
    keyboard.add(types.KeyboardButton(text=BACK))

    pervKeyBoard = currentKeyBoard
    currentKeyBoard = keyboard

    bot.send_message(message.chat.id, "Возможные действия:", reply_markup=keyboard)

@bot.message_handler(regexp=SEND)
def profile(message):
    bot.send_message(message.chat.id, "Введите сообщение для рассылки")

@bot.message_handler(regexp=CHANGEMOD)
def profile(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=TTABLE), types.KeyboardButton(text=TSTUDENT))
    keyboard.add(types.KeyboardButton(text=BACK))
    bot.send_message(message.chat.id, "Выбирите режим просмотра расписания", reply_markup=keyboard)

@bot.message_handler(regexp=MYSP)
def profile(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=SUB), types.KeyboardButton(text=BACK))
    bot.send_message(message.chat.id, "Возможные функции:", reply_markup=keyboard)

@bot.message_handler(regexp=SUB)
def profile(message):
    bot.send_message(message.chat.id, "Введите логин пользователя")

@bot.message_handler(regexp=BACK)
def profile(message):
    global pervKeyBoard
    global currentKeyBoard
    bot.send_message(message.chat.id, "Назад", reply_markup=pervKeyBoard)
    pervKeyBoard = currentKeyBoard
    currentKeyBoard = pervKeyBoard


if __name__ == '__main__':
    global bot_state
    bot_state = 'none'
    bot.polling()
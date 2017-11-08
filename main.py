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



WHATLESSON = "Какая у меня пара?"
PROFILE = "Профиль"
SEND = "Отправить сообщение"

CHANGEMOD = "Изменить режить"
MYSP = "Мои подписки"
MYSPS = "Мои подписчики"
BACK = "Назад"

SUB = "Подписаться"

TTABLE = "Расписание преподавателя"
TSTUDENT = "Расписание Cтудента"

def whatLesson():
    return "Алгебра"

import telebot
from telebot import types
bot = telebot.TeleBot("495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test":
            bot.send_message(call.message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)

@bot.message_handler(commands=["start"])
def mainMenu(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=WHATLESSON))
    keyboard.row_width = 2
    keyboard.add(types.KeyboardButton(text=PROFILE), types.KeyboardButton(text=SEND))
    #bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)

@bot.message_handler(regexp=PROFILE)
def profile(message):
    print(message)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=CHANGEMOD))
    keyboard.row_width = 2
    keyboard.add(types.KeyboardButton(text=MYSP), types.KeyboardButton(text=MYSPS))
    keyboard.row_width = 1
    keyboard.add(types.KeyboardButton(text=BACK))


# @bot.message_handler(content_types=["text"])
# def any_msg(message):
#     if(message.text == Command.WHATLESSON):
#         bot.send_message(message.chat.id, message.text)
#     if (message.text == Command.SEND):
#         bot.send_message(message.chat.id, message.text)
#     if (message.text == Command.PROFILE):
#         bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)

import re
from main import *

@bot.message_handler(regexp=SUB)
def profile(message):
    bot.send_message(message.chat.id, "Введите логин пользователя")
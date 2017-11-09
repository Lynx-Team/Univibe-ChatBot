import re
from main import *
def sendMessage(userName, text):
    userText = re.findall(r'.*send\s*(.*)$', text)
    if (userText[0] == ""):
        return "Вы должны ввести сообщние после команды send"
    return "@" + userName + ":\n" + userText[0]

@bot.message_handler(regexp=SEND)
def profile(message):
    bot.send_message(message.chat.id, "Введите сообщение для рассылки")
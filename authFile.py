from urllib.request import urlopen
from config import *

def addNewUserId(message):
    urlopen(PATH_TO_API + 'RegisterTelegram/' + str(message.chat.id))
    cursor = cnxn.cursor()
    cursor.execute('UPDATE TelegramUsers SET UserLogin = \'' + message.text + '\' WHERE TelegramID = \'' + str(message.chat.id) + '\';')
    cnxn.commit()
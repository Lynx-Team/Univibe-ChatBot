import re
from main import *

def subscribe(message):
    userId = message.chat.id
    subToLogin = message.text
    cursor = cnxn.cursor()

    cursor.execute('SELECT TelegramID FROM TelegramUsers WHERE UserLogin = ' + subToLogin)
    isExist = cursor.fetchall()[0]
    if (isExist == 'None'):
        return

    cursor.execute('SELECT Subscribers FROM TelegramUsers WHERE UserLogin = ' + subToLogin)
    userSubs = cursor.fetchall()[0]
    cursor.execute('SELECT UserLogin FROM TelegramUsers WHERE TelegramID = ' + userId)
    userLogin = cursor.fetchall()[0]
    userSubs += ',' + userLogin 

    cursor.execute('SELECT Subscriptions FROM TelegramUsers WHERE TelegramID = ' + userId)
    userSubs = cursor.fetchall()[0]
    userSubs += ',' + subToLogin
    cursor.execute('UPDATE TelegramUsers SET Subscriptions = "' + userSubs + '" WHERE TelegramID = ' + userId)
    cursor.fetchall()

from config import *

def sendMessage(messgeForSale, id, bot):
    cursor = cnxn.cursor()
    cursor.execute("SELECT Subscribers FROM TelegramUsers WHERE TelegramID = '" + str(id) + "'")
    subscribers = str(cursor.fetchall()[0][0]).split(',')
    for sub in subscribers:
        cursor.execute("SELECT TelegramID FROM TelegramUsers WHERE UserLogin = '" + str(sub) + "'")
        fetch = cursor.fetchall()
        if(len(fetch) == 0 or len(fetch[0][0])):
            continue
        userId = str(fetch[0][0])
        bot.send_message(userId, messgeForSale)
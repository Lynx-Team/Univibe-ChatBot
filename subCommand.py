from config import cnxn

def subscribe_com(message):
    userId = message.chat.id
    subToLogin = message.text

    cursor = cnxn.cursor()
    cursor.execute('SELECT TelegramID FROM TelegramUsers WHERE UserLogin = \'' + subToLogin + '\'')
    fetch = cursor.fetchall()
    if(len(fetch) == 0):
        return
    isExist = str(fetch[0][0])
    if (isExist == 'None'):
        return


    cursor.execute('SELECT Subscribers FROM TelegramUsers WHERE UserLogin = \'' + subToLogin + '\'');
    fetch = cursor.fetchall()
    if(len(fetch) == 0):
        return
    res = str(fetch[0][0])
    
    userSubs = '' if res == None else res

    cursor.execute('SELECT UserLogin FROM TelegramUsers WHERE TelegramID = \'' + str(userId) + '\'');
    fetch = cursor.fetchall()
    if(len(fetch) == 0):
        return
    userLogin = str(fetch[0][0])
    userSubs += ('' if userSubs == '' else ',') + userLogin 

    cursor.execute('SELECT Subscriptions FROM TelegramUsers WHERE TelegramID = \'' + str(userId) + '\'');
    fetch = cursor.fetchall()
    if(len(fetch) == 0):
        return
    userSubs = str(fetch[0][0])
    userSubs += ('' if userSubs == '' else ',') + subToLogin

    print('UPDATE TelegramUsers SET Subscriptions = \'' + userSubs + '\' WHERE TelegramID = \'' + str(userId) + '\'')
    cursor.execute('UPDATE TelegramUsers SET Subscriptions = \'' + userSubs + '\' WHERE TelegramID = \'' + str(userId) + '\'');
    cnxn.commit();

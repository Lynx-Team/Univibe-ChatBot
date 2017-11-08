from urllib.request import urlopen
from dbconfig import PATH_TO_API

def startMessage(userId):
    isReg = urlopen(PATH_TO_API + 'IsRegistered/' + str(userId)).read().decode('utf-8') 

    if (isReg == 'false'):
        urlopen(PATH_TO_API + 'RegisterTelegram/' + str(userId))
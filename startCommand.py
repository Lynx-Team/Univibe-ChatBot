from urllib.request import urlopen
from config import PATH_TO_API
from main import *

def startMessage(userId):
    isReg = urlopen(PATH_TO_API + 'IsRegistered/' + str(userId)).read().decode('utf-8') 

    if (isReg == 'false'):
        urlopen(PATH_TO_API + 'RegisterTelegram/' + str(userId))
        return True

    return False
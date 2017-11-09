from urllib.request import urlopen
from config import *
def addNewUserId(id):
    urlopen(PATH_TO_API + 'RegisterTelegram/' + str(id))
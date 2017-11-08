import re
def subMessage(text):
    subNick = re.findall(r'sub\s*(.*)\s*$', text)
    if (subNick[0] == ""):
        return "Вы должны ввести логин пользователя после команды sub"
    return "Вы подписались на " + subNick[0]
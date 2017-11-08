import re
def sendMessage(userName, text):
    userText = re.findall(r'.*send\s*(.*)$', text)
    if (userText[0] == ""):
        return "Вы должны ввести сообщние после команды send"
    return "@" + userName + ":\n" + userText[0]
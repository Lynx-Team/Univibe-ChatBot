import random
HiMEssages = ["И тебе привет", "Привет, чем могу помочь?", "Здравствуй"]

def hiMessage():
    return HiMEssages[random.randint(0,len(HiMEssages) - 1)]

def helpMessage():
    return "/sub - Подписаться на рассылку пользователя \n /send \"Сообщение\" -  Отправить сообщение своим подписчикам"

def unknownMessage():
    return "Прости, я тебя не понял. Попробуй ввести команду точнее или узнай что я могу с помощью команды /help"
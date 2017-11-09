from main import *
@bot.message_handler(regexp=TSTUDENT)
def profile(message):
    bot.send_message(message.chat.id, "Теперь вы в режиме студента")

@bot.message_handler(regexp=TTABLE)
def profile(message):
    bot.send_message(message.chat.id, "Теперь вы в режиме преподователя")
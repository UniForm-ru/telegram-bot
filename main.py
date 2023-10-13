import telebot
from telebot import types

import scenatries
bot = telebot.TeleBot('6632246938:AAG9-k_TMuw6mhylWLPjFu6NvPbI6diZ8oo')

@bot.message_handler(content_types=['text'])
def start(message):
   bot.send_message(message.from_user.id, scenatries.start)



bot.polling(none_stop=True, interval=0)
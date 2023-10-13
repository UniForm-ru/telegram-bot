import telebot
from telebot import types
import psycopg2

import scenatries
bot = telebot.TeleBot('6632246938:AAG9-k_TMuw6mhylWLPjFu6NvPbI6diZ8oo')

# Подключаемся к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="UniFormBot",
    user="postgres",
    password="Indigomen_221"
)

@bot.message_handler(commands=['start'])
def start(message):
   bot.send_message(message.from_user.id, scenatries.start)
   bot.send_message(message.from_user.id, scenatries.auth)
   bot.register_next_step_handler(message, get_group_number)

def get_group_number(message):
    student_id = message.text
    global group
    cursor = conn.cursor()
    cursor.execute("SELECT group_number FROM users WHERE student_id = %s", (student_id,))
    group = cursor.fetchone()
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    button1 = telebot.types.KeyboardButton('Угадал)')
    button2 = telebot.types.KeyboardButton('Мимо')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, f"Ты из группы {group[0]}?", reply_markup=keyboard)
    bot.register_next_step_handler(message, checker)


def checker(message):
    if message.text == "Угадал)":
        bot.send_message(message.chat.id, 'Запомню : )')
    elif message.text == "Мимо":
        bot.send_message(message.chat.id, 'напиши пожалуйста из какой ты на самом деле группы и мы решим эту проблему)')
    bot.register_next_step_handler(message, schedule)

def schedule(message):
    # keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    # button1 = telebot.types.KeyboardButton('Хочу узнать расписание на сегодня!')
    # keyboard.add(button1)
    if message.text == "Хочу узнать расписание на сегодня":
        cursor = conn.cursor()
        cursor.execute("SELECT start_time FROM schedule WHERE group_name = %s", (group))
        start_time = cursor.fetchone()
        cursor.execute("SELECT end_time FROM schedule WHERE group_name = %s", (group))
        end_time = cursor.fetchone()
        bot.send_message(message.chat.id, f"сегодня у тебя занятиe с  {start_time[0]} до {end_time[0]}")



bot.polling(none_stop=True, interval=0)
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
        cursor.execute("SELECT campus, classroom, teacher,discipline, start_time, end_time FROM schedule WHERE group_name = 'M45' AND day_of_week = 'Вторник'")
        data = cursor.fetchall()
        bot.send_message(message.chat.id, 'Сегодня тебя ждут следующие испытания')
        lesson = ""
        for lesson_data in data:
            lesson = f"{lesson_data[3]} \nКорпус {lesson_data[0]} Аудитория {lesson_data[1]} \nПреподователь {lesson_data[2]} \nc {lesson_data[4]} до {lesson_data[5]} \n \n {lesson}"

        bot.send_message(message.chat.id, lesson)



bot.polling(none_stop=True, interval=0)
import telebot
import psycopg2
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from deploy import CREATE_TABLE_SCHEDULE,CREATE_TABLE_USER,insert_query_user,insert_query_schedule_1,insert_query_schedule_2,insert_query_schedule_3,insert_query_schedule_4

import scenatries
bot = telebot.TeleBot('6632246938:AAG9-k_TMuw6mhylWLPjFu6NvPbI6diZ8oo')

# Подключаемся к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="UniFormBot3",
    user="postgres",
    password="Indigomen_221"
)
cur = conn.cursor()
cur.execute(CREATE_TABLE_SCHEDULE)
cur.execute(CREATE_TABLE_USER)
cur.execute("SELECT * FROM users")
if not cur.fetchone():
    cur.execute(insert_query_user)
    cur.execute(insert_query_schedule_1)
    cur.execute(insert_query_schedule_2)
    cur.execute(insert_query_schedule_3)
    cur.execute(insert_query_schedule_4)
    conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
   global chat_id
   chat_id = message.chat.id
   bot.send_message(message.from_user.id, scenatries.start)
   bot.send_message(message.from_user.id, scenatries.auth)
   bot.register_next_step_handler(message, get_group_number)

def get_group_number(message):
    student_id = message.text
    global group, markup
    cursor = conn.cursor()
    cursor.execute("SELECT group_number FROM users WHERE student_id = %s", (student_id,))
    group = cursor.fetchone()
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton('Мимо', callback_data='no')
    button1 = InlineKeyboardButton('Угадал)', callback_data='yes')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, f"Ты из группы {group[0]}?", reply_markup=markup)
    # bot.register_next_step_handler(call, checker)

# Обрабатываем нажатие на кнопки
@bot.callback_query_handler(func=lambda call: True)
def checker(call):
    if call.data == 'yes':
        markup = InlineKeyboardMarkup()
        teacher_button = InlineKeyboardButton('расписание \n преподователя', callback_data='schedule_teacher_today')
        student_button_today = InlineKeyboardButton('расписание \n на сегодня', callback_data='schedule_today')
        student_button_tomorrow = InlineKeyboardButton('расписание \n на завтра', callback_data='schedule_tomorrow')
        markup.add(student_button_today,teacher_button,student_button_tomorrow)
        bot.send_message(chat_id, 'Запомню :)',reply_markup=markup)
    elif call.data == 'no':
        bot.send_message(chat_id, 'напиши пожалуйста из какой ты на самом деле группы и мы решим эту проблему')
    if call.data == 'schedule_teacher_today':
        cursor = conn.cursor()
        cursor.execute("SELECT campus, classroom,discipline, start_time, end_time FROM schedule WHERE teacher = 'Сушкин' AND day_of_week = 'Понедельник'")
        data = cursor.fetchall()
        bot.send_message(chat_id, 'Сегодня этого преподавателя можно найти тут')
        lesson = ""
        for lesson_data in data:
            lesson = f"{lesson_data[2]} \nКорпус {lesson_data[0]} Аудитория {lesson_data[1]} \nc {lesson_data[3]} до {lesson_data[4]} \n \n {lesson}"
        bot.send_message(chat_id, lesson)
    if call.data == 'schedule_today':
            cursor = conn.cursor()
            cursor.execute(
                "SELECT campus, classroom, teacher,discipline, start_time, end_time FROM schedule WHERE group_name = 'М45' AND day_of_week = 'Понедельник'")
            data = cursor.fetchall()
            bot.send_message(chat_id, 'Сегодня тебя ждут следующие испытания')
            lesson = ""
            for lesson_data in data:
                lesson = f"{lesson_data[3]} \nКорпус {lesson_data[0]} Аудитория {lesson_data[1]} \nПреподователь {lesson_data[2]} \nc {lesson_data[4]} до {lesson_data[5]} \n \n {lesson}"
            bot.send_message(chat_id, lesson)
    if call.data == 'schedule_tomorrow':
            cursor = conn.cursor()
            cursor.execute(
                "SELECT campus, classroom, teacher,discipline, start_time, end_time FROM schedule WHERE group_name = 'М45' AND day_of_week = 'Вторник'")
            data = cursor.fetchall()
            bot.send_message(chat_id, 'На завтра квесты такие')
            lesson = ""
            for lesson_data in data:
                lesson = f"{lesson_data[3]} \nКорпус {lesson_data[0]} Аудитория {lesson_data[1]} \nПреподователь {lesson_data[2]} \nc {lesson_data[4]} до {lesson_data[5]} \n \n {lesson}"
            bot.send_message(chat_id, lesson)



bot.polling(none_stop=True, interval=0)
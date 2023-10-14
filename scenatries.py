import datetime

start = "Привет! Это бот приложения UniForm,я буду присылать тебе расписание и информацию о твоих экзаменах и пересдачах"
auth = "Введи номер своего электронного студенческого указанный в нашем приложении P.S.(сейчас есть только пользователь 92)"


def today_weekday(tommorow=False):
    today = datetime.datetime.today().weekday()
    if tommorow:
        if today == 5:
            today = today + 2
        else:
            today = today + 1
    if today == 1:
        return "Вторник"
    elif today == 2:
        return "Среда"
    elif today == 3:
        return "Четверг"
    elif today == 4:
        return "Пятница"
    elif today == 5:
        return "Суббота"
    else:
        return "Понедельник"


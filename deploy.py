CREATE_TABLE_SCHEDULE = "CREATE TABLE IF NOT EXISTS schedule (id SERIAL PRIMARY KEY,   day_of_week VARCHAR(15) NOT NULL,group_name VARCHAR(20) NOT NULL,   start_time TIME NOT NULL,   end_time TIME NOT NULL,   classroom VARCHAR(20) NOT NULL, campus VARCHAR(20) NOT NULL,teacher VARCHAR(50) NOT NULL,discipline VARCHAR(50) NOT NULL )"
CREATE_TABLE_USER = "     CREATE TABLE IF NOT EXISTS users (         id SERIAL PRIMARY KEY,         group_number VARCHAR(50) NOT NULL,         first_name VARCHAR(50) NOT NULL,         last_name VARCHAR(50) NOT NULL,         student_id VARCHAR(50) UNIQUE NOT NULL     ); "
insert_query_user = """
    INSERT INTO users (group_number, first_name, last_name, student_id)
    VALUES ('М45', 'Дмитрий', 'Кузнецов', '92')
"""
insert_query_schedule_1 = """
    INSERT INTO schedule (day_of_week, start_time, end_time, classroom,campus,teacher,discipline,group_name )
    VALUES ('Понедельник', '12:10:00', '13:45:00', '224','3','Сушкин','Теория псевдослучайных генераторов','М45')
"""
insert_query_schedule_2 = """
    INSERT INTO schedule (day_of_week, start_time, end_time, classroom,campus,teacher,discipline,group_name )
    VALUES ('Понедельник', '14:00:00', '15:35:00', '224','3','Сушкин','Теория псевдослучайных генераторов','М45')
"""
insert_query_schedule_3 = """
    INSERT INTO schedule (day_of_week, start_time, end_time, classroom,campus,teacher,discipline,group_name )
    VALUES ('Вторник', '12:10:00', '13:45:00', '314','3','Горбунов','Дискретная Математика','М45')
"""
insert_query_schedule_4 = """
    INSERT INTO schedule (day_of_week, start_time, end_time, classroom,campus,teacher,discipline,group_name )
    VALUES ('Вторник', '14:00:00', '15:35:00', '314','3','Горбунов','Дискретная Математика','М45')
"""

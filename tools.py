# source: my old version of this bot https://gitlab.com/FFenek/session-bot/-/blob/master/tools.py
import os
from datetime import datetime, timedelta, date
import time


def get_even():  # True - Четная; False - Нечетная
    date_day = date.today()
    w = datetime(date_day.year, date_day.month, date_day.day)
    day_w = w.isoweekday()
    w = w.strftime("%d %b %Y")
    d = time.strptime(w, "%d %b %Y")
    resul = (int(time.strftime("%U", d)) % 2) == 0
    if day_w == 7:
        return not resul
    return resul


def from_text_to_array_schedule(message):
    answer = []
    temp = ''
    temp_d = []
    temp_w = []
    number_of_blank_lines = 0

    for i in message:
        if i == '\n':

            if i == "'":
                i = "’"

            number_of_blank_lines = number_of_blank_lines + 1
            if number_of_blank_lines == 1:  # следущее занятие
                temp_d.append(temp)
                temp = ''
            if number_of_blank_lines == 2:  # следущий день
                temp_w.append(temp_d)
                temp_d = []
            if number_of_blank_lines == 3:  # следущая неделя
                answer.append(temp_w)
                temp_w = []
        else:
            temp = temp + i
            number_of_blank_lines = 0

    n = 0
    while n < 2:
        if not answer:
            answer.append([])
            answer.append([])

        if len(answer) < 2:
            answer.append([])

        missing = 7 - len(answer[n])
        for j in range(missing):
            answer[n].append([' '])
        n += 1

    return answer


def from_file_to_schedule_array(name):
    try:
        file = open('temp/' + str(name) + '.txt', 'r', encoding='utf-8')

    except Exception as e:
        print(e)
        return [[[' '], [' '], [' '], [' '], [' '], [' '], [' ']], [[' '], [' '], [' '], [' '], [' '], [' '], [' ']],
                [[' ']]]

    message = file.read()

    answer = from_text_to_array_schedule(message)

    file.close()
    os.remove('temp/' + str(name) + '.txt')
    return answer

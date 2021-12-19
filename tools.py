# source: my old version of this bot https://gitlab.com/FFenek/session-bot/-/blob/master/tools.py
import os
from copy import copy
from datetime import datetime, timedelta, date
import time

import numpy as np
import pandas as pd


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


def make_the_same_number_of_elements(array):
    max = 0
    for i in array:
        if len(i) > max:
            max = len(i)

    for c in range(len(array)):
        times = max - len(array[c])
        for i in range(times):
            array[c].append('')

    return array


def delete_nans(array):
    for i in range(len(array)):
        if pd.isna(array[i]):
            array[i] = ''
    return array


def from_xlsx_to_array_schedule(message):
    file = pd.read_excel(f"temp/{str(message)}.xlsx")
    array = [list(i) for i in zip(*file.to_numpy())]

    w0 = []
    w1 = []
    for i in range(7):
        w1.append(delete_nans(array[i + 2][5:14]))
        w0.append(delete_nans(array[i + 2][20:30]))

    answer = [w0, w1]
    return answer


def from_xlsx_to_array_schedule_time(message):
    file = pd.read_excel(f"temp/{str(message)}.xlsx")
    array = [list(i) for i in zip(*file.to_numpy())]

    w0 = []
    w1 = []
    for i in range(7):
        w1.append(delete_nans(array[i + 10][5:14]))
        w0.append(delete_nans(array[i + 10][20:30]))

    answer = [w0, w1]
    return answer


def from_xlsx_to_time_of_lesson(message):
    file = pd.read_excel(f"temp/{str(message)}.xlsx")
    array = [list(i) for i in file.to_numpy()]
    return datetime.combine(date.min, array[1][12]) - datetime.min


def from_xlsx_to_name(message):
    file = pd.read_excel(f"temp/{str(message)}.xlsx")
    array = [list(i) for i in file.to_numpy()]
    return str(array[0][4])


def remove_last_empty_slots(schedule):
    schedule.reverse()
    answer = copy(schedule)
    for element in schedule:
        if element != '': break
        answer.pop(0)
    answer.reverse()
    return answer

from datetime import datetime, timedelta, date
import calendar

from Specimen import united as template
import tools


def language(user=template.User, user_language='us'):
    if user.id == 0:
        return "Sorry sweetheart, but I have no data about you, try to write /start.\n<3"
    user.language = user_language
    return f"Your preferred language => {user.language}"


# ohh... this wos so stupid... I am too lazy to write the code over a new one, so I took it from the old one when,
# comments I am not me, I would change, but I did not understand.
# https://gitlab.com/FFenek/session-bot/-/blob/master/main.py
def daily_schedule(client=template.User(), w=0, d=1, arrow=False, choice=False, week_even_ignore=False):
    try:
        if client.position['week even'] and not week_even_ignore:
            w = 1 if w == 0 else 0  # меняем местами четность недели по требованию пользователя

        if client.settings['combination of weeks']:
            w = 0  # устанавливаем четное расписание если у пользователя расписание только на одну неделю

        answer = ''
        on_account = 0
        #               UTC 0                         пользовательский UTC
        localtime = datetime.now() + timedelta(minutes=client.settings['UTC'] * 60)

        for i in client.schedule[w][d - 1]:
            on_account = on_account + 1
            couples_schedule = client.couples_schedule
            if client.settings['Time instead of number'] and len(client.schedule[w][d - 1]) < len(couples_schedule):

                # Выбор пары, тогда не стрелка и не время пары
                if choice and (on_account == client.position['lesson']):
                    answer = answer + '        ● ' + ' \t '

                # Стрелка тогда не время пары
                elif (couples_schedule[on_account] <= localtime.strftime('%H:%M') <
                      couples_schedule[on_account + 1]) and arrow:
                    answer = answer + '      → ' + ' \t '

                # Время пары
                else:
                    answer = answer + couples_schedule[on_account] + ' \t  '

            # Номер занятия
            else:
                if choice and (on_account == client.position['lesson']):
                    answer = answer + ' ●   ' + ' \t '
                else:
                    answer = answer + str(on_account) + ':  ' + ' \t  '

            answer = answer + str(i) + '\n'
    except Exception as e:
        answer = 'Wowps! We had a problem reading your schedule, I only know that: ' + str(e)
        if str(e) == 'list index out of range':
            answer = "No schedule"

    return answer


def information_line(user_id=0, w=0, d=1, message='', week_even_ignore=False):

    user = template.session.get(template.User, user_id)
    settings = template.session.query(template.Settings).filter(template.Settings.user_id == user_id)

    #               UTC 0                         пользовательский UTC
    localtime = datetime.now() + timedelta(minutes=user.utc * 60)

    answer = localtime.strftime('%H:%M') if message == '' else str(message)

    answer += ' | ' + calendar.day_name[d]

    answer += ' | ' + 'Week: E' if w % 2 == 0 else 'Week: NE'

    return answer


def information_line_daily(client, w, d):
    if client.position['week even']:
        w = 1 if w == 0 else 0  # меняем местами четность недели по требованию пользователя

    answer = f"Have a good {calendar.day_name[d]}" + ', ' + client.name
    if not client.settings['combination of weeks']:
        answer += ' | ' + 'Week: E' if w % 2 == 0 else 'Week: NE'

    return answer


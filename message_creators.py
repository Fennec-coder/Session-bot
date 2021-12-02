from datetime import datetime, timedelta, date
import telebot

from Specimen import united as template
import tools


def information_line(user_id=0, week=tools.get_even(), day=datetime.today().weekday()):
    user = template.session.get(template.User, user_id)
    localtime = datetime.utcnow() + timedelta(minutes=user.utc * 60)

    answer = f"{'Even' if week else 'Odd'} | {localtime.strftime('%H:%M')} | day: {day + 1}"

    return answer


def daily_schedule(user_id=0, week=False, day=0):
    if user_id != 0:
        settings = template.session.query(template.Settings).where(template.Settings.user_id == user_id).first()
        answer = "\n"

        if settings.id_of_the_selected_schedule is None:
            return f"{answer}You don't have schedule"

        timetable = template.session.get(template.Timetable, settings.id_of_the_selected_schedule)
        schedule = template.session.get(template.Schedule, timetable.id_of_schedule)

        if timetable is not None:
            table = timetable.table_E[day] if week else timetable.table_NE[day]
        else:
            return f"I did not find a schedule with this id ({settings.id_of_the_selected_schedule}, " \
                   f"it may have been deleted)"

        current_user = template.session.get(template.User, user_id)
        user_delta = timedelta(minutes=current_user.utc * 60)

        r_day = (datetime.utcnow() + user_delta).date().weekday()
        localtime = datetime.utcnow() + user_delta

        for lesson in range(len(table)):
            st_sch = (schedule.table_E if week else schedule.table_NE)[day][lesson]

            if settings.time_in_schedule_switch:
                next_l = datetime.combine(date.today(), st_sch) + schedule.time_of_one_lesson

                if day == r_day and next_l.time() > localtime.time() > st_sch:
                    item_number = f"{(datetime.min + (next_l - localtime)).strftime('%H:%M')}:>"
                else:
                    item_number = f"{st_sch.strftime('%H:%M')}:"
            else:
                item_number = f"{lesson + 1}:"

            answer += f"{item_number} {table[lesson]}\n"

        return answer
    else:
        return "Sorry sweetheart, but I have no data about you, try to write /start.\n<3"


def navigation_week(user_id):
    position = template.session.get(template.Positions, user_id)

    if position is None:
        return

    navigation = telebot.types.InlineKeyboardMarkup()
    week_back = telebot.types.InlineKeyboardButton(text='<', callback_data='-day')
    week_forward = telebot.types.InlineKeyboardButton(text='>', callback_data='+day')
    navigation.add(week_back, week_forward)

    week_another = telebot.types.InlineKeyboardButton(
        text=f"show {'odd' if position.week_even else 'even'} week",
        callback_data='?week')
    navigation.add(week_another)

    return navigation


def navigation_schedule_info(table):
    navigation = telebot.types.InlineKeyboardMarkup()

    if table is None:
        return

    # name = telebot.types.InlineKeyboardButton(text=f"Name: {table.name}", callback_data='?name')
    public = telebot.types.InlineKeyboardButton(text=f"Public: {'yes' if table.public else 'no'}",
                                                callback_data='?public')
    delete = telebot.types.InlineKeyboardButton(
        text="Delete", callback_data='?delete')

    # navigation.add(name)
    navigation.add(public)
    navigation.add(delete)

    return navigation

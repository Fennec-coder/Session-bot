from datetime import datetime, timedelta, date
import calendar

from Specimen import united as template
import tools


def information_line(user_id=0):
    user = template.session.get(template.User, user_id)
    localtime = datetime.utcnow() + timedelta(minutes=user.utc * 60)

    answer = f"{'E' if tools.get_even() else 'NE'} | {localtime.strftime('%H:%M')} | {localtime.strftime('%A')}"

    return answer


def daily_schedule(user_id=0, week=False, day=0):
    if user_id != 0:
        settings = template.session.query(template.Settings).where(template.Settings.user_id == user_id).first()
        timetable = template.session.get(template.Timetable, settings.id_of_the_selected_schedule)
        answer = "\n"

        table = timetable.table_E[day] if week else timetable.table_NE[day]

        for lesson in range(len(table)):
            answer += f"{lesson + 1}: {table[lesson]}\n"

        return answer
    else:
        return "Sorry sweetheart, but I have no data about you, try to write /start.\n<3"

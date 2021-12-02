from Specimen.united import *
import telebot
import message_creators
import tools

config = configparser.ConfigParser()  # parser object
config.read("config/settings.ini")  # read the configuration from the ini file

token = config["telegram"]["token"]
if token == 'token':
    token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)  # open a connection with a telegram

# hot buttons for issuing a schedule
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('/yesterday', '/today', '/tomorrow')
keyboard.row('/week')


@bot.message_handler(commands=['start'])
def start(message):
    current_user = session.get(User, message.from_user.id)

    lang = 'ru' if message.from_user.language_code == 'ru' else 'us'

    if current_user is None:
        current_user = User(id=message.from_user.id, username=message.from_user.username, language=lang)
        user_validation(current_user.id, database_check=True)
        session.add(current_user)
        session.commit()
    else:
        current_user.username = message.from_user.username

    bot.send_message(message.chat.id,
                     f"hello {current_user.username}! \nif anything, this bot is made very badly. And in general, "
                     f"I'm some kind of leftist person who receives data about you, and you also give me your "
                     f"schedule, so if I'm not too lazy, I'll take it and hunt you down and stalk you. ",
                     reply_markup=keyboard)

    session.commit()
    # crutch, I hope it won't break anything
    validation_all_users()


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        settings = session.get(Settings, message.from_user.id)

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'temp/' + str(message.from_user.id) + '.xlsx'

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        id_of_timetable = datetime.today().second + message.from_user.id

        if file_info.file_path[-4:] == 'xlsx':

            array_of_schedule = tools.from_xlsx_to_array_schedule(message.from_user.id)
            array_of_schedule_time = tools.from_xlsx_to_array_schedule_time(message.from_user.id)

            timetable = Timetable(
                id=id_of_timetable,
                name=tools.from_xlsx_to_name(message.from_user.id),
                creator=message.from_user.id,
                table_E=array_of_schedule[0],
                table_NE=array_of_schedule[1],
                id_of_schedule=id_of_timetable
            )

            schedule = Schedule(
                id=id_of_timetable,
                time_of_one_lesson=tools.from_xlsx_to_time_of_lesson(message.from_user.id),
                table_E=array_of_schedule_time[0],
                table_NE=array_of_schedule_time[1]
            )

            session.add(schedule)
            session.add(timetable)

            session.commit()

            settings.id_of_the_selected_schedule = id_of_timetable
            session.commit()

            session.query(Timetable).filter(Timetable.id != id_of_timetable,
                                            Timetable.creator == message.from_user.id,
                                            Timetable.public == False).delete()
            session.commit()
            os.remove(f"temp/{str(message.from_user.id)}.xlsx")

            bot.reply_to(message, "saved! my congratulations, best wishes, health to the victims (well, lol, you are "
                                  "studying at the university).")


        else:
            f = open("temp/Schedule template for use in session bot.xlsx", "rb")
            bot.send_document(message.chat.id, f)

            if file_info.file_path[-3:] == 'txt':
                bot.reply_to(message,
                             "this file format is no longer supported, I threw you a template, look at it ")
            else:
                bot.reply_to(message,
                             "devil knows what kind of format this is, I threw you a template, look at it ")


    except Exception as ex:
        bot.reply_to(message, f"some error occured.. sorry\n\n{ex}")
        session.rollback()


@bot.message_handler(commands=['today'])
def today(message):
    current_user = session.get(User, message.from_user.id)

    week_parity = tools.get_even()
    day = (datetime.utcnow() + timedelta(minutes=current_user.utc * 60)).date().weekday()

    answer = message_creators.information_line(current_user.id) + message_creators.daily_schedule(current_user.id,
                                                                                                  week_parity,
                                                                                                  day)
    # sorry about this
    print(f"today--> name: {current_user.username}; day: {day}; "
          f"time: {datetime.utcnow() + timedelta(minutes=current_user.utc * 60)}")

    message_id = bot.send_message(message.chat.id, answer).message_id

    position = session.get(Positions, current_user.id)
    position.last_message_id = message_id
    position.last_message_type = 'today'
    position.last_message_text = answer
    session.commit()


@bot.message_handler(commands=['yesterday'])
def yesterday(message):
    current_user = session.get(User, message.from_user.id)

    week_parity = tools.get_even()

    wd = datetime.today().weekday()
    if wd > 0:
        wd = wd - 1
    else:
        wd = 6
    week_parity = not week_parity if wd == 6 else week_parity

    answer = message_creators.information_line(current_user.id,
                                               week_parity,
                                               wd) + message_creators.daily_schedule(current_user.id,
                                                                                     week_parity,
                                                                                     wd)

    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    current_user = session.get(User, message.from_user.id)

    week_parity = tools.get_even()

    wd = datetime.today().weekday()
    if wd < 6:
        wd = wd + 1
    else:
        wd = 0
    week_parity = not week_parity if wd == 0 else week_parity

    answer = message_creators.information_line(current_user.id,
                                               week_parity,
                                               wd) + message_creators.daily_schedule(current_user.id,
                                                                                     week_parity,
                                                                                     wd)

    bot.send_message(message.chat.id, answer)


"""WEEK"""


def _week(user_id):
    current_user = session.get(User, user_id)
    position = session.get(Positions, user_id)

    answer = message_creators.information_line(current_user.id,
                                               position.week_even,
                                               position.day) + message_creators.daily_schedule(current_user.id,
                                                                                               position.week_even,
                                                                                               position.day)
    return answer


@bot.message_handler(commands=['week'])
def week(message):
    bot.send_message(message.chat.id,
                     _week(message.chat.id),
                     reply_markup=message_creators.navigation_week(message.chat.id))


"""NAVIGATION OF navigation_week"""


@bot.callback_query_handler(lambda call: call.data == '-day')
def callback_worker(call):
    position = session.get(Positions, call.message.chat.id)
    position.day = position.day - 1 if position.day > 0 else 6
    session.commit()

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=_week(call.message.chat.id),
                          reply_markup=message_creators.navigation_week(call.message.chat.id))


@bot.callback_query_handler(lambda call: call.data == '+day')
def callback_worker(call):
    position = session.get(Positions, call.message.chat.id)
    position.day = position.day + 1 if position.day < 6 else 0
    session.commit()

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=_week(call.message.chat.id),
                          reply_markup=message_creators.navigation_week(call.message.chat.id))


@bot.callback_query_handler(lambda call: call.data == '?week')
def callback_worker(call):
    position = session.get(Positions, call.message.chat.id)
    position.week_even = not position.week_even
    session.commit()

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=_week(call.message.chat.id),
                          reply_markup=message_creators.navigation_week(call.message.chat.id))


"""SCHEDULE info"""


def _schedule(user_id, table):
    current_user = session.get(User, user_id)
    settings = session.get(Settings, user_id)

    if table is None:
        return f"Schedule not found"

    answer = "Schedule information:\n" \
             f"ID: {settings.id_of_the_selected_schedule}\n\n" \
             f"Name: {table.name}\n" \
             f"Creator: {session.get(User, table.creator).username} " \
             f"{'(you)' if table.creator == current_user.id else ''}"

    return answer


@bot.message_handler(commands=['schedule'])
def schedule(message):
    settings = session.get(Settings, message.chat.id)
    positions = session.get(Positions, message.chat.id)
    table = session.get(Timetable, settings.id_of_the_selected_schedule)

    positions.last_message_type = 'id_of_the_selected_schedule'
    positions.last_message_text = str(settings.id_of_the_selected_schedule)
    session.commit()

    bot.send_message(message.chat.id,
                     _schedule(message.chat.id, table),
                     reply_markup=message_creators.navigation_schedule_info(table))


@bot.callback_query_handler(lambda call: call.data == '?public')
def callback_worker(call):
    current_user = session.get(User, call.message.chat.id)
    positions = session.get(Positions, call.message.chat.id)
    table = session.get(Timetable, int(positions.last_message_text))

    if current_user.id != table.creator:
        bot.answer_callback_query(call.id, "Dude, this is not your schedule.", show_alert=False)
    else:
        table.public = not table.public
        session.commit()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=_schedule(call.message.chat.id, table),
                              reply_markup=message_creators.navigation_schedule_info(table))


"""SETTINGS"""


# UNRELIABLE!
@bot.message_handler(commands=['time'])
def time_in_schedule_switch(message):
    settings = session.get(Settings, message.chat.id)
    settings.time_in_schedule_switch = not settings.time_in_schedule_switch
    session.commit()
    bot.send_message(message.chat.id,
                     f"Now you will see the "
                     f"{'start TIME of classes' if settings.time_in_schedule_switch else 'class NUMBER'}")


bot.polling(none_stop=True)

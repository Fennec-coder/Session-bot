import os
from Specimen.united import *

import telebot
from telebot import types

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
    lang = 'ua' if message.from_user.language_code == 'uk' else 'us'

    if current_user is None:
        current_user = User(id=message.from_user.id, username=message.from_user.username, language=lang)

        session.add(current_user)
        session.commit()
        session.add(Settings(user_id=message.from_user.id))
        session.add(Positions(user_id=message.from_user.id))
    else:
        current_user.username = message.from_user.username

    bot.send_message(message.chat.id,
                     f"hello {current_user.username}! \nif anything, this bot is made very badly. And in general, "
                     f"I'm some kind of leftist person who receives data about you, and you also give me your "
                     f"schedule, so if I'm not too lazy, I'll take it and hunt you down and stalk you. ",
                     reply_markup=keyboard)

    session.commit()


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        current_user = session.get(User, message.from_user.id)
        settings = session.get(Settings, message.from_user.id)

        if current_user is not None:

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'temp/' + str(message.from_user.id) + '.txt'

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            id_of_timetable = datetime.today().second + message.from_user.id

            array_of_schedule = tools.from_file_to_schedule_array(message.from_user.id)

            exemplar = Timetable(
                id=id_of_timetable,
                name=file_info.file_path,
                creator=message.from_user.id,
                table_E=tools.make_the_same_number_of_elements(array_of_schedule[0]),
                table_NE=tools.make_the_same_number_of_elements(array_of_schedule[1])
            )

            session.add(exemplar)
            session.commit()

            settings.id_of_the_selected_schedule = id_of_timetable
            session.commit()

            session.query(Timetable).filter(Timetable.id != id_of_timetable,
                                            Timetable.creator == message.from_user.id,
                                            Timetable.public == False).delete()
            session.commit()

            bot.reply_to(message, "saved! my congratulations, best wishes, health to the victims (well, lol, you are "
                                  "studying at the university).")
        else:
            bot.send_message(message.chat.id,
                             "i can't find you in my stalking database")

    except Exception as ex:
        bot.reply_to(message, ex)
        session.rollback()


@bot.message_handler(commands=['today'])
def today(message):
    current_user = session.get(User, message.from_user.id)

    week_parity = tools.get_even()
    if current_user is None:
        bot.send_message(message.chat.id,
                         "i can't find you in my stalking database")
    else:
        answer = message_creators.information_line(current_user.id) + \
                 message_creators.daily_schedule(current_user.id,
                                                 week_parity,
                                                 datetime.today().weekday())

        bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['yesterday'])
def yesterday(message):
    current_user = session.get(User, message.from_user.id)

    week_parity = tools.get_even()
    if current_user is None:
        bot.send_message(message.chat.id,
                         "i can't find you in my stalking database")
    else:
        wd = datetime.today().weekday()
        if wd > 0:
            wd = wd - 1
        else:
            wd = 6
        week_parity = not week_parity if wd == 6 else week_parity

        answer = message_creators.information_line(current_user.id,
                                                   week_parity,
                                                   wd) + \
                 message_creators.daily_schedule(current_user.id,
                                                 week_parity,
                                                 wd)

        bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    current_user = session.get(User, message.from_user.id)

    week_parity = tools.get_even()
    if current_user is None:
        bot.send_message(message.chat.id,
                         "i can't find you in my stalking database")
    else:
        wd = datetime.today().weekday()
        if wd < 6:
            wd = wd + 1
        else:
            wd = 0
        week_parity = not week_parity if wd == 0 else week_parity

        answer = message_creators.information_line(current_user.id,
                                                   week_parity,
                                                   wd) + \
                 message_creators.daily_schedule(current_user.id,
                                                 week_parity,
                                                 wd)

        bot.send_message(message.chat.id, answer)


@bot.callback_query_handler(func=lambda call: True)
def callback_language(call):
    answer = "-"

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=answer)


bot.polling(none_stop=True)

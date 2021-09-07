from Specimen.united import *

import telebot
from telebot import types

import message_creators
import tools

config = configparser.ConfigParser()  # parser object
config.read("config/settings.ini")  # read the configuration from the ini file

token = config["telegram"]["token"]

bot = telebot.TeleBot(token)  # open a connection with a telegram

# language selection (oh yea, real?)
language_selection = types.InlineKeyboardMarkup()
eng_button = types.InlineKeyboardButton(text="🇺🇸", callback_data='language us')
rus_button = types.InlineKeyboardButton(text="🇷🇺", callback_data='language ru')
language_selection.add(eng_button, rus_button)

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

    bot.send_message(message.chat.id,
                     f"hello {current_user.username}!",
                     reply_markup=keyboard)

    session.commit()


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        current_user = session.get(User, message.from_user.id)

        if current_user is not None:

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'temp/' + str(message.from_user.id) + '.txt'

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            current_user.schedule = tools.from_file_to_schedule_array(message.from_user.id)
            bot.reply_to(message, "saved! my congratulations, best wishes, health to the victims (well, lol, you are "
                                  "studying at the university).")
            connection.update(current_user)

        else:
            bot.send_message(message.chat.id,
                             languages.assembly['not in the database']['ru'])

    except Exception as e:
        bot.reply_to(message, e)


@bot.callback_query_handler(func=lambda call: True)
def callback_language(call):
    answer = message_creators.language(user=User.User(call.message.chat.id), user_language='ru')

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=answer)


bot.polling(none_stop=True)

import configparser
import database
from Specimen import User

import telebot
from telebot import types

config = configparser.ConfigParser()  # parser object
config.read("settings.ini")  # read the configuration from the ini file

token = config["Telegram"]["token"]

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
    client = database.get_user_obj(message.from_user.id)

    lang = 'ru' if message.from_user.language_code == 'ru' else 'us'
    lang = 'ua' if message.from_user.language_code == 'uk' else 'us'

    if client is None:
        client = User.User(0)
        client.user_id = message.from_user.id
        client.language = lang
        database.create_user(client)

    bot.send_message(message.chat.id,
                     "hi!",
                     reply_markup=keyboard)

    bot.send_message(message.chat.id,
                     f"choose a language now = {client.language}",
                     reply_markup=language_selection)


import message_creators


@bot.callback_query_handler(func=lambda call: True)
def callback_language(call):
    answer = message_creators.language(user=User.User(call.message.chat.id), user_language='ru')

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=answer)


bot.polling(none_stop=True)

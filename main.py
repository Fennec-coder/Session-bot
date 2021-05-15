import configparser

import telebot
from telebot import types

config = configparser.ConfigParser()  # parser object
config.read("settings.ini")  # read the configuration from the ini file

token = config["Telegram"]["token"]

bot = telebot.TeleBot(token)  # open a connection with a telegram

# language selection (oh yea, real?)
language_selection = types.InlineKeyboardMarkup()
eng_button = types.InlineKeyboardButton(text="🇺🇸", callback_data='language us')
ukr_button = types.InlineKeyboardButton(text="🇺🇦", callback_data='language ua')
rus_button = types.InlineKeyboardButton(text="🇷🇺", callback_data='language ru')
language_selection.add(eng_button, ukr_button, rus_button)

u_lang = 1


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'a'+('m'*u_lang)+' hi)', reply_markup=language_selection)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    pass


bot.polling(none_stop=True)

import telebot
import os
from dotenv import load_dotenv, find_dotenv
from start import *
from button_operation import *
from work_with_notes import *
from info import *

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv('TOKEN'))

bot.polling(none_stop=True)

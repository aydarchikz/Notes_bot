import telebot
from start import *
from button_operation import *
from work_with_notes import *
from info import *

bot = telebot.TeleBot('6600265888:AAF1YKbFqVrw_T2lmYY3DVRV2qyTg2PnTx0')

bot.polling(none_stop=True)

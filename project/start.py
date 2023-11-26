import sqlite3
from telebot import types

name = ''
login = ''
correct_password = ''
stop = False
retry = False
current_profile = ''
current_id = 0

@bot.message_handler(commands=['start'])
def start(message):
    global current_profile
    current_profile = ''
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar, login varchar, password varchar)')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Войти', callback_data='sign_in')
    btn2 = types.InlineKeyboardButton('Зарегистрироваться', callback_data='sign_up')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, 'Здравствуйте! Войдите в свой профиль или зарегистрируйтесь.', reply_markup=markup)

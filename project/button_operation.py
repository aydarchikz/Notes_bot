import sqlite3
from telebot import types

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global retry
    if callback.data == 'sign_up':
        bot.send_message(callback.message.chat.id, 'Введите ваше имя.')
        bot.register_next_step_handler(callback.message, user_name)
    elif callback.data == 'sign_in':
        bot.send_message(callback.message.chat.id, 'Введите ваш логин.')
        retry = True
        bot.register_next_step_handler(callback.message, check_login)
    elif callback.data == 'cancel':
        global stop
        stop = True
        bot.send_message(callback.message.chat.id, 'Для начала работы с ботом воспользуйтесь /start')
    elif callback.data == 'retry':
        retry = True

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Придумайте логин')
    global retry
    retry = True
    bot.register_next_step_handler(message, user_login)

def user_login(message):
    global stop
    global retry
    while not retry:
        if stop:
            stop = False
            return

    retry = False
    global login
    login = message.text.strip()

    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    for user in users:
        if user[2] == login:
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Отмена', callback_data='cancel')
            btn2 = types.InlineKeyboardButton('Попробовать снова', callback_data='retry')
            markup.row(btn1, btn2)
            bot.send_message(message.chat.id, 'Этот логин уже занят, придумайте другой или нажмите "Отмена" и войдите в существующий профиль.', reply_markup=markup)
            cur.close()
            conn.close()
            bot.register_next_step_handler(message, user_login)
            return
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Придумайте пароль')
    bot.register_next_step_handler(message, user_password)

def user_password(message):
    password = message.text.strip()
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, login, password) VALUES ('%s', '%s', '%s')" % (name, login, password))
    cur.execute("CREATE TABLE  IF NOT EXISTS %s (id int auto_increment primary key, note varchar)" % (login))
    conn.commit()
    cur.close()
    conn.close()
    global current_profile
    current_profile = login
    bot.send_message(message.chat.id, 'Ура! Вы успешно зарегистрировались.\nДля ознакомления с функционалом бота воспользуйтесь /info.')

def check_login(message):
    global stop
    global retry
    while not retry:
        if stop:
            stop = False
            return

    retry = False
    global login
    login = message.text.strip()
    correct_login = False

    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    global name
    global correct_password
    for user in users:
        if user[2] == login:
            correct_login = True
            name = user[1]
            correct_password = user[3]
            break
    cur.close()
    conn.close()
    if correct_login:
        bot.send_message(message.chat.id,'Введите пароль.')
        retry = True
        bot.register_next_step_handler(message, check_password)
    else:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Отмена', callback_data='cancel')
        btn2 = types.InlineKeyboardButton('Попробовать снова', callback_data='retry')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Профиля с таким логином не существует. Введите логин корректно или нажмите "Отмена" зарегистрируйтесь.', reply_markup=markup)
        bot.register_next_step_handler(message, check_login)

def check_password(message):
    global stop
    global retry
    while not retry:
        if stop:
            stop = False
            return

    retry = False
    password = message.text.strip()
    if password == correct_password:
        global current_profile
        current_profile = login
        bot.send_message(message.chat.id, "С возвращением, %s!\nДля ознакомления с функционалом бота воспользуйтесь /info." % (name))
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Отмена', callback_data='cancel'))
        bot.send_message(message.chat.id, 'Неверный пароль, попробуйте еще раз или нажмите "Отмена".', reply_markup=markup)
        bot.register_next_step_handler(message, check_password)

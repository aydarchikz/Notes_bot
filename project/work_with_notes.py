import sqlite3

@bot.message_handler(commands=['add_note'])
def add_note(message):
    global current_profile
    if current_profile == '':
        bot.send_message(message.chat.id, 'Для начала работы с ботом воспользуйтесь /start.')
        return

    bot.send_message(message.chat.id, 'Введите заметку.')
    bot.register_next_step_handler(message, add_note_finish)

def add_note_finish(message):
    note = message.text
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    global current_id
    cur.execute("INSERT INTO %s (id, note) VALUES (%d,'%s')" % (current_profile, current_id, note))
    current_id += 1
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Заметка успешно добавлена!')

@bot.message_handler(commands=['view_notes'])
def view_notes(message):
    global current_profile
    if current_profile == '':
        bot.send_message(message.chat.id, 'Для начала работы с ботом воспользуйтесь /start.')
        return

    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM %s' % (current_profile))
    notes = cur.fetchall()
    cur.close()
    conn.close()

    info = ''
    number = 0
    for note in notes:
        number += 1
        info += str(number) + '. ' + note[1] + '\n'
    bot.send_message(message.chat.id, "Ваши заметки:\n%s" % (info))

@bot.message_handler(commands=['remove_note'])
def remove_note(message):
    global current_profile
    if current_profile == '':
        bot.send_message(message.chat.id, 'Для начала работы с ботом воспользуйтесь /start.')
        return

    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM %s' % (current_profile))
    notes = cur.fetchall()
    cur.close()
    conn.close()

    info = ''
    number = 0
    for note in notes:
        number += 1
        info += str(number) + '. ' + note[1] + '\n'

    if number == 0:
        bot.send_message(message.chat.id, 'У вас нет заметок. Чтобы добавить замтеку воспользуйтесь /add_note')
        return

    bot.send_message(message.chat.id, "Ваши заметки:\n%s" % (info))
    bot.send_message(message.chat.id, 'Введите номер заметки, которую хотите удалить.')
    bot.register_next_step_handler(message, remove_note_finish)

def remove_note_finish(message):
    number = int(message.text)

    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM %s' % (current_profile))
    notes = cur.fetchall()
    remove_id = notes[0][0]
    for note in notes:
        number -= 1
        if number == 0:
            remove_id = note[0]
            break

    cur.execute(f'DELETE FROM {current_profile} WHERE id = {remove_id}')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Заметка успешно удалена.')

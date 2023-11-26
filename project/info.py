@bot.message_handler(commands=['info'])
def get_info(message):
    bot.send_message(message.chat.id, '''Данный бот умеет хранить заметки. Вы можете добавлять, просматривать и удалять заметки с любого аккаунта телеграм, если войдете в свой профиль.\n
Список команд:
/start - смена аккаунта
/add_note - добавление заметки
/view_notes - просмотр заметок
/remove_note - удаление заметок''')

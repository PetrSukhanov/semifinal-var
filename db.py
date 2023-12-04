from telebot import TeleBot, types
import mysql.connector
import telebot


bot = telebot.TeleBot('bot')

mydb = mysql.connector.connect(
    host="host",
    user="user",
    password="pass",
    database="db",
)

cursor = mydb.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    surname = f" {message.from_user.last_name}" if message.from_user.last_name else ''
    bot.send_message(message.chat.id,
                     f"Доброго времени суток, {message.from_user.first_name}{surname}. Введите пожалуйста ИНН вашей компании.")


@bot.message_handler(func=lambda message: True)
def get_next(message):
    conn = mydb.cursor()
    user_inn = message.text

    if user_inn == "/help":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Нет документов для оплаты", callback_data='fetch_doc')
        btn2 = types.InlineKeyboardButton("Нужен акт сверки", callback_data='fetch_act')
        btn3 = types.InlineKeyboardButton("Шаблон гарантийного письма", callback_data='guarantee_letter')
        btn4 = types.InlineKeyboardButton("Иной вопрос", callback_data='another_question')
        markup.add(btn1, btn2, btn3,btn4)
        bot.send_message(message.chat.id,'выберите один из следующих вопросов, который мешает вам урегулировать задолженность по договорам',reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data == 'fetch_act')
        def handle_query(call):
            if call.data == 'fetch_act':
                bot.send_message(call.message.chat.id, "Введите ИНН для более точной и быстрой обработки запроса:")
                bot.register_next_step_handler(call.message, update_value)

        def update_value(message):
            global id_value
            id_value = message.text
            bot.send_message(message.chat.id, "Если нужно введите какой-либо коментарий к этой записи или же просто введите да")
            bot.register_next_step_handler(message, update_database, id_value)

        def update_database(message, id_value):
            new_value = message.text
            cursor = mydb.cursor()
            sql = "UPDATE able SET АктСверки = %s WHERE id = %s"
            val = (new_value, id_value)
            cursor.execute(sql, val)
            mydb.commit()
            bot.send_message(message.chat.id, "Значение обновлено успешно")

        @bot.callback_query_handler(func=lambda call: call.data == 'fetch_doc')
        def handle(call):
            if call.data == 'fetch_doc':
                markup = types.InlineKeyboardMarkup(row_width=1)
                btn1 = types.InlineKeyboardButton("счет-фактура", callback_data='factura')
                btn2 = types.InlineKeyboardButton("акт выполненных работ", callback_data='act')
                btn3 = types.InlineKeyboardButton("Универсальный передаточный документ (УПД)", callback_data='UPD')
                btn4 = types.InlineKeyboardButton("счет", callback_data='schet')
                markup.add(btn1, btn2, btn3, btn4)
                bot.send_message(message.chat.id, "какие документы вам необходимы для погашения задолженности?", reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data == 'guarantee_letter')
        def handle_query(call):
            if call.data == 'guarantee_letter':
                bot.send_message(message.chat.id, "Шаблон")

        @bot.callback_query_handler(func=lambda call: call.data == 'factura')
        def handle_query(call):
            if call.data == 'factura':
                bot.send_message(call.message.chat.id, "Введите ИНН для более точной и быстрой обработки запроса:")
                bot.register_next_step_handler(call.message, value)

        def value(message):
            global id_value
            id_value = message.text
            bot.send_message(message.chat.id, "Если нужно введите какой-либо коментарий к этой записи или же просто введите да")
            bot.register_next_step_handler(message, database, id_value)

        def database(message, id_value):
            new_value = message.text
            cursor = mydb.cursor()
            sql = "UPDATE able SET СчетФактура = %s WHERE ИННдолжника = %s"
            val = (new_value, id_value)
            cursor.execute(sql, val)
            mydb.commit()
            bot.send_message(message.chat.id, "Принято")

        @bot.callback_query_handler(func=lambda call: call.data == 'schet')
        def handle_query(call):
            if call.data == 'schet':
                bot.send_message(call.message.chat.id, "Введите ИНН для более точной и быстрой обработки запроса:")
                bot.register_next_step_handler(call.message, hala)

        def hala(message):
            global id_value
            id_value = message.text
            bot.send_message(message.chat.id, "укажите пожалуйста на какую сумму необходим счет. В этом же сообщении напишите пожалуйста свои ЭДО, почтовый адрес и номер телефона, для оперативной связи с вами")
            bot.register_next_step_handler(message, base, id_value)

        def base(message, id_value):
            new_value = message.text
            cursor = mydb.cursor()
            sql = "UPDATE able SET Счет = %s WHERE ИННдолжника = %s"
            val = (new_value, id_value)
            cursor.execute(sql, val)
            mydb.commit()
            bot.send_message(message.chat.id, "Принято")

        @bot.callback_query_handler(func=lambda call: call.data == 'act')
        def handle_query(call):
            if call.data == 'act':
                bot.send_message(call.message.chat.id,"Введите ИНН для более точной и быстрой обработки запроса:")
                bot.register_next_step_handler(call.message, mala)

        def mala(message):
            global id_value
            id_value = message.text
            bot.send_message(message.chat.id,"Если нужно введите какой-либо коментарий к этой записи или же просто введите да")
            bot.register_next_step_handler(message, gala, id_value)

        def gala(message, id_value):
            new_value = message.text
            cursor = mydb.cursor()
            sql = "UPDATE able SET АктВыполненныхРабот = %s WHERE ИННдолжника = %s"
            val = (new_value, id_value)
            cursor.execute(sql, val)
            mydb.commit()
            bot.send_message(message.chat.id, "Принято")

        @bot.callback_query_handler(func=lambda call: call.data == 'UPD')
        def handle_query(call):
            if call.data == 'UPD':
                bot.send_message(call.message.chat.id,
                                 "Введите ИНН для более точной и быстрой обработки запроса:")
                bot.register_next_step_handler(call.message, malka)

        def malka(message):
            global id_value
            id_value = message.text
            bot.send_message(message.chat.id, "Если нужно введите какой-либо коментарий к этой записи или же просто введите да")
            bot.register_next_step_handler(message, galka, id_value)

        def galka(message, id_value):
            new_value = message.text
            cursor = mydb.cursor()
            sql = "UPDATE able SET УПД = %s WHERE ИННдолжника = %s"
            val = (new_value, id_value)
            cursor.execute(sql, val)
            mydb.commit()
            bot.send_message(message.chat.id, "Принято")

        return
    else:
        conn.execute("SELECT УФПС FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваш УФПС: " + str(result[0]))
        else:
            bot.send_message(message.chat.id,"Информация об организации, которую вы представляете отсутствует в базе данных должников АО Почта россии. Проверьте правильность ввода и нажмите /start, чтобы попробовать еще раз")

        conn.execute("SELECT ОДЗ FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваше ОДЗ: " + str(result[0]))

        conn.execute("SELECT ПДЗ FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваше ПДЗ: " + str(result[0]))

        conn.execute("SELECT НомерДоговора FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваш Номер Договора: " + str(result[0]))

        conn.execute("SELECT ДниПросрочкиПА FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "У вас: " + str(result[0]) + " дней просрочки")

        conn.execute("SELECT Должник FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваша компания: " + str(result[0]))
        # conn.close()

    bot.send_message(message.chat.id, 'введите /help, чтобы получить нужные вам документы или задать вопрос поддержке')





bot.polling(none_stop=True)

import telebot
from all_in import *
import logging
import time
from telebot import types


#Инициация логгов(отчет о работе бота)
logging.basicConfig(level=logging.INFO, filename='telebot_log.log', filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")

#Токен телеграм бота, можно менять
bot = telebot.TeleBot('token')

# Коэффициент
coefficient = {
    'valfex': 1,
    'valtec': 1,
    'aquasfera': 1,
    'gallop': 1,
    'itap': 1,
    'stout': 1,
    'bugatti': 1,
}

# Список торговых марок
list_tm = [
    'valfex',
    'valtec','aquasfera','gallop',
    'itap','stout','bugatti',
]

# Создаем сущность кнопок
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

# Создаем сами кнопки в которых находиться текст
btn1 = types.KeyboardButton("👋 Поздороваться")
btn2 = types.KeyboardButton("📊 Верни базы данных")
btn3 = types.KeyboardButton("❓ Как мне обновить базу артикулов?")
btn4 = types.KeyboardButton("💹 Верни базу артикулов с ценами")
btn5 = types.KeyboardButton("🎰 Изменить коэффиценты")
btn6 = types.KeyboardButton("🗑 База артикулов")

# Добовляем отображение кнопок
markup.add(btn1, btn2, btn3, btn4, btn5, btn6)


# Создаем сущность кнопок
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)

# Создаем сами кнопки в которых находиться текст
tm1 = types.KeyboardButton("Valfex")
tm2 = types.KeyboardButton("Valtec")
tm3 = types.KeyboardButton("Aquasfera")
tm4 = types.KeyboardButton("Gallop")
tm5 = types.KeyboardButton("Itap")
tm6 = types.KeyboardButton("Stout")
tm7 = types.KeyboardButton("Bugatti")

# Добовляем отображение кнопок
markup3.add(tm1, tm2, tm3, tm4, tm5, tm6, tm7)












@bot.message_handler(commands = ['start'])
def start(message):
    global coefficient
# Переменные
    n = 0

#Написание сообщения полсе ввода функции старт
    bot.send_message(message.chat.id, text=
    "Привет, {0.first_name}! Я бот ☃. \nЯ захожу на сайты раз в сутки и собираю с них цены."
    "\nСписок сайтов которые я сейчас поддерживаю:\n -valtec.ru \n -valfex.ru \n -santech.ru \n -stout.ru \n -teremopt.ru"
    .format(message.from_user), reply_markup=markup)

#Отбраотка парсера сайтов
    try:    
        while n < 1:
            time = datetime.now().strftime("%H:%M:%S")
            if time == '04:01:00':
                logging.info('Взял в работу')
                main(coefficient) #< парсер вот тут
                logging.info('Отработал')
                bot.send_message(message.chat.id, text = f'{datetime.now()}\n Все отработало корректно!')
    except Exception as exc:
        bot.send_message(message.chat.id, text = exc)
        logging.error("Exception", exc_info=True)
        pass

# Отработка функции change
@bot.message_handler(commands = ['change'])
# Запрашиваем у пользователя торговую марку
def change(message):
    send = bot.send_message(message.chat.id, 'Введите тороговую марку', reply_markup=markup3)
    bot.register_next_step_handler(send, trade_mark)

# Запрашиваем у пользователя коэффицент
def trade_mark(message):
    global tm
    tm = message.text.lower()
    if tm in list_tm:
        send = bot.send_message(message.chat.id, 'Введите коэффицент')
        bot.register_next_step_handler(send, enter_coff)
    else:
        bot.send_message(message.chat.id, 'Нет такой тороговой марки')
        return

# Исправляем имеющийся списко
def enter_coff(message):
    global coefficient
    try:
        text = message.text
        text = text.replace(',', '.')
        coefficient[tm] = float(text)
    except Exception as exc:
        bot.send_message(message.chat.id, 'Некорректное значение')
    bot.send_message(message.chat.id, text=
                        f'Valfex : {coefficient["valfex"]}\n'
                        f'Valtec : {coefficient["valtec"]}\n'
                        f'Aquasfera : {coefficient["aquasfera"]}\n'
                        f'Gallop : {coefficient["gallop"]}\n'
                        f'Itap : {coefficient["itap"]}\n'
                        f'Stout : {coefficient["stout"]}\n'
                        f'Bugatti : {coefficient["bugatti"]}\n',
                        reply_markup=markup
                        )

@bot.message_handler(commands = ['log_info'])
def log_info(message):
    bot.send_message(message.from_user.id, text = 'Возвращаю логи')

    bot.send_document(message.chat.id, open('telebot_log.log', 'rb'))

# Отработка кнопок
@bot.message_handler(content_types='text') 
def func(message):
    global coefficient
#Ответ на кнопку поздороваться
    if (message.text == "👋 Поздороваться"):
        bot.send_message(message.chat.id, text = 'Привет! Работаем!')

#Ответ на кнопку Верни базы данных
    elif (message.text == "📊 Верни базы данных"):
        bot.send_message(message.chat.id, text = 'Хорошо ✅')
        bot.send_document(message.chat.id,open('santex.xlsx','rb'))
        bot.send_document(message.chat.id,open('valtec.xlsx','rb'))
        bot.send_document(message.chat.id,open('santex.xlsx','rb'))
        bot.send_document(message.chat.id,open('valfex.xlsx','rb'))
        bot.send_document(message.chat.id,open('gallop.xlsx','rb'))
        bot.send_document(message.chat.id,open('itap.xlsx','rb'))
        bot.send_document(message.chat.id,open('stout.xlsx','rb'))
        bot.send_document(message.chat.id,open('bugatti.xlsx','rb'))

#Ответ на кнопку Как мне обновить базу артикулов?
    elif (message.text == "❓ Как мне обновить базу артикулов?"):
        bot.send_message(message.chat.id, text = '1. Скачать шаблон базы артикулов')
        bot.send_document(message.chat.id,open('Шаблон сопоставления артикулов.xlsx','rb'))
        bot.send_message(message.chat.id, text = '2. Назвать файл следующий именем:\n База сопоставления артикулов.xlsx')
        bot.send_message(message.chat.id, text = '3. Отправить файл мне')

#Ответ на кнопку Верни базу артикулов с ценами
    elif (message.text == "💹 Верни базу артикулов с ценами"):
        bot.send_message(message.chat.id, text = 'Секунду ✅')
        time.sleep(2)
        bot.send_document(message.chat.id,open('База артикулов с ценами.xlsx','rb'))
        bot.send_document(message.chat.id,open('База артикулов с ценами без кэф.xlsx','rb'))

#Ответ на кнопку Изменить коэффиценты
    elif(message.text == "🎰 Изменить коэффиценты"):
        bot.send_message(message.chat.id, 'Актуальные коэфициенты')
        bot.send_message(message.chat.id, text =
                        f'Valfex : {coefficient["valfex"]}\n'
                        f'Valtec : {coefficient["valtec"]}\n'
                        f'Aquasfera : {coefficient["aquasfera"]}\n'
                        f'Gallop : {coefficient["gallop"]}\n'
                        f'Itap : {coefficient["itap"]}\n'
                        f'Stout : {coefficient["stout"]}\n'
                        f'Bugatti : {coefficient["bugatti"]}\n'
                        )
        bot.send_message(message.chat.id, 'Если хотите их изменить введите или нажмите -> /change')

#Ответ на кнопку База артикулов
    elif (message.text == "🗑 База артикулов"):
        bot.send_message(message.chat.id, 'Актуальная база артикулов')
        bot.send_document(message.chat.id,open('База сопоставления артикулов.xlsx','rb'))


@bot.message_handler(content_types = ['document'])
def handler_doc(message):
    try:
#Условия сохрарнение документа
        if message.document.file_name == 'База сопоставления артикулов.xlsx':
            chat_id = message.chat.id

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = message.document.file_name

            with open(src, 'wb') as new_fiel:
                new_fiel.write(downloaded_file)

            bot.reply_to(message, 'Пожалуй я сохраню это')
        else:
            bot.reply_to(message, 'Такое я сохранять не буду ❌')
    except Exception as exc:
        bot.send_message(chat_id, text = exc)
        logging.error("Exception", exc_info=True)
        pass

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as exc:
        logging.error("Exception", exc_info=True)
        time.sleep(15)
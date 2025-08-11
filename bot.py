# БЛОК ИМПОРТА НЕОБХОДИМЫХ ИНСТРУМЕНТОВ
import telebot 
from telebot import types
bot = telebot.TeleBot('8332629811:AAFkM9cE-W1a3abIWNMTADdfFi_L6dADpDc')  # API token


'''# объявим метод для получения текстовых сообщений
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
# тут добавили слушателя для текстовых сообщений и метод их обработки
# сделали тип контента - текст, хотя может быть любой: document, audio etc.
# @bot.message_handler(content_types=['text', 'document', 'audio'])

# сделаем 2 простые команды:
# 1. при написании привет - отреагируем
# 2. при написании /help - поможем

    # if message.text.lower() == 'привет':
    #     bot.send_message(message.chat.id, 'Привет, чем могу помочь?')
    # elif message.text == '/help':
    #     bot.send_message(message.chat.id, 'Попробуй написать "Привет"')
    # else:
    #     bot.send_message(message.chat.id, 'Я тебя не понимаю, попробуй написать "/help"')



# теперь вне всех методов напишем строку
# # bot.polling(none_stop=True, interval=0)

# теперь бот будет постоянно спрашивать у сервера о том, написал ли пользователь сообщени. 
# если написал, то немедленно ответит

# теперь пишем в консоли "python bot.py" 'bot.py' - название файла


# теперь добавим кнопки и ветки сообщений
# сделаем простого бота, что спрашивает имя, фамилию, возраст
# используем метод register_next_step_handler
# 
# keyboard = types.InlineKeyboardMarkup()
# key_start = types.InlineKeyboardButton(text='Старт', callback_data='/start'
# key_help = types.InlineKeyboardButton(text='Помощь', callback_data='/help'
# key_reg = types.InlineKeyboardButton(text='Регистрация', callback_data='/reg'
# key_hi = types.InlineKeyboardButton(text='Привет (надо поздороваться)', callback_data='привет')
# keyboard.add(key_start, key_help, key_reg, key_hi)'''



# ХЕНДЛЕР 1 (=обработчик)
@bot.message_handler(content_types=['text'])



# БЛОК ОСНОВНЫХ ФУНКЦИЙ
def base(message):    
    if message.text == '/start':
        start(message)
        mvp(message)
    
    elif message.text.lower() == 'привет':
        hi_message(message)
        mvp(message)
    
    elif message.text == '/help':
        help(message)
    
    elif message.text == '/reg':
        reg(message)
    
    else:
        err(message)

def start(message):
    bot.send_message(message.chat.id, '---ОПИСАНИЕ---\nТелеграм бот для записи на процедуры в студию маникюра Malyar\n v.0.0.0.1 от 08.08.2025')

def mvp(message):
    bot.send_message(message.chat.id, '---MVP---\nПопробуй написать /help или /reg')

def hi_message(message):
    bot.send_message(message.chat.id, '---ПРИВЕТСТВИЕ---\nа вот раньше надо было здороваться ))')

def help(message):
    help_message = '---ПОМОЩЬ---\n- /start - в самое начало\n- /help - помощь и перечень возможностей бота\n- /reg - регистрация своих данных\n- "привет" - общение надо начинать с приветствия :)'
    bot.send_message(message.chat.id, help_message)

def reg(message):
    bot.send_message(message.chat.id, '---ТЫ КТО---\nКак тебя зовут?')
    later(message)

def later(message):
    bot.register_next_step_handler(message, get_name)

def err(message):
    error_message = f'---ОШИБКА---\nУпс, кажись я тебя не понимаю... ты вписал: "{message.text}, что не является внутренней командой. Попробуй написать /help'
    bot.send_message(message.chat.id, error_message)




def response(call):
    bot.send_message(call.message.chat.id, '---MVP---\nПопробуй написать /help или /reg')



# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ (ПОКА ХЗ ЗАЧЕМ)
name = ''
lastname = ''
age = 0

# ЛИЧНАЯ ИНФОРМАЦИЯ
def get_name(message):
    '''мы изначально добавили глобальные переменные имени, фамилии и возраста. 
    ключевое слово global даст доступ к этой перемнной внутри других функций, в добавок к этому
    оно изменит значения глобальных переменных, позволит нам менять их внутри самих функций. 
    пока хз для чего'''
    
    global name  
    name = message.text
    bot.send_message(message.chat.id, '---ПОГОНЯЛО---\nКакая у тебя фамилия?')
    bot.register_next_step_handler(message, get_lastname)

def get_lastname(message):
    global lastname  # Исправлено: было global get_lastname
    lastname = message.text  # Добавлено сохранение фамилии
    bot.send_message(message.chat.id, '---КТО ПО МАСТИ---\nСколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    try:
        age = int(message.text)
    except Exception:
        bot.send_message(message.chat.id, 'Возраст введен некорректно. Введите число.')
        bot.register_next_step_handler(message, get_age)  # Повторный запрос возраста
        return
        
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='/reg')
    keyboard.add(key_yes, key_no)
    
    question = f'---ПРОВЕРЬ---\nТебе {age} лет, тебя зовут {name} {lastname}?'
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)
# теперь бот присылает клавиатуру, но ничего с ней не делает
# напишем метод-обработчик


# ХЕНДЛЕР 2 (=обработчик)
@bot.callback_query_handler(func=lambda call: True)


# ОБРАБОТЧИК КНОПОК
def callback_worker(call):
    if call.data == 'yes':
        answ = f'---АНКЕТА---\nАга, значит ты {name} {lastname} и тебе {age} лет'
        bot.send_message(call.message.chat.id, answ)  # Исправлено: call.message.chat.id
        response(call)
    
    
    elif call.data == '/reg':
        answ = '---ТЫ КАЖЕТСЯ ЧЕ-ТО НАПУТАЛ---\nТак, что-то тут нечисто, давай разбираться снова...\nнажми вот сюда --> /reg'
        bot.send_message(call.message.chat.id, answ)  # Исправлено: call.message.chat.id
        # start(call)  # Запускаем процесс заново



# БЕСКОНЕЧНЫЙ ЗАПРОС НА СЕРВЕР ОБ АКТИВНОСТИ ПОЛЬЗОВАТЕЛЯ
bot.polling(none_stop=True, interval=0)
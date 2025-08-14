import telebot
from telebot import types
import sqlite3


API_TOKEN = '8332629811:AAFkM9cE-W1a3abIWNMTADdfFi_L6dADpDc'
bot = telebot.TeleBot(API_TOKEN)
#todo Это нароботка для работы с бд! Пока она не работает и не трогай ее 
# # БАЗА ДАННЫХ 
def init_db():
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            lastname TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_client(chat_id, name=None, lastname=None, age=None, phone=None):
    try:
        conn = sqlite3.connect('clients.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO clients (chat_id, name, lastname, age, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, name, lastname, age, phone))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка при сохранении в БД: {e}")

def get_client(chat_id):
    try:
        conn = sqlite3.connect('clients.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, lastname, age, phone FROM clients WHERE chat_id = ?', (chat_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"Ошибка при чтении из БД: {e}")
        return None

init_db()

# КОМАНДЫ
@bot.message_handler(commands=['start'])
def start(message):
    # Проверяем, есть ли пользователь в базе
    user_data = get_client(message.chat.id)

    if user_data:
        name, lastname, age, phone = user_data
        # Пользователь уже есть
        bot.send_message(
            message.chat.id,
            f'💅 Добро пожаловать обратно, {name}!\n'
            'Вы уже зарегистрированы.\n'
            'Чтобы посмотреть свои данные — /mydata\n'
            'Чтобы записаться — /record (в разработке)'
        )
    else:
        # Нового пользователя встречаем
        bot.send_message(
            message.chat.id,
            '💅 Добро пожаловать в *Malyar Studio*!\n'
            'Для записи на процедуру нужно пройти быструю регистрацию.',
            parse_mode='Markdown'
        )
        # Предлагаем зарегистрироваться
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton('/reg')
        markup.add(btn)
        bot.send_message(message.chat.id, 'Нажмите кнопку ниже, чтобы начать:', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = ('---ПОМОЩЬ---\n'
                 '/start — начать\n'
                 '/help — помощь\n'
                 '/reg — зарегистрироваться\n'
                 '/update - редактировать ваши данные после регистрации'
                 '"привет" — поздороваться')
    bot.send_message(message.chat.id, help_text)
#todo пока бот ломается если человек, который уже зарегестрировался, регестрируется повторно
@bot.message_handler(commands=['reg'])
def reg(message):
    user_data = get_client(message.chat.id)

    if user_data:
        # Уже зарегистрирован
        name, lastname, age, phone = user_data
        bot.send_message(
            message.chat.id,
            f'✅ Вы уже зарегистрированы как {name} {lastname}.\n'
            'Если нужно обновить данные — напишите /update'
        )
        return

    # Если нет — начинаем анкету
    bot.send_message(message.chat.id, '---АНКЕТА---\nКак вас зовут?')
    bot.register_next_step_handler(message, get_name)

@bot.message_handler(commands=['update'])
def update_data(message):
    bot.send_message(
        message.chat.id,
        ' Вы можете обновить свои данные.\n'
        'Начнём с имени:'
    )
    bot.register_next_step_handler(message, get_name)
    
# Имя
def get_name(message):
    # Проверяем, что пришёл текст
    if message.content_type != 'text':
        bot.send_message(message.chat.id, 'Ожидался текст. Пожалуйста, введите имя.')
        bot.register_next_step_handler(message, get_name)
        return

    name = message.text.strip()
    if not name:
        bot.send_message(message.chat.id, 'Имя не может быть пустым. Попробуйте снова:')
        bot.register_next_step_handler(message, get_name)
        return

    bot.send_message(message.chat.id, 'Фамилия:')
    bot.register_next_step_handler(message, get_lastname, name)

# Фамилия
def get_lastname(message, name):
    if message.content_type != 'text':
        bot.send_message(message.chat.id, 'Ожидался текст. Введите фамилию:')
        bot.register_next_step_handler(message, get_lastname, name)
        return

    lastname = message.text.strip()
    if not lastname:
        bot.send_message(message.chat.id, 'Фамилия не может быть пустой. Попробуйте снова:')
        bot.register_next_step_handler(message, get_lastname, name)
        return

    bot.send_message(message.chat.id, 'Напишите ваш номер телефона ')
    bot.register_next_step_handler(message, get_number, name, lastname)

# Номер телефона
def get_number(message, name, lastname):
    if message.content_type != 'text':
        bot.send_message(message.chat.id, 'Ожидался текст. Введите возраст числом:')
        bot.register_next_step_handler(message, get_number, name, lastname)
        return

    try:
        age = message.text
        if  len(age) == 10:
            raise ValueError
    except:
        bot.send_message(message.chat.id, 'ВВедите 10 цифр')
        bot.register_next_step_handler(message, get_number, name, lastname) # пока не обработается ошибка бот не заработает 
        return

    # Сохраняем
    save_client(message.chat.id, name=name, lastname=lastname, age=age)

    # Подтверждение
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text=' Да', callback_data='confirm_yes')
    key_no = types.InlineKeyboardButton(text=' Заново', callback_data='confirm_no')
    keyboard.add(key_yes, key_no)

    bot.send_message(
        message.chat.id,
        f'Проверьте данные:\nИмя: {name}\nФамилия: {lastname}\nВозраст: {age}',
        reply_markup=keyboard
    )

# === ОБРАБОТЧИК КНОПОК ===
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'confirm_yes': 
        #todo надо здесь нужно сделать сохранение данных в бота, а то получается что он пишет, что сохранил, а по факту не сохранил 
        bot.send_message(call.message.chat.id, 'Спасибо! Ваши данные сохранены в базе.')
    elif call.data == 'confirm_no':
        bot.send_message(call.message.chat.id, 'Хорошо, начнём анкету заново.')
        reg(call.message)

# === ОБРАБОТЧИК ТЕКСТА ===
@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text.lower() in ['привет', 'hello', 'hi']:
        bot.send_message(message.chat.id, 'Привет! Нажми /help, чтобы узнать, что я умею.')
    elif not message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Я не понял. Напишите /help.')

# === ОБРАБОТЧИК СТИКЕРОВ, ФОТО, ГОЛОСОВЫХ И Т.Д. ===
@bot.message_handler(content_types=['sticker', 'photo', 'voice', 'video', 'document', 'audio', 'animation', 'video_note'])
def handle_unexpected_content(message):
    bot.send_message(
        message.chat.id,
        "Я принимаю только текстовые сообщения.\n"
        "Пожалуйста, введите данные текстом или используйте команды."
    )

# === ЗАПУСК ===
if __name__ == '__main__':
    print("Бот запущен. Ожидание сообщений...")
    bot.polling(none_stop=True, interval=0)
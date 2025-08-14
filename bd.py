import sqlite3

# Подключаемся к базе
conn = sqlite3.connect('clients.db')
cursor = conn.cursor()

# Выполняем запрос
cursor.execute("SELECT chat_id, name, lastname, age, phone FROM clients")
rows = cursor.fetchall()

# Проверяем, есть ли данные
if rows:
    print(" Все клиенты:")
    print("-" * 60)
    for row in rows:
        chat_id, name, lastname, age, phone = row
        print(f" ID чата: {chat_id}")
        print(f" Имя: {name}")
        print(f" Фамилия: {lastname}")
        print(f" Возраст: {age}")
        print(f" Телефон: {phone or 'не указан'}")
        print("-" * 60)
else:
    print(" База данных пуста.")

# Закрываем соединение
conn.close()
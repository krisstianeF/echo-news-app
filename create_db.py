import sqlite3
import os
from blob import convert_to_binary  # Импортируем вашу функцию для работы с картинками

def create_and_fill_database():
    db_name = 'echo_database.db'
    
    # Подключаемся к БД (если файла нет, он создастся)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    print("Шаг 1: Создание таблиц...")

    # 1. Таблица article
    cursor.execute("""CREATE TABLE IF NOT EXISTS article (
        articleID INTEGER NOT NULL PRIMARY KEY, publishID INTEGER NOT NULL,
        categoryID INTEGER NOT NULL, image BLOB, title TEXT NOT NULL,
        subtitle TEXT, article_text TEXT NOT NULL, article_date DATE NOT NULL,
        article_time TIME NOT NULL, article_link TEXT NOT NULL)""")

    # 2. Таблица avatar
    cursor.execute("""CREATE TABLE IF NOT EXISTS avatar (
        avatarID INTEGER NOT NULL PRIMARY KEY, avatarPath TEXT)""")

    # 3. Таблица category
    cursor.execute("""CREATE TABLE IF NOT EXISTS category (
        categoryID INTEGER NOT NULL PRIMARY KEY, category_name TEXT(50) NOT NULL, icon BLOB)""")

    # 4. Таблица comment
    cursor.execute("""CREATE TABLE IF NOT EXISTS comment (
        commentID INTEGER NOT NULL PRIMARY KEY, articleID INTEGER NOT NULL,
        userID INTEGER NOT NULL, comment_text TEXT NOT NULL,
        comment_date DATE NOT NULL, comment_time TIME NOT NULL)""")

    # 5. Таблица connection_tag_article
    cursor.execute("""CREATE TABLE IF NOT EXISTS connection_tag_article (
        connectionTagID INTEGER NOT NULL PRIMARY KEY, tagID INTEGER NOT NULL, articleID INTEGER NOT NULL)""")

    # 6. Таблица connection_user_category
    cursor.execute("""CREATE TABLE IF NOT EXISTS connection_user_category (
        connectionUserID INTEGER NOT NULL PRIMARY KEY, userID INTEGER NOT NULL, categoryID INTEGER NOT NULL)""")

    # 7. Таблица interaction
    cursor.execute("""CREATE TABLE IF NOT EXISTS interaction (
        interactionID INTEGER NOT NULL PRIMARY KEY, userID INTEGER NOT NULL,
        articleID INTEGER NOT NULL, type TEXT NOT NULL)""")

    # 8. Таблица publish
    cursor.execute("""CREATE TABLE IF NOT EXISTS publish (
        publishID INTEGER NOT NULL PRIMARY KEY, publish_name TEXT(50) NOT NULL,
        logo BLOB, link TEXT)""")

    # 9. Таблица tag
    cursor.execute("""CREATE TABLE IF NOT EXISTS tag (
        tagID INTEGER NOT NULL PRIMARY KEY, tag_name TEXT NOT NULL)""")

    # 10. Таблица user
    cursor.execute("""CREATE TABLE IF NOT EXISTS user (
        userID INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL,
        username TEXT NOT NULL, user_password TEXT NOT NULL, avatarID INTEGER NOT NULL)""")

    print("Шаг 2: Заполнение таблиц данными...")

    # --- ЗАПОЛНЕНИЕ ТАБЛИЦЫ PUBLISH (Издательства) ---
    # Данные со скриншота
    publishes = [
        (1, 'РИА Новости', 'publish/ria.jpg', 'https://ria.ru/'),
        (2, 'Аргументы и факты', 'publish/aif.jpg', 'https://aif.ru/'),
        (3, 'ТАСС', 'publish/tass.jpg', 'https://tass.ru/')
    ]
    
    for p_id, p_name, p_logo_path, p_link in publishes:
        try:
            # Проверяем, есть ли файл, чтобы не было ошибки
            if os.path.exists(p_logo_path):
                logo_blob = convert_to_binary(p_logo_path)
            else:
                logo_blob = None # Если картинки нет, оставляем пусто
                
            cursor.execute("INSERT OR IGNORE INTO publish VALUES (?, ?, ?, ?)", (p_id, p_name, logo_blob, p_link))
            print(f" - Добавлено издательство: {p_name}")
        except Exception as e:
            print(f" ! Ошибка при добавлении издательства {p_name}: {e}")

    # --- ЗАПОЛНЕНИЕ ТАБЛИЦЫ CATEGORY (Категории) ---
    # Данные со скриншота
    categories = [
        (1, 'Популярное', 'categories/hot.jpg'),   # Взял hot.jpg как заглушку, поменяйте если есть другая
        (2, 'Свежее', 'categories/recent.jpg'),
        (3, 'Политика', 'categories/hot.jpg'),
        (4, 'Экономика', 'categories/coin.jpg'),
        (5, 'Культура', 'categories/masks.jpg'),
        (6, 'Спорт', 'categories/gamepad.jpg'),
        (7, 'Наука', 'categories/science.jpg'),
        (8, 'Здоровье', 'categories/health.jpg'),
        (9, 'Игры', 'categories/gamepad.jpg')      # Взял gamepad.jpg как заглушку
    ]

    for c_id, c_name, c_icon_path in categories:
        try:
            if os.path.exists(c_icon_path):
                icon_blob = convert_to_binary(c_icon_path)
            else:
                icon_blob = None
                
            cursor.execute("INSERT OR IGNORE INTO category VALUES (?, ?, ?)", (c_id, c_name, icon_blob))
            print(f" - Добавлена категория: {c_name}")
        except Exception as e:
            print(f" ! Ошибка при добавлении категории {c_name}: {e}")

    # --- ЗАПОЛНЕНИЕ ТАБЛИЦЫ AVATAR (Аватарки) ---
    # Данные со скриншота (от 1 до 16)
    for i in range(1, 17):
        avatar_path = f'gui/avatars/avatar_{i}.png'
        cursor.execute("INSERT OR IGNORE INTO avatar VALUES (?, ?)", (i, avatar_path))
    print(" - Добавлены аватарки (с 1 по 16)")

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
    
    print("\nБаза данных успешно создана и заполнена всеми базовыми данными!")

if __name__ == "__main__":
    create_and_fill_database()
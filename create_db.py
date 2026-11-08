import sqlite3
import os
from src.core.blob import convert_to_binary
from src.config import DB_PATH, Assets

def create_and_fill_database():
    # --- 1. УДАЛЕНИЕ СТАРОЙ БАЗЫ ---
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("Старая база данных удалена. Создаем новую...")
        except PermissionError:
            print("\n❌ ОШИБКА: Файл базы данных занят другим процессом!")
            print("Закройте приложение (main.py) и SQLiteStudio, затем запустите скрипт снова.")
            return
    else:
        print("Файл базы данных не найден. Создаем новый...")

    # Подключаемся к БД
    connection = sqlite3.connect(DB_PATH)
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
    # ВАЖНО: Пути к картинкам должны совпадать с реальностью. 
    # Если картинки в assets/publish/, используйте пути с 'assets/'.
    publishes = [
        (1, 'РИА Новости', Assets.PUB_RIA, 'https://ria.ru/'),
        (2, 'Аргументы и факты', Assets.PUB_AIF, 'https://aif.ru/'),
        (3, 'ТАСС', Assets.PUB_TASS, 'https://tass.ru/')
    ]
    
    for p_id, p_name, p_logo_path, p_link in publishes:
        try:
            if os.path.exists(p_logo_path):
                logo_blob = convert_to_binary(p_logo_path)
            else:
                logo_blob = None
            cursor.execute("INSERT OR IGNORE INTO publish VALUES (?, ?, ?, ?)", (p_id, p_name, logo_blob, p_link))
            print(f" - Добавлено издательство: {p_name}")
        except Exception as e:
            print(f" ! Ошибка при добавлении издательства {p_name}: {e}")

    # --- ЗАПОЛНЕНИЕ ТАБЛИЦЫ CATEGORY (Категории) ---
    # ВАЖНО: На скриншоте видно, что картинки категорий лежат в assets/categories/
    # Но с расширением .jpg, а не .png!
    categories = [
        (1, 'Популярное', Assets.CAT_HOT),
        (2, 'Свежее', Assets.CAT_RECENT),
        (3, 'Политика', Assets.CAT_POLITICS),   # Взял hot как заглушку
        (4, 'Экономика', Assets.CAT_ECONOMY),
        (5, 'Культура', Assets.CAT_CULTURE),
        (6, 'Спорт', Assets.CAT_SPORT),      # Взял cup как заглушку
        (7, 'Наука', Assets.CAT_SCIENCE),
        (8, 'Здоровье', Assets.CAT_HEALTH),
        (9, 'Игры', Assets.CAT_GAMES)
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
    for i, avatar_path in enumerate(Assets.AVATARS, start=1):
        cursor.execute("INSERT OR IGNORE INTO avatar VALUES (?, ?)", (i, avatar_path))
    print(f" - Добавлены аватарки (с 1 по 16)")

    # --- ЗАПОЛНЕНИЕ ТАБЛИЦЫ USER (Тестовый пользователь) ---
    try:
        cursor.execute("""INSERT OR IGNORE INTO user (userID, name, username, user_password, avatarID) 
                          VALUES (?, ?, ?, ?, ?)""", (1, 'kris', 'kris', '111111', 1))
        print(" - Добавлен тестовый пользователь: kris (пароль: 111111)")
    except Exception as e:
        print(f" ! Ошибка при добавлении пользователя: {e}")

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
    
    print("\nБаза данных успешно создана в папке 'data' и заполнена!")

if __name__ == "__main__":
    create_and_fill_database()
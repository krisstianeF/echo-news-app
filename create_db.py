import sqlite3

def create_database():
    # Подключаемся к БД (если файла нет, он создастся)
    connection = sqlite3.connect('echo_database.db')
    cursor = connection.cursor()

    # 1. Таблица article
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS article (
        articleID INTEGER NOT NULL PRIMARY KEY,
        publishID INTEGER NOT NULL,
        categoryID INTEGER NOT NULL,
        image BLOB,
        title TEXT NOT NULL,
        subtitle TEXT,
        article_text TEXT NOT NULL,
        article_date DATE NOT NULL,
        article_time TIME NOT NULL,
        article_link TEXT NOT NULL
    )
    """)

    # 2. Таблица avatar
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avatar (
        avatarID INTEGER NOT NULL PRIMARY KEY,
        avatarPath TEXT
    )
    """)

    # 3. Таблица category
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category (
        categoryID INTEGER NOT NULL PRIMARY KEY,
        category_name TEXT(50) NOT NULL,
        icon BLOB
    )
    """)

    # 4. Таблица comment
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comment (
        commentID INTEGER NOT NULL PRIMARY KEY,
        articleID INTEGER NOT NULL,
        userID INTEGER NOT NULL,
        comment_text TEXT NOT NULL,
        comment_date DATE NOT NULL,
        comment_time TIME NOT NULL
    )
    """)

    # 5. Таблица connection_tag_article
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS connection_tag_article (
        connectionTagID INTEGER NOT NULL PRIMARY KEY,
        tagID INTEGER NOT NULL,
        articleID INTEGER NOT NULL
    )
    """)

    # 6. Таблица connection_user_category
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS connection_user_category (
        connectionUserID INTEGER NOT NULL PRIMARY KEY,
        userID INTEGER NOT NULL,
        categoryID INTEGER NOT NULL
    )
    """)

    # 7. Таблица interaction
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interaction (
        interactionID INTEGER NOT NULL PRIMARY KEY,
        userID INTEGER NOT NULL,
        articleID INTEGER NOT NULL,
        type TEXT NOT NULL
    )
    """)

    # 8. Таблица publish
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publish (
        publishID INTEGER NOT NULL PRIMARY KEY,
        publish_name TEXT(50) NOT NULL,
        logo BLOB,
        link TEXT
    )
    """)

    # 9. Таблица tag
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tag (
        tagID INTEGER NOT NULL PRIMARY KEY,
        tag_name TEXT NOT NULL
    )
    """)

    # 10. Таблица user
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        userID INTEGER NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        user_password TEXT NOT NULL,
        avatarID INTEGER NOT NULL
    )
    """)

    connection.commit()
    connection.close()
    print("База данных 'echo_database.db' успешно создана (все 10 таблиц).")

if __name__ == "__main__":
    create_database()
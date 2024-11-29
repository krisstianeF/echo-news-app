from database import INSERT
from blob import convert_to_binary
import sqlite3

def insert_into_publish(publishID, publish_name, image, link):
    sqlite_connection = sqlite3.connect('echo_database.db')
    cursor = sqlite_connection.cursor()

    insert = """INSERT INTO publish (publishID, publish_name, logo, link) VALUES (?, ?, ?, ?)"""
    logo = convert_to_binary(image)

    try:
        data_tuple = (publishID, publish_name, logo, link)
        cursor.execute(insert, data_tuple)
        print('Добавлено новое издательство: ', publish_name)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def insert_into_category(categoryID, category_name, image):
    sqlite_connection = sqlite3.connect('echo_database.db')
    cursor = sqlite_connection.cursor()

    insert = """INSERT INTO category (categoryID, category_name, icon) VALUES (?, ?, ?)"""
    icon = convert_to_binary(image)

    try:
        data_tuple = (categoryID, category_name, icon)
        cursor.execute(insert, data_tuple)
        print('Добавлена категория: ', category_name)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


'''insert_into_publish(2, "Аругменты и факты", "publish/aif.jpg", "https://aif.ru/")
insert_into_publish(3, "ТАСС", "publish/tass.jpg", "https://tass.ru/")'''

'''insert_into_category(7, 'Наука', 'categories/science.jpg')
insert_into_category(8, 'Здоровье', 'categories/health.jpg')
insert_into_category(9, 'Игры', 'categories/gamepad.jpg')'''

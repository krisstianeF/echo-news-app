import sqlite3
import os
from datetime import datetime
from src.style import Style

from src.core.blob import convert_to_binary
from src.config import DB_PATH

class Database:
    """Взаимодействия интерфейса с базой данных"""
    def __init__(self):
        self.db_connection = sqlite3.connect(DB_PATH)

    def get_one(self, request, id):
        cursor = self.db_connection.cursor()
        cursor.execute(request, (id, ))
        return cursor.fetchone()[0]


    """Publish and category -----------------------------------------------------"""

    def get_category_name(self, id):
        cursor = self.db_connection.cursor()
        cursor.execute("""SELECT category_name FROM category WHERE categoryID = ?""", (id,))
        return cursor.fetchone()[0]

    def get_publish_name(self, id):
        cursor = self.db_connection.cursor()
        cursor.execute("""SELECT publish_name FROM publish WHERE publishID = ?""", (id,))
        return cursor.fetchone()[0]

    def insert_into_publish(self, publishID, publish_name, image, link):

        sqlite_connection = sqlite3.connect(DB_PATH)
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

    def insert_into_category(self, categoryID, category_name, image):

        sqlite_connection = sqlite3.connect(DB_PATH)
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


    """Article -------------------------------------------------------------------"""

    def get_ids(self, request) -> list:
        ids_list = []

        cursor = self.db_connection.cursor()
        cursor.execute(request)
        ids = cursor.fetchall()
        for id in ids:
            ids_list.append(id[0])

        self.db_connection.commit()

        return ids_list

    def get_category_ids(self, request, id) -> list:
        '''Формирование списка id из sql запроса request'''
        ids = []

        cursor = self.db_connection.cursor()
        cursor.execute(request, (id, ))
        id_list = cursor.fetchall()
        for id in id_list:
            ids.append(id[0])

        self.db_connection.commit()

        return ids

    def get_search_ids(self, query):
        ids = []

        if not query:
            return
        # Поиск новостей в базе данных
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT articleID FROM article WHERE LOWER(title) LIKE ? OR LOWER(subtitle) LIKE ?", (f'%{query}%', f'%{query}%'))
        news_ids = cursor.fetchall()
        for id in news_ids:
            ids.append(id[0])

        self.db_connection.commit()

        return ids

    def get_search_ids_wth_filter(self, start_date, end_date, query):
        ids = []

        if not query:
            return
        # Поиск новостей в базе данных
        cursor = self.db_connection.cursor()
        cursor.execute(
            """SELECT articleID, article_date FROM article 
            WHERE article_date <= ? AND article_date >= ? 
            AND (title LIKE ? OR subtitle LIKE ?) 
            ORDER BY article_date DESC;""", (start_date, end_date, f'%{query}%', f'%{query}%'))
        news_ids = cursor.fetchall()
        for id in news_ids:
            ids.append(id[0])

        self.db_connection.commit()

        return ids

    def transform_date(self, date_str):
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return date_obj.strftime("%d.%m.%Y")
            except ValueError as e:
                print(f"Ошибка преобразования даты: {e}")
                return None

    def get_article_card_data(self, id) -> list:
        '''Получение данных статьи для карточки'''
        data = []
        cursor = self.db_connection.cursor()
        select = """SELECT title, subtitle FROM article WHERE articleID = ?;"""
        cursor.execute(select, (id, ))
        title_subtitle = cursor.fetchone()
        data.append(title_subtitle)

        other_data_select = f"""SELECT publish.publish_name, category.category_name, article.article_date, article.article_time FROM publish, article, category
                                WHERE articleID = {id} AND article.publishID = publish.publishID AND article.categoryID = category.categoryID;"""

        cursor.execute(other_data_select)
        other_data = cursor.fetchone()
        date = self.transform_date(other_data[2])

        other_data_new = other_data[:2] + (date,) + other_data[3:]
        data.append(other_data_new)

        title = data[0][0]
        subtitle = data[0][1]
        other = '    |    '.join(data[1])

        select = f"""SELECT article_link FROM article WHERE articleID = {id};"""
        cursor.execute(select)
        url = cursor.fetchone()

        '''select = f"""SELECT image FROM article WHERE articleID = {id};"""
        cursor.execute(select)
        image = cursor.fetchone()
        blob_image = image[0]
        png_data = blob_to_png(blob_image)'''
        png_data = 0

        data = [title, subtitle, other, url[0], png_data]

        return data

    def insert_interaction(self, user_id, article_id, type):

        cursor = self.db_connection.cursor()
        ids = self.get_ids("""SELECT interactionID FROM interaction""")
        last_id = ids[-1]

        cursor.execute('''SELECT userID, articleID FROM interaction''')
        user_article = cursor.fetchall()

        a = (user_id, article_id)
        if a not in user_article:
            insert = """INSERT INTO interaction VALUES (?, ?, ?, ?);"""
            cursor.execute(insert, (last_id+1, user_id, article_id, type))
            self.show_message_box('echo',
                                 'Статья успешно добавлена')
        else:
            self.show_message_box('echo',
                                  'Статья уже добавлена')

        self.db_connection.commit()

    @classmethod
    def show_message_box(self, title, message):
        from PyQt5.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)

        msg_box.setStyleSheet(f'''
                        QMessageBox {{
                            background-color: {Style.white};
                            font-family: Muller Light;
                            font-size: 14px;
                        }}''')
        msg_box.setStandardButtons(QMessageBox.Yes)

        # Изменение стиля и текста кнопок
        yes_button = msg_box.button(QMessageBox.Yes)
        yes_button.setStyleSheet(f'''QPushButton {{
                            background-color: {Style.blue40};
                            color: {Style.black};
                            border: none;
                            padding-left: 32px;
                            padding-right: 32px;
                            padding-top: 8px;
                            padding-bottom: 8px;
                            border-radius: 4px;
                            font-size: 14px;
                        }}
                        QPushButton:hover {{
                            background-color: {Style.blue50};
                        }}''')
        yes_button.setText('ОК')

        msg_box.setText(message)
        msg_box.exec_()





    """User ---------------------------------------------------------------------"""

    def get_user_data(self, user_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name, username FROM user WHERE userID = ?", (user_id,))
        return cursor.fetchone()

    def get_avatar_path(self, user_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT avatarPath FROM avatar, user WHERE user.avatarID = avatar.avatarID AND userID = ?", (user_id,))
        return cursor.fetchone()[0]

    """---------------------------------------------------------------------"""

    def user_max_id(self) -> int:
        cursor = self.db_connection.cursor()
        cursor.execute("""SELECT userID FROM user""")

        id = cursor.fetchall()
        article_id_list = []

        for row in id:
            for x in row:
                    article_id_list.append(x)

        maxID = max(article_id_list)
        self.db_connection.commit()
        return maxID

    def update_name(self, user_id, new_name):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE user SET name = ? WHERE userID = ?", (new_name, user_id))
        self.db_connection.commit()

    def update_username(self, user_id, new_name):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE user SET username = ? WHERE userID = ?", (new_name, user_id))
        self.db_connection.commit()

    def insert_user_data(self, id, name, username, password, avatarID):
        cursor = self.db_connection.cursor()
        insert = f"""INSERT INTO user VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(insert, (id, name, username, password, avatarID,))
        self.db_connection.commit()

    def delete_user_data(self, id):
        cursor = self.db_connection.cursor()
        cursor.execute(f"DELETE FROM user WHERE userID = ?", (id, ))
        self.db_connection.commit()


    """Interaction----------------------------------------------------------------"""

    def create_interaction(self):
        cursor = self.db_connection.cursor()


        self.db_connection.commit()
        pass

class INSERT:

    def __init__(self):

        db = SELECT()
        self.new_id = db.article_max_id()

        ria = RIA()
        aif = AIF()
        tass = TASS()

        for l in ria.categoties_urls:
            ria_urls = ria.get_urls(l[1])
            ria_articles_data = ria.get_articles_data(ria_urls, 1, l[0])
            self.insert_into_article(ria_articles_data)

        for l in aif.categoties_urls:
            aif_urls = aif.get_urls(l[1])
            articles_data = aif.get_articles_data(aif_urls, 2, l[0])
            self.insert_into_article(articles_data)

        for l in tass.categoties_urls:
            urls = tass.get_urls(l[1])
            articles_data = tass.get_articles_data(urls, 3, l[0])
            self.insert_into_article(articles_data)

    def insert_into_article(self, data_list: list):
            sqlite_connection = sqlite3.connect(DB_PATH)
            cursor = sqlite_connection.cursor()

            insert = f"""INSERT INTO article VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            try:
                print('Максимальный articleID:', self.new_id)
                for data in data_list:
                    self.new_id += 1
                    all_data = (self.new_id,) + data

                    cursor.execute(insert, all_data)
                    print(f'Добавлено: {all_data[7]} | {all_data[0]} | {all_data[4]} | {all_data[9]}')

                sqlite_connection.commit()
                cursor.close()

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)

            finally:
                if sqlite_connection:
                    sqlite_connection.close()


class SELECT:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect(DB_PATH)
        self.cursor = self.sqlite_connection.cursor()

    def article_max_id(self) -> int:
        select = """SELECT articleID FROM article"""
        self.cursor.execute(select)
        id = self.cursor.fetchall()
        article_id_list = []

        for row in id:
            for x in row:
                    article_id_list.append(x)

        # ИСПРАВЛЕНИЕ: Если база пустая, возвращаем 0
        if not article_id_list:
            self.maxID = 0
        else:
            self.maxID = max(article_id_list)
            
        self.sqlite_connection.commit()
        return self.maxID


    def links(self) -> list:

        self.cursor.execute("""SELECT article_link FROM article""")
        link = self.cursor.fetchall()

        self.article_urls = []

        for row in link:
            for x in row:
                self.article_urls.append(x)

        #print('Начальная длинна списка ссылок: ', len(self.article_urls))
        self.sqlite_connection.commit()

        return self.article_urls
import requests
import sqlite3
import shutil
from bs4 import BeautifulSoup
from blob import convert_to_binary
import os
from datetime import datetime
from style import Style

class Database:
    """Взаимодействия интерфейса с базой данных"""
    def __init__(self):
        self.db_connection = sqlite3.connect('echo_database.db')

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

    def insert_into_category(self, categoryID, category_name, image):

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


class SELECT:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('echo_database.db')
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
            sqlite_connection = sqlite3.connect('echo_database.db')
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

class RIA:
    def __init__(self):
        self.db = SELECT()

        self.categoties_urls = [(3, 'https://ria.ru/politics/'),
                           (4, 'https://ria.ru/economy/'),
                           (6, 'https://rsport.ria.ru/football/'),
                           (6, 'https://rsport.ria.ru/hockey/'),
                           (6, 'https://rsport.ria.ru/figure_skating/'),
                           (6, 'https://rsport.ria.ru/tennis/'),
                           (6, 'https://rsport.ria.ru/fights/'),
                           (6, 'https://rsport.ria.ru/lyzhnye-gonki/'),
                           (6, 'https://rsport.ria.ru/biathlon/'),
                           (6, 'https://rsport.ria.ru/category_formula_1/'),
                           (5, 'https://ria.ru/culture/'),
                           (7, 'https://ria.ru/science/')]

    def get_urls(self, category_url) -> list:
        '''Получение ссылок на новости РИА по категориям'''
        urls = self.db.links()

        responce = requests.get(category_url)
        html = responce.text
        soup = BeautifulSoup(html, 'html.parser')

        try:
            ria_news_container = soup.select_one("div.list.list-tags")
            ria_news = ria_news_container.find_all("a")
        except AttributeError:
            ria_news_container = soup.select_one("div.list")
            ria_news = ria_news_container.find_all("a")

        ria_category_urls = []

        for new_link in ria_news:

            url = new_link.get("href")

            if url.startswith("https://") and url not in self.db.article_urls:
                ria_category_urls.append(url)
                urls.append(url)

        return ria_category_urls

    '''Получение данных каждой новости (articleID, publishID, categoryID, image, title, subtitle, article_text, article_date, article_time, article_link)'''
    def get_articles_data(self, urls, publishID, categoryID) -> list:

        articleID = self.db.article_max_id()
        articles_data = []

        for url in urls:

            responce = requests.get(url)
            html = responce.text
            soup = BeautifulSoup(html, 'html.parser')

            ''' Сохранение текста статьи в массив '''
            try:
                text_container = soup.select_one(
                    'div.article__body.js-mediator-article.mia-analytics')  # контейнер всего текста статьи
                article_blocks = text_container.find_all('div',
                                                         class_='article__text')  # список абзацев статьи в html формате
            except AttributeError:
                continue

            article_text_array = []  # список абзацев статьи
            for i in article_blocks:
                article_text_array.append(i.get_text())

            article_text = "/".join(article_text_array)

            articleID += 1
            ''' Сохранение изображения статьи в директорию article_images'''
            try:
                image_container = soup.select_one('div.photoview__open')  # контейнер, где хранится фото
                image_tag = image_container.find_all('img')
                image_link = image_tag[0].get("src")  # получение ссылки на фото
                response = requests.get(image_link, stream=True)
                # Сохранение фото
                with open(f"article_images/article{articleID}_img.jpg", 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
            except AttributeError:
                continue

            blob_article_img = convert_to_binary(
                f"article_images/article{articleID}_img.jpg")  # Конвертация в формат blob

            os.remove(f"article_images/article{articleID}_img.jpg")

            ''' Заголовок и подзаголовок статьи по ссылке url из списка ссылок urls '''
            try:
                title = soup.select_one('div.article__title').text
                subtitle = soup.select_one('h1.article__second-title').text
            except AttributeError:
                title = soup.select_one('h1.article__title').text
                subtitle = ' '

            ''' Дата и время публикации статьи '''
            date_container = soup.select_one('div.article__info-date')
            article_date = date_container.select_one('a').text[-10:]
            year = article_date[6:]
            month = article_date[3:5]
            day = article_date[:2]
            date_list = [year, month, day]
            article_date = '-'.join(date_list)
            article_time = date_container.select_one('a').text[:5]
            article_link = url

            ''' Добавление данных статьи в кортеж articles_data '''
            article_data = (publishID, categoryID, blob_article_img, title, subtitle, article_text, article_date, article_time, article_link)
            #article_data = (publishID, categoryID, f"article_images/article{articleID}_img.jpg", title, subtitle, article_text, article_date, article_time, article_link)
            articles_data.append(article_data)

        return articles_data


    '''Получение тэгов статей'''
    def get_articles_tags(self, category_url):

        responce = requests.get(category_url)
        html = responce.text
        soup = BeautifulSoup(html, 'html.parser')

class AIF:
    def __init__(self):
        self.db = SELECT()
        self.categoties_urls = [(3, 'https://aif.ru/politics'),
                                (4, 'https://aif.ru/money'),
                                (5, 'https://aif.ru/culture'),
                                (6, 'https://aif.ru/sport'),
                                (7, 'https://aif.ru/society/science'),
                                (8, 'https://aif.ru/health')]

    '''Получение ссылок на новости по категориям'''

    def get_urls(self, category_url) -> list:

        urls = self.db.links()

        responce = requests.get(category_url)
        html = responce.text
        soup = BeautifulSoup(html, 'html.parser')

        news_container = soup.select_one("section.article_list.content_list_js")
        news = news_container.find_all("a")

        category_urls = []

        for new_link in news:
            url = new_link.get("href")

            if url.startswith("https://") and url not in category_urls and url not in urls:
                category_urls.append(url)
                urls.append(url)

        return category_urls

    ''' Получение данных каждой новости '''

    def get_articles_data(self, urls, publishID, categoryID) -> list:

        articles_data = []
        articleID = self.db.article_max_id()

        for url in urls:
            responce = requests.get(url)
            html = responce.text
            soup = BeautifulSoup(html, 'html.parser')

            ''' Сохранение текста статьи в массив '''
            try:
                text_container = soup.select_one('div.article_text')
                article_texts = text_container.find_all('p')

                article_text_array = []  # список абзацев статьи
                for i in article_texts:
                    article_text_array.append(i.get_text())

                article_text = "/".join(article_text_array)

            except AttributeError:
                continue

            articleID += 1
            ''' Сохранение изображения статьи в директорию article_images'''
            try:
                image_container = soup.select_one('div.img_box')  # контейнер, где хранится фото
                image_tag = image_container.find_all('img')
                image_link = image_tag[0].get("src")  # получение ссылки на фото
                response = requests.get(image_link, stream=True)
                # Сохранение фото
                with open(f"article_images/article{articleID}_img.jpg", 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
            except AttributeError:
                continue

            blob_article_img = convert_to_binary(
                f"article_images/article{articleID}_img.jpg")  # Конвертация в формат blob

            ''' Заголовок и подзаголовок статьи по ссылке url из списка ссылок urls '''
            title_check = soup.select_one('h1').text
            if title_check[-1] != "?":
                title = soup.select_one('h1').text[9:-4]
            else:
                continue

            subtitle = None
            ''' Дата и время публикации статьи '''
            date_container = soup.select_one('div.article_top')
            article_date = date_container.select_one('a').text[:10]
            year = article_date[6:]
            month = article_date[3:5]
            day = article_date[:2]
            date_list = [year, month, day]
            article_date = '-'.join(date_list)

            article_time = date_container.select_one('a').text[-5:]

            article_link = url

            ''' Добавление данных статьи в список articles_data '''
            article_data = (
            publishID, categoryID, blob_article_img, title, subtitle, article_text, article_date, article_time,
            article_link)
            # article_data = (publishID, categoryID, f"article_images/article{articleID}_img.jpg", title, subtitle, article_text, article_date, article_time, article_link)
            articles_data.append(article_data)

        return articles_data

class TASS:
    def __init__(self):
        self.db = SELECT()
        self.categoties_urls = [(3, 'https://tass.ru/politika'),
                                (4, 'https://tass.ru/ekonomika'),
                                (6, 'https://tass.ru/sport'),
                                (5, 'https://tass.ru/kultura')]

        self.month = [('01', 'января'), ('02', 'февраля'),
                      ('03', 'марта'), ('04', 'апреля'), ('05', 'мая'),
                      ('06', 'июня'), ('07', 'июля'), ('08', 'августа'),
                      ('09', 'сентября'), ('10', 'октября'), ('11', 'ноября'),
                      ('12', 'декабря')]

    '''Получение ссылок на новости по категориям'''

    def get_urls(self, category_url) -> list:

        urls = self.db.links()

        responce = requests.get(category_url)
        html = responce.text
        soup = BeautifulSoup(html, 'html.parser')

        news_container = soup.select_one("div.Listing_list__GXTvv")
        news = news_container.find_all("a", "tass_pkg_link-v5WdK tass_pkg_card_wrapper-r-hZB tass_pkg_card_wrapper--fixed-aaYyN tass_pkg_card_wrapper--extra_large-uKpvC")

        category_urls = []

        for new_link in news:
            url = new_link.get("href")

            if url not in category_urls and url not in urls:
                url = "https://tass.ru" + url
                category_urls.append(url)
                urls.append(url)

        return category_urls

    ''' Получение данных каждой новости '''

    def get_articles_data(self, urls, publishID, categoryID) -> list:

        articles_data = []
        articleID = self.db.article_max_id()

        for url in urls:
            responce = requests.get(url)
            html = responce.text
            soup = BeautifulSoup(html, 'html.parser')

            ''' Заголовок и подзаголовок статьи по ссылке url из списка ссылок urls '''
            title = soup.select_one('h1').text
            subtitle = soup.select_one('div.NewsHeader_lead__PbGDx.NewsHeader_lead--with_media__iebqJ')
            if subtitle != None:
                subtitle = subtitle.text

            ''' Сохранение текста статьи '''
            try:
                text_container = soup.select_one('article.Content_wrapper__DiAVL')
                article_texts = text_container.find_all('span')

                article_text_array = []  # список абзацев статьи
                for i in article_texts:
                    article_text_array.append(i.get_text())

                article_text = "/".join(article_text_array)
            except AttributeError:
                continue

            articleID += 1
            ''' Сохранение изображения статьи '''
            '''try:
                image_container = soup.select_one('div.ImageSSR_wrapper__5_A4t') # контейнер, где хранится фото
                image_tag = image_container.select_one('img')
                image_link = image_tag.get("src") # получение ссылки на фото


                h = httplib2.Http('.cache')
                response, content = h.request(image_link)
                out = open(f'article_images/article{articleID}_img.jpg', 'wb')
                out.write(content)
                out.close()

                blob_article_img = convert_to_binary(f"article_images/article{articleID}_img.jpg")  # Конвертация в формат blob

            except AttributeError:
                image_container = ''
                image_tag = ''
                image_link = ''
                blob_article_img = None
            '''

            ''' Дата и время публикации статьи '''
            info = soup.select_one('div.PublishedMark_date__LG42P').text
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            if info[-1] not in numbers:
                info = info[:-2]

            article_date = info[:-7]
            month = ''
            day = article_date[:2]
            day1 = ''
            for t in self.month:
                if t[1] in article_date:
                    month = t[0]
            if  article_date[1] not in numbers:
                day1 = f'0{day[:-1]}'
            else:
                day1 = day[:2]


            article_date_list = ['2024', month, day1]
            article_date = '-'.join(article_date_list)

            article_time = info[-5:]

            article_link = url


            ''' Добавление данных статьи в список articles_data '''
            # article_data = (publishID, categoryID, blob_article_img, title, subtitle, article_text, article_date, article_time, article_link)

            article_data = (publishID, categoryID, None, title, subtitle, article_text, article_date, article_time, article_link)
            articles_data.append(article_data)

        return articles_data
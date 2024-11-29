import requests
import sqlite3
import shutil
from bs4 import BeautifulSoup
from blob import convert_to_binary
import os

class SELECT:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('echo_database.db')
        self.cursor = self.sqlite_connection.cursor()

    def max_id(self) -> int:
        select = """SELECT articleID FROM article"""
        self.cursor.execute(select)

        id = self.cursor.fetchall()
        article_id_list = []

        for row in id:
            for x in row:
                    article_id_list.append(x)

        self.maxID = max(article_id_list)
        self.sqlite_connection.close()

        return self.maxID
    def links(self) -> list:

        self.cursor.execute("""SELECT article_link FROM article""")
        link = self.cursor.fetchall()

        self.article_urls = []

        for row in link:
            for x in row:
                self.article_urls.append(x)

        #print('Начальная длинна списка ссылок: ', len(self.article_urls))
        self.sqlite_connection.close()

        return self.article_urls

class INSERT:
    def __init__(self):

        a = SELECT()
        self.new_id = a.max_id()

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

    '''Получение ссылок на новости РИА по категориям'''
    def get_urls(self, category_url) -> list:
        a = SELECT()
        urls = a.links()

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

            if url.startswith("https://") and url not in a.article_urls:
                ria_category_urls.append(url)
                urls.append(url)

        return ria_category_urls

    '''Получение данных каждой новости (articleID, publishID, categoryID, image, title, subtitle, article_text, article_date, article_time, article_link)'''
    def get_articles_data(self, urls, publishID, categoryID) -> list:

        a = SELECT()
        articleID = a.max_id()

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
        self.categoties_urls = [(3, 'https://aif.ru/politics'),
                                (4, 'https://aif.ru/money'),
                                (5, 'https://aif.ru/culture'),
                                (6, 'https://aif.ru/sport'),
                                (7, 'https://aif.ru/society/science'),
                                (8, 'https://aif.ru/health')]

    '''Получение ссылок на новости по категориям'''

    def get_urls(self, category_url) -> list:

        a = SELECT()
        urls = a.links()

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

        a = SELECT()
        articles_data = []
        articleID = a.max_id()

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

        a = SELECT()
        urls = a.links()

        responce = requests.get(category_url)
        html = responce.text
        soup = BeautifulSoup(html, 'html.parser')

        news_container = soup.select_one("div.Listing_list__GXTvv")
        news = news_container.find_all("a", 'tass_pkg_link-v5WdK tass_pkg_card_wrapper-r-hZB tass_pkg_card_wrapper--fixed-aaYyN tass_pkg_card_wrapper--extra_large-uKpvC')

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

        a = SELECT()
        articles_data = []
        articleID = a.max_id()

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


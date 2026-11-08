from src.core.database import SELECT
from src.core.blob import convert_to_binary
from src.config import BASE_DIR
import os, requests, shutil
from bs4 import BeautifulSoup

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
            '''try:
                image_container = soup.select_one('div.photoview__open')  # контейнер, где хранится фото
                image_tag = image_container.find_all('img')
                image_link = image_tag[0].get("src")  # получение ссылки на фото
                response = requests.get(image_link, stream=True)
                # Сохранение фото
                img_path = os.path.join(ARTICLE_IMAGES_DIR, f"article{articleID}_img.jpg")
                with open(img_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
            except AttributeError:
                continue

            blob_article_img = convert_to_binary(
                f"article_images/article{articleID}_img.jpg")  # Конвертация в формат blob

            os.remove(f"article_images/article{articleID}_img.jpg")'''

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
            article_data = (publishID, categoryID, None, title, subtitle, article_text, article_date, article_time, article_link)
            #article_data = (publishID, categoryID, f"article_images/article{articleID}_img.jpg", title, subtitle, article_text, article_date, article_time, article_link)
            articles_data.append(article_data)

        return articles_data


    '''Получение тэгов статей'''
    def get_articles_tags(self, category_url):

        responce = requests.get(category_url)
        html = responce.text
        soup = BeautifulSoup(html, 'html.parser')
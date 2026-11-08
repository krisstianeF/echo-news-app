from src.core.database import SELECT
from src.core.blob import convert_to_binary
from src.config import BASE_DIR
import os, requests, shutil
from bs4 import BeautifulSoup

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
            '''try:
                image_container = soup.select_one('div.img_box')  # контейнер, где хранится фото
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
            publishID, categoryID, None, title, subtitle, article_text, article_date, article_time,
            article_link)
            # article_data = (publishID, categoryID, f"article_images/article{articleID}_img.jpg", title, subtitle, article_text, article_date, article_time, article_link)
            articles_data.append(article_data)

        return articles_data
from src.core.database import SELECT
from src.core.blob import convert_to_binary
from src.config import BASE_DIR
import os, requests, shutil
from bs4 import BeautifulSoup

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
                os.remove(f"article_images/article{articleID}_img.jpg")
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
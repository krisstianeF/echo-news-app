from src.parsers.ria import RIA
from src.parsers.aif import AIF
from src.parsers.tass import TASS
from src.core.database import SELECT
from src.config import DB_PATH
import sqlite3

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
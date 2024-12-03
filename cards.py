from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QScrollArea,
                             QFrame, QLabel, QPushButton, QHBoxLayout,
                             QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize
from datetime import datetime
import sqlite3
import webbrowser
import os
from blob import blob_to_png, crop_image

def font(family, size):
    font = QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font
def transform_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except ValueError as e:
        print(f"Ошибка преобразования даты: {e}")
        return None

def open_link(url):
    if url:
        webbrowser.open(url)

''' Создание интерфейса карточки новости '''
def create_news_card(title, subtitle, other_data, url, png_data):
    # Создание фрейма для карточки новости
    card_frame = QFrame()
    card_frame.setStyleSheet("background-color: white; border-radius: 16px;")

    card_layout = QHBoxLayout()
    card_layout.setContentsMargins(16, 16, 16, 16)
    card_layout.setSpacing(16)

    wrap = QVBoxLayout()

    if png_data != None:
        # изображение
        imageButton = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(imageButton.sizePolicy().hasHeightForWidth())
        imageButton.setSizePolicy(sizePolicy)
        #imageButton.setMinimumSize(QtCore.QSize(250, 180))
        imageButton.setStyleSheet(f'''QPushButton{{
        border-radius: 16px;
        border: none;
        background-color: transparent;
        padding: 0;
        margin: 0;
        }}''')

        # Сохранение файла
        with open('article_image.png', 'wb') as f:
            f.write(png_data)
        crop_image('article_image.png', 'article_image.png', 1250, 1000, 80)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('article_image.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        imageButton.setIcon(icon)
        imageButton.setIconSize(QtCore.QSize(250, 180))

        # Удаление файла
        if os.path.exists('article_image.png'):
            os.remove('article_image.png')


        card_layout.addWidget(imageButton)


    # Лейбл для других данных и кнопки
    other_data_layout = QHBoxLayout()

    other_data_label = QLabel(other_data)
    font = QFont("Muller", 9, QFont.Normal)
    other_data_label.setFont(font)
    other_data_label.setStyleSheet("color: #6BB0FF;")
    other_data_layout.addWidget(other_data_label)

    # Добавляем горизонтальный спейсер
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    other_data_layout.addItem(spacer)

    # Кнопки
    icon_size = 32

    favorite_button = QPushButton()
    favorite_button.setIcon(QIcon("gui/icons/heart.png"))
    favorite_button.setIconSize(QSize(icon_size, icon_size))
    favorite_button.setFixedSize(icon_size, icon_size)
    favorite_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    favorite_button.setStyleSheet('''QPushButton:hover {
    icon: url(gui/icons/heart2.png);
    }''')

    read_later_button = QPushButton()
    read_later_button.setIcon(QIcon("gui/icons/bookmark.png"))
    read_later_button.setIconSize(QSize(icon_size, icon_size))
    read_later_button.setFixedSize(icon_size, icon_size)
    read_later_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    read_later_button.setStyleSheet('''QPushButton:hover {
        icon: url(gui/icons/bookmark2.png);
        }''')

    other_data_layout.addWidget(favorite_button)
    other_data_layout.addWidget(read_later_button)

    # Добавляем layout с кнопками в основной layout карточки
    wrap.addLayout(other_data_layout)

    # Лейблы для заголовка и подзаголовка
    title_label = QLabel(title)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(50)
    sizePolicy.setHeightForWidth(title_label.sizePolicy().hasHeightForWidth())
    title_label.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setFamily("Muller Light")
    font.setPointSize(16)
    title_label.setFont(font)
    title_label.setWordWrap(True)

    subtitle_label = QLabel(subtitle)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(50)
    sizePolicy.setHeightForWidth(subtitle_label.sizePolicy().hasHeightForWidth())
    subtitle_label.setSizePolicy(sizePolicy)
    font = QFont()
    font.setFamily("Muller")
    font.setPointSize(12)
    subtitle_label.setFont(font)
    subtitle_label.setStyleSheet("color: #BFC8D3;")
    subtitle_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    subtitle_label.setWordWrap(True)

    wrap.addWidget(title_label)
    wrap.addWidget(subtitle_label)

    readArticleBtn = QtWidgets.QPushButton("Читать новость")
    readArticleBtn.setMinimumSize(QtCore.QSize(180, 40))
    readArticleBtn.setMaximumSize(QtCore.QSize(180, 40))
    font = QFont()
    font.setFamily("Muller Regular")
    font.setPointSize(11)
    readArticleBtn.setFont(font)
    readArticleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    readArticleBtn.setStyleSheet('''QPushButton{
    color: rgb(255, 255, 255);
    background-color: #2C88F0;
    border-radius: 8px;
    border: 0px solid #094065;
}
QPushButton::hover{
    background-color: #237DE3;}''')
    readArticleBtn.clicked.connect(lambda: open_link(url))
    wrap.addWidget(readArticleBtn)
    card_layout.addLayout(wrap)

    # Устанавливаем layout в фрейм карточки
    card_frame.setLayout(card_layout)

    return card_frame

'''Получение данных статьи для карточки по articleID'''
def get_article_card_data(id) -> list:
    data = []
    sqlite_connection = sqlite3.connect('echo_database.db')
    cursor = sqlite_connection.cursor()

    select = f"""SELECT title, subtitle FROM article WHERE articleID = {id};"""
    cursor.execute(select)
    title_subtitle = cursor.fetchone()
    data.append(title_subtitle)

    other_data_select = f"""SELECT publish.publish_name, category.category_name, article.article_date, article.article_time FROM publish, article, category
                            WHERE articleID = {id} AND article.publishID = publish.publishID AND article.categoryID = category.categoryID;"""

    cursor.execute(other_data_select)
    other_data = cursor.fetchone()
    date =  transform_date(other_data[2])

    other_data_new = other_data[:2] + (date,) + other_data[3:]
    data.append(other_data_new)

    title = data[0][0]
    subtitle = data[0][1]
    other = '    |    '.join(data[1])

    select = f"""SELECT article_link FROM article WHERE articleID = {id};"""
    cursor.execute(select)
    url = cursor.fetchone()

    select = f"""SELECT image FROM article WHERE articleID = {id};"""
    cursor.execute(select)
    image = cursor.fetchone()
    blob_image = image[0]
    png_data = blob_to_png(blob_image)

    data = [title, subtitle, other, url[0], png_data]
    return data

'''Формирование списка id из sql запроса request'''
def get_ids(request) -> list:
    ids = []
    sqlite_connection = sqlite3.connect('echo_database.db')
    cursor = sqlite_connection.cursor()

    cursor.execute(request)
    id_list = cursor.fetchall()
    for id in id_list:
        ids.append(id[0])

    cursor.connection.close()

    return ids

class ArticlesWidget(QWidget):
    scrollStyle = f'''QScrollArea {{
                                        border: none;
                                        }}
                                        /* VERTICAL SCROLLBAR */
                                         QScrollBar:vertical {{
                                            border: none;
                                            background: rgb(255, 255, 255);
                                            width: 14px;
                                            margin: 15px 0 15px 0;
                                            border-radius: 0px;
                                         }}

                                        /*  HANDLE BAR VERTICAL */
                                        QScrollBar::handle:vertical {{	
                                            background-color: rgb(154, 198, 249);
                                            min-height: 30px;
                                            border-radius: 7px;
                                        }}
                                        QScrollBar::handle:vertical:hover{{	
                                            background-color: rgb(177, 213, 255);
                                        }}
                                        QScrollBar::handle:vertical:pressed {{	
                                            background-color: rgb(177, 213, 255);
                                        }}

                                        /* BTN TOP - SCROLLBAR */
                                        QScrollBar::sub-line:vertical {{
                                            border: none;
                                            background-color: rgb(255, 255, 255);
                                            height: 15px;
                                            border-top-left-radius: 7px;
                                            border-top-right-radius: 7px;
                                            subcontrol-position: top;
                                            subcontrol-origin: margin;
                                        }}
                                        QScrollBar::sub-line:vertical:hover {{	
                                            background-color: rgb(255, 255, 255);
                                        }}
                                        QScrollBar::sub-line:vertical:pressed {{	
                                            background-color: rgb(177, 213, 255);
                                        }}

                                        /* BTN BOTTOM - SCROLLBAR */
                                        QScrollBar::add-line:vertical {{
                                            border: none;
                                            background-color: rgb(255, 255, 255);
                                            height: 15px;
                                            border-bottom-left-radius: 7px;
                                            border-bottom-right-radius: 7px;
                                            subcontrol-position: bottom;
                                            subcontrol-origin: margin;
                                        }}
                                        QScrollBar::add-line:vertical:hover {{	
                                            background-color: rgb(255, 255, 255);
                                        }}
                                        QScrollBar::add-line:vertical:pressed {{	
                                            background-color: rgb(177, 213, 255);
                                        }}

                                        /* RESET ARROW */
                                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                                            background: none;
                                        }}
                                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                                            background: none;
                                        }}'''
    def __init__(self, id_request):
        super().__init__()

        self.idRequest = id_request

        # Основной вертикальный layout
        self.main_layout = QVBoxLayout()

        # Создание QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(ArticlesWidget.scrollStyle)

        # Внутренний виджет для scroll area
        self.scroll_area_content = QWidget()
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setContentsMargins(64, 0, 64, 0)

        self.article_layout = QVBoxLayout()
        self.article_layout.setContentsMargins(0, 0, 0, 0)
        self.article_layout.setSpacing(16)
        self.scroll_area_layout.addLayout(self.article_layout)
        self.scroll_area_content.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_content)

        self.load_more_layout = QVBoxLayout()
        self.load_more_layout.setContentsMargins(64, 64, 64, 64)

        self.load_more_btn = QPushButton("ЗАГРУЗИТЬ ЕЩЁ")
        self.load_more_btn.setMinimumSize(QtCore.QSize(164, 56))
        font = QFont()
        font.setFamily("Muller Light")
        font.setPointSize(9)
        self.load_more_btn.setFont(font)
        self.load_more_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load_more_btn.setStyleSheet('''QPushButton{color: rgb(0, 0, 0);
                                    background-color: #C7E0FD;
                                    border-radius: 28px;                     /* <----  40px  */ 
                                    border: 0px solid #094065;}
                                    QPushButton::hover{
                                    background-color: #B1D5FF;}''')

        self.load_more_btn.clicked.connect(self.load_more_news)
        self.load_more_layout.addWidget(self.load_more_btn)

        self.load_initial_news()
        self.scroll_area_layout.addLayout(self.load_more_layout)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)


    start = 0
    end = 10

    def load_initial_news(self):
        global start
        global end
        self.load_news()  # Загружаем 5 новостей изначально
        self.start += 10
        self.end += 10

    def load_more_news(self):
        global start
        global end

        self.load_news()  # Загружаем ещё 5 новостей
        self.start += 10
        self.end += 10

    def load_news(self):
        global start
        global end

        ids = get_ids(self.idRequest)
        for i in (ids)[self.start:self.end]:
            data = get_article_card_data(i)
            news_card = create_news_card(data[0],
                                         data[1],
                                         data[2],
                                         data[3],
                                         data[4])
            self.article_layout.addWidget(news_card)
        self.scroll_area.update()


class subArticlesWidget(QWidget):
    def __init__(self, id_request, title_request):
        super().__init__()

        self.idRequest = id_request

        sqlite_connection = sqlite3.connect('echo_database.db')
        cursor = sqlite_connection.cursor()

        cursor.execute(title_request)

        title = cursor.fetchone()[0]
        cursor.connection.close()

        # Основной вертикальный layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)

        # Создание QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet('''QScrollArea {
                                border: none;
                                }
                                /* VERTICAL SCROLLBAR */
                                 QScrollBar:vertical {
                                    border: none;
                                    background: rgb(255, 255, 255);
                                    width: 14px;
                                    margin: 15px 0 15px 0;
                                    border-radius: 0px;
                                 }

                                /*  HANDLE BAR VERTICAL */
                                QScrollBar::handle:vertical {	
                                    background-color: rgb(154, 198, 249);
                                    min-height: 30px;
                                    border-radius: 7px;
                                }
                                QScrollBar::handle:vertical:hover{	
                                    background-color: rgb(177, 213, 255);
                                }
                                QScrollBar::handle:vertical:pressed {	
                                    background-color: rgb(177, 213, 255);
                                }

                                /* BTN TOP - SCROLLBAR */
                                QScrollBar::sub-line:vertical {
                                    border: none;
                                    background-color: rgb(255, 255, 255);
                                    height: 15px;
                                    border-top-left-radius: 7px;
                                    border-top-right-radius: 7px;
                                    subcontrol-position: top;
                                    subcontrol-origin: margin;
                                }
                                QScrollBar::sub-line:vertical:hover {	
                                    background-color: rgb(255, 255, 255);
                                }
                                QScrollBar::sub-line:vertical:pressed {	
                                    background-color: rgb(177, 213, 255);
                                }

                                /* BTN BOTTOM - SCROLLBAR */
                                QScrollBar::add-line:vertical {
                                    border: none;
                                    background-color: rgb(255, 255, 255);
                                    height: 15px;
                                    border-bottom-left-radius: 7px;
                                    border-bottom-right-radius: 7px;
                                    subcontrol-position: bottom;
                                    subcontrol-origin: margin;
                                }
                                QScrollBar::add-line:vertical:hover {	
                                    background-color: rgb(255, 255, 255);
                                }
                                QScrollBar::add-line:vertical:pressed {	
                                    background-color: rgb(177, 213, 255);
                                }

                                /* RESET ARROW */
                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                    background: none;
                                }
                                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                    background: none;
                                }''')

        # Внутренний виджет для scroll area
        self.scroll_area_content = QWidget()
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setContentsMargins(64, 32, 64, 0)
        self.scroll_area_layout.setSpacing(16)

        self.categoryLabelLayout = QHBoxLayout()
        self.categoryLabelLayout.setContentsMargins(64, 0, 64, 0)

        self.categoryLabel = QLabel(title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoryLabel.sizePolicy().hasHeightForWidth())
        self.categoryLabel.setSizePolicy(sizePolicy)
        self.categoryLabel.setMinimumSize(60, 60)
        font = QFont()
        font.setFamily("Muller Light")
        font.setPointSize(24)
        self.categoryLabel.setFont(font)
        self.categoryLabel.setStyleSheet('''QLabel{ color: #2C88F0; border-bottom: 1px solid #E5F1FF;}''')
        self.categoryLabelLayout.addWidget(self.categoryLabel)
        self.main_layout.addLayout(self.categoryLabelLayout)

        #
        self.article_layout = QVBoxLayout()

        self.scroll_area_layout.addLayout(self.article_layout)
        self.scroll_area_content.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_content)

        #
        self.load_more_layout = QVBoxLayout()
        self.load_more_layout.setContentsMargins(64, 32, 64, 32)

        self.load_more_btn = QPushButton("ЗАГРУЗИТЬ ЕЩЁ")
        self.load_more_btn.setMinimumSize(QtCore.QSize(164, 56))
        font = QFont()
        font.setFamily("Muller Light")
        font.setPointSize(9)
        self.load_more_btn.setFont(font)
        self.load_more_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load_more_btn.setStyleSheet('''color: rgb(0, 0, 0);
                                    background-color: rgb(229, 241, 255);
                                    border-radius: 28px;                     /* <----  40px  */ 
                                    border: 0px solid #094065;''')

        self.load_more_btn.clicked.connect(self.load_more_news)
        self.load_more_layout.addWidget(self.load_more_btn)

        self.load_initial_news()
        self.scroll_area_layout.addLayout(self.load_more_layout)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)


    start = 0
    end = 10

    def load_initial_news(self):
        global start
        global end
        self.load_news()  # Загружаем 5 новостей изначально
        self.start += 10
        self.end += 10
    def load_more_news(self):
        global start
        global end

        self.load_news()  # Загружаем ещё 5 новостей
        self.start += 10
        self.end += 10

    def load_news(self):
        global start
        global end

        ids = get_ids(self.idRequest)
        for i in (ids)[self.start:self.end]:
            data = get_article_card_data(i)
            news_card = create_news_card(data[0],
                                         data[1],
                                         data[2],
                                         data[3],
                                         data[4])
            self.article_layout.addWidget(news_card)
        self.scroll_area.update()
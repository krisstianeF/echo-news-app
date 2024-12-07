from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QScrollArea,
                             QFrame, QLabel, QPushButton, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize
import webbrowser
import os
from blob import blob_to_png, crop_image
from style import Style
from dbModel import Model


class ArticlesWidget(QWidget):
    favorite_button = None
    read_later_button = None

    def __init__(self, id_request, title_request, id):
        super().__init__()

        self.db = Model()

        self.idRequest = id_request
        self.titleRequest = title_request
        self.id = id

        # Основной вертикальный layout
        self.main_layout = QVBoxLayout()

        # Создание QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(Style.scrollStyle)

        # Внутренний виджет для scroll area
        self.scroll_area_content = QWidget()
        self.scroll_area_content.setStyleSheet(f'''QWidget{{ background-color: rgba(0, 0, 0, 0);}}''')
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setContentsMargins(64, 16, 64, 16)

        if self.titleRequest != None:
            self.add_category_label_layout()

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
        self.load_more_btn.setFont(Style.font("Muller Light", 9))
        self.load_more_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load_more_btn.setStyleSheet(f'''QPushButton{{color: {Style.black};
                                    background-color: {Style.blue50};
                                    border-radius: 28px;
                                    border: 0px solid;}}
                                    QPushButton::hover{{
                                    background-color: {Style.blue40};}}''')

        self.load_more_btn.clicked.connect(self.load_more_news)
        self.load_more_layout.addWidget(self.load_more_btn)

        self.load_initial_news()
        self.scroll_area_layout.addLayout(self.load_more_layout)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

    ''' Создание интерфейса карточки новости '''
    @classmethod
    def create_news_card(cls, title, subtitle, other_data, url, png_data):
        # Создание фрейма для карточки новости
        card_frame = QFrame()
        card_frame.setStyleSheet(f"background-color: {Style.white}; border-radius: 16px;")

        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        wrap = QVBoxLayout()

        # Добавление изображения в карточку if png_data != None:
        """if png_data != None:
            # изображение
            imageButton = QPushButton()
            sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            sizePolicy.setHeightForWidth(imageButton.sizePolicy().hasHeightForWidth())
            imageButton.setSizePolicy(sizePolicy)
            # imageButton.setMinimumSize(QtCore.QSize(250, 180))
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
            crop_image('article_image.png', 'article_image.png', 300, 200, 16)

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap('article_image.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            imageButton.setIcon(icon)
            imageButton.setIconSize(QtCore.QSize(300, 200))

            # Удаление файла
            if os.path.exists('article_image.png'):
                os.remove('article_image.png')

            card_layout.addWidget(imageButton)"""

        # Лейбл для других данных и кнопки
        other_data_layout = QHBoxLayout()

        other_data_label = QLabel(other_data)
        other_data_label.setFont(Style.font("Muller", 9))
        other_data_label.setStyleSheet(f"color: {Style.blue100};")
        other_data_layout.addWidget(other_data_label)

        # Добавляем горизонтальный спейсер
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        other_data_layout.addItem(spacer)

        # Кнопки
        icon_size = 32

        ArticlesWidget.favorite_button = QPushButton()
        ArticlesWidget.favorite_button.setIcon(QIcon("gui/icons/heart.png"))
        ArticlesWidget.favorite_button.setIconSize(QSize(icon_size, icon_size))
        ArticlesWidget.favorite_button.setFixedSize(icon_size, icon_size)
        ArticlesWidget.favorite_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        ArticlesWidget.favorite_button.setStyleSheet('''QPushButton:hover {
        icon: url(gui/icons/heart2.png);
        }''')

        ArticlesWidget.read_later_button = QPushButton()
        ArticlesWidget.read_later_button.setIcon(QIcon("gui/icons/bookmark.png"))
        ArticlesWidget.read_later_button.setIconSize(QSize(icon_size, icon_size))
        ArticlesWidget.read_later_button.setFixedSize(icon_size, icon_size)
        ArticlesWidget.read_later_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        ArticlesWidget.read_later_button.setStyleSheet('''QPushButton:hover {
        icon: url(gui/icons/bookmark2.png);}''')

        ArticlesWidget.favorite_button.clicked.connect(cls.like)
        ArticlesWidget.read_later_button.clicked.connect(cls.read_later)

        other_data_layout.addWidget(ArticlesWidget.favorite_button)
        other_data_layout.addWidget(ArticlesWidget.read_later_button)

        # Добавляем layout с кнопками в основной layout карточки
        wrap.addLayout(other_data_layout)

        # Лейблы для заголовка и подзаголовка
        title_label = QLabel(title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(title_label.sizePolicy().hasHeightForWidth())
        title_label.setSizePolicy(sizePolicy)
        title_label.setFont(Style.font("Muller Light", 16))
        title_label.setWordWrap(True)

        subtitle_label = QLabel(subtitle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(subtitle_label.sizePolicy().hasHeightForWidth())
        subtitle_label.setSizePolicy(sizePolicy)
        subtitle_label.setFont(Style.font("Muller", 12))
        subtitle_label.setStyleSheet(f"color: {Style.grey};")
        subtitle_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        subtitle_label.setWordWrap(True)

        wrap.addWidget(title_label)
        wrap.addWidget(subtitle_label)

        readArticleBtn = QtWidgets.QPushButton("Читать новость")
        readArticleBtn.setMinimumSize(QtCore.QSize(180, 40))
        readArticleBtn.setMaximumSize(QtCore.QSize(180, 40))
        readArticleBtn.setFont(Style.font("Muller", 11))
        readArticleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        readArticleBtn.setStyleSheet(f'''QPushButton{{
        color: {Style.white};
        background-color: {Style.blue100};
        border-radius: 8px;
        border: 0px solid;
    }}
    QPushButton::hover{{
        background-color: {Style.blue110};}}''')
        readArticleBtn.clicked.connect(lambda: cls.open_link(url))
        wrap.addWidget(readArticleBtn)
        card_layout.addLayout(wrap)

        # Устанавливаем layout в фрейм карточки
        card_frame.setLayout(card_layout)

        return card_frame


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

        if self.id != None:
            ids = self.db.get_category_ids(self.idRequest, self.id)
        else:
            ids = self.db.get_ids(self.idRequest)

        for i in (ids)[self.start:self.end]:
            data = self.db.get_article_card_data(i)
            news_card = ArticlesWidget.create_news_card(data[0],
                                         data[1],
                                         data[2],
                                         data[3],
                                         data[4])
            self.article_layout.addWidget(news_card)
        self.scroll_area.update()

    def add_category_label_layout(self):
        title = self.db.get_one(self.titleRequest, self.id)

        self.categoryLabelLayout = QHBoxLayout()
        self.categoryLabelLayout.setContentsMargins(64, 8, 64, 8)

        self.categoryLabel = QLabel(title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(self.categoryLabel.sizePolicy().hasHeightForWidth())
        self.categoryLabel.setSizePolicy(sizePolicy)
        self.categoryLabel.setMinimumSize(60, 60)
        self.categoryLabel.setFont(Style.font("Muller Light", 24))
        self.categoryLabel.setStyleSheet(f'''QLabel{{ color: {Style.blue100}; border-bottom: 2px solid {Style.blue60};}}''')

        self.categoryLabelLayout.addWidget(self.categoryLabel)
        self.main_layout.addLayout(self.categoryLabelLayout)

    @classmethod
    def open_link(cls, url):
        if url:
            webbrowser.open(url)

    @classmethod
    def like(cls):
        cls.show_message_box('echo', 'Чтобы добавить статью в список "Избранное" сначала войдите или зарегистрируйтесь.')

    @classmethod
    def read_later(cls):
        cls.show_message_box('echo', 'Чтобы добавить статью в список "Читать позже" сначала войдите или зарегистрируйтесь.')

    @classmethod
    def show_message_box(cls, title, message, icon=QMessageBox.Information):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
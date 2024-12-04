from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
import datetime
import sqlite3
from cards import ArticlesWidget
from style import Style


class Window(QMainWindow):
    horizontalLayout = None

    def __init__(self):
        super().__init__()
        self.resize(1400, 900)
        self.setMinimumSize(QtCore.QSize(1400, 640))
        self.setStyleSheet(f"QMainWindow{{ background-color: {Style.blue20}}};")
        self.setWindowTitle("echo")

        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        Window.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        Window.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.centralwidget.setLayout(Window.horizontalLayout)


        '''-----------------mainWnd------------------'''

        self.main_widget = MainWidget()
        Window.horizontalLayout.addWidget(self.main_widget)

    def setMainWidget(self):
        self.clear_layout(self.layout)
        self.main = MainWidget()
        Window.horizontalLayout.addWidget(self.main)

    def setUserMainWidget(self):
        self.clear_layout(self.layout)
        main = MainWidget()
        MainWidget.createUserMainWidget()
        Window.horizontalLayout.addWidget(main)


class MainWidget(QWidget):
    profileButton = None
    articleLayout = None
    horizontalLayout = None

    def __init__(self):
        super().__init__()
        MainWidget.horizontalLayout = QtWidgets.QHBoxLayout()
        MainWidget.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(MainWidget.horizontalLayout)


        '''______________________main menu_________________________'''

        self.menuFrame = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuFrame.sizePolicy().hasHeightForWidth())
        self.menuFrame.setSizePolicy(sizePolicy)
        self.menuFrame.setMinimumSize(QtCore.QSize(255, 0))
        self.menuFrame.setBaseSize(QtCore.QSize(228, 0))
        self.menuFrame.setStyleSheet(f"background-color: {Style.white};")
        self.menuFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menuFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.menuLayout = QtWidgets.QVBoxLayout(self.menuFrame)
        self.menuLayout.setContentsMargins(32, -1, 16, -1)


        self.main_btn_style = '''QPushButton{
                            color: rgb(255, 255, 255);
                            background-color: rgb(44, 136, 240);
                            border-radius: 28px;   
                            border: 0px solid #094065;
                            }
                            QPushButton:hover {
                            background-color: #237DE3;
                            }'''

        self.mainButton = QtWidgets.QPushButton("echo")
        self.mainButton.setMinimumSize(QtCore.QSize(164, 56))
        self.mainButton.setFont(Style.font("Cruinn", 14))
        self.mainButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mainButton.setStyleSheet(self.main_btn_style)

        self.menuLayout.addWidget(self.mainButton)

        MainWidget.profileButton = QtWidgets.QPushButton(self.menuFrame)
        MainWidget.profileButton.setMinimumSize(QtCore.QSize(164, 56))
        MainWidget.profileButton.setFont(Style.font("Muller Light", 12))
        MainWidget.profileButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        MainWidget.profileButton.setStyleSheet("QPushButton{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(229, 241, 255);\n"
"    border-radius: 28px;                     /* <----  40px  */ \n"
"    border: 0px solid #094065;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: #C7E0FD;}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui\\icons/profile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWidget.profileButton.setIcon(icon)
        MainWidget.profileButton.setIconSize(QtCore.QSize(28, 28))
        MainWidget.profileButton.setText("Вход")
        self.menuLayout.addWidget(MainWidget.profileButton)

        spacerItem = QtWidgets.QSpacerItem(20, 16, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.menuLayout.addItem(spacerItem)

        hot_icon = QtGui.QIcon()
        hot_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/hot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hotButton = self.create_category_btn(1, hot_icon)
        self.menuLayout.addWidget(self.hotButton)

        recent_icon = QtGui.QIcon()
        recent_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/recent.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.recentButton = self.create_category_btn(2, recent_icon)
        self.menuLayout.addWidget(self.recentButton)

        spacerItem1 = QtWidgets.QSpacerItem(20, 16, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.menuLayout.addItem(spacerItem1)

        self.categoryGroup = QtWidgets.QGroupBox(self.menuFrame)
        self.categoryGroup.setFont(Style.font("Muller Light", 10))
        self.categoryGroup.setStyleSheet('''QGroupBox{ color: #9AC6F9; border: 0px solid;}''')
        self.categoryLayout = QtWidgets.QVBoxLayout(self.categoryGroup)
        self.categoryLayout.setContentsMargins(0, 32, 0, 32)
        self.categoryLayout.setSpacing(8)
        self.categoryGroup.setTitle("Разделы")

        politic_icon = QtGui.QIcon()
        politic_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/earth.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.politicButton = self.create_category_btn(3, politic_icon)
        self.categoryLayout.addWidget(self.politicButton)

        economy_icon = QtGui.QIcon()
        economy_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/coin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.economyButton = self.create_category_btn(4, economy_icon)
        self.categoryLayout.addWidget(self.economyButton)

        culture_icon = QtGui.QIcon()
        culture_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/masks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cultureButton = self.create_category_btn(5, culture_icon)
        self.categoryLayout.addWidget(self.cultureButton)

        sport_icon = QtGui.QIcon()
        sport_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/cup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sportButton = self.create_category_btn(6, sport_icon)
        self.categoryLayout.addWidget(self.sportButton)

        science_icon = QtGui.QIcon()
        science_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/science.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scienceButton = self.create_category_btn(7, science_icon)
        self.categoryLayout.addWidget(self.scienceButton)

        health_icon = QtGui.QIcon()
        health_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/health.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.healthButton = self.create_category_btn(8, health_icon)
        self.categoryLayout.addWidget(self.healthButton)

        games_icon = QtGui.QIcon()
        games_icon.addPixmap(QtGui.QPixmap("gui\\icons/category/gamepad.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.gamesButton = self.create_category_btn(9, games_icon)
        self.categoryLayout.addWidget(self.gamesButton)

        self.menuLayout.addWidget(self.categoryGroup)

        spacerItem4 = QtWidgets.QSpacerItem(20, 16, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.menuLayout.addItem(spacerItem4)

        self.publishGroup = QtWidgets.QGroupBox(self.menuFrame)
        self.publishGroup.setFont(Style.font("Muller Light", 10))
        self.publishGroup.setStyleSheet('''QGroupBox{ color: #9AC6F9; border: 0px solid;}''')
        self.publishGroup.setTitle("Издательства")

        self.publishLayout = QtWidgets.QVBoxLayout(self.publishGroup)
        self.publishLayout.setContentsMargins(0, 32, 0, 32)
        self.publishLayout.setSpacing(8)

        riaIcon = QtGui.QIcon()
        riaIcon.addPixmap(QtGui.QPixmap("gui\\icons/publish/ria.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.riaButton = self.create_publish_btn(1, riaIcon)
        self.publishLayout.addWidget(self.riaButton)

        aifIcon = QtGui.QIcon()
        aifIcon.addPixmap(QtGui.QPixmap("gui\\icons/publish/aif.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aifButton = self.create_publish_btn(2, aifIcon)
        self.publishLayout.addWidget(self.aifButton)

        tassIcon = QtGui.QIcon()
        tassIcon.addPixmap(QtGui.QPixmap("gui\\icons/publish/tass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tassButton = self.create_publish_btn(3, tassIcon)
        self.publishLayout.addWidget(self.tassButton)

        self.menuLayout.addWidget(self.publishGroup)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.menuLayout.addItem(spacerItem2)


        MainWidget.horizontalLayout.addWidget(self.menuFrame)
        self.mainFrame = QtWidgets.QFrame(self)
        self.mainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.mainLayout = QtWidgets.QVBoxLayout(self.mainFrame)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)


        '''______________________top_menu_________________________'''

        self.topMenuFrame = QtWidgets.QFrame(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topMenuFrame.sizePolicy().hasHeightForWidth())
        self.topMenuFrame.setSizePolicy(sizePolicy)
        self.topMenuFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topMenuFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topMenuLayout = QtWidgets.QHBoxLayout(self.topMenuFrame)
        self.topMenuLayout.setContentsMargins(64, 32, 64, 16)


        self.serchFrame = QtWidgets.QFrame(self.topMenuFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serchFrame.sizePolicy().hasHeightForWidth())

        self.serchFrame.setSizePolicy(sizePolicy)
        self.serchFrame.setStyleSheet("background-color: rgb(255, 255, 255); border: 1px solid #C7E0FD; border-radius: 20px;")
        self.serchFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.serchFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.searchLayout = QtWidgets.QHBoxLayout(self.serchFrame)
        self.searchLayout.setContentsMargins(0, 0, 0, 0)

        self.search_icon = QtWidgets.QPushButton(self.serchFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_icon.sizePolicy().hasHeightForWidth())
        self.search_icon.setSizePolicy(sizePolicy)
        self.search_icon.setMinimumSize(QtCore.QSize(40, 40))
        self.search_icon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_icon.setStyleSheet("border: 0px solid;")
        self.search_icon.setText("")
        searchIcon = QtGui.QIcon()
        searchIcon.addPixmap(QtGui.QPixmap("gui\\icons/Search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_icon.setIcon(searchIcon)
        self.search_icon.setIconSize(QtCore.QSize(32, 32))
        self.searchLayout.addWidget(self.search_icon)

        self.lineEdit = QtWidgets.QLineEdit(self.serchFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setFont(Style.font("Muller Light", 10))
        self.lineEdit.setStyleSheet("border: 0px solid;")
        self.searchLayout.addWidget(self.lineEdit)

        self.topMenuLayout.addWidget(self.serchFrame)

        self.find_btn = QtWidgets.QPushButton(self.topMenuFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.find_btn.sizePolicy().hasHeightForWidth())
        self.find_btn.setSizePolicy(sizePolicy)
        self.find_btn.setMinimumSize(QtCore.QSize(120, 40))
        self.find_btn.setFont(Style.font("Muller Regular", 10))
        self.find_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.find_btn.setStyleSheet('''QPushButton{
        color: rgb(255, 255, 255); 
        background-color: rgb(44, 136, 240); 
        border-radius: 20px; 
        border: 0px solid #094065;}
        QPushButton::hover{
        background-color: #237DE3;}''')
        self.topMenuLayout.addWidget(self.find_btn)

        self.find_btn.setText("Найти")

        self.comboBoxFrame = QtWidgets.QFrame(self.topMenuFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFrame.sizePolicy().hasHeightForWidth())
        self.comboBoxFrame.setSizePolicy(sizePolicy)
        self.comboBoxFrame.setMinimumSize(QtCore.QSize(116, 40))
        self.comboBoxFrame.setStyleSheet("background-color: rgb(229, 241, 255); border-radius: 20px;")
        self.comboBoxFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.comboBoxFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.comboBoxLayout = QtWidgets.QHBoxLayout(self.comboBoxFrame)
        self.comboBoxLayout.setContentsMargins(16, 6, 16, 6)

        self.comboBox = QtWidgets.QComboBox(self.comboBoxFrame)
        self.comboBox.setMinimumSize(QtCore.QSize(116, 20))
        self.comboBox.setFont(Style.font("Muller Light", 10))
        self.comboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setStyleSheet("QComboBox {\n"
"    background-color: #E5F1FF; /* Цвет фона */\n"
"    color: #000000;          /* Цвет текста */\n"
"    border: 0px solid #E5F1FF; /* Рамка */\n"
"    border-radius: 20px;       /* Скругленные углы */\n"
"    padding: 5px;            /* Отступы */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #C7E0FD;\n"
"    border-radius: 10px; /* Скругление выпадающего списка */\n"
"    selection-background-color: #C7E0FD; /* Цвет выделения */\n"
"    selection-color: black; /* Цвет текста выделенного элемента */\n"
"    padding: 5px;            /* Отступы */\n"
"    spacing: 5px;\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 20px;\n"
"    border-left: 0px solid #cccccc; /* Граница выпадающего списка */\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(gui/icons/arrow down.png); /* Замените на свой путь к картинке */\n"
"}")
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtCurrent)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox.setIconSize(QtCore.QSize(40, 40))
        self.comboBox.setDuplicatesEnabled(False)
        self.comboBox.setFrame(True)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBoxLayout.addWidget(self.comboBox)
        self.topMenuLayout.addWidget(self.comboBoxFrame)
        self.mainLayout.addWidget(self.topMenuFrame)

        self.comboBox.setCurrentText("За день")
        self.comboBox.setItemText(0, "За день")
        self.comboBox.setItemText(1, "За неделю")
        self.comboBox.setItemText(2, "За месяц")
        self.comboBox.setItemText(3, "За год")


        self.articleFrame = QtWidgets.QFrame(self.mainFrame)
        self.articleFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.articleFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        MainWidget.articleLayout = QtWidgets.QVBoxLayout(self.articleFrame)
        self.mainLayout.addWidget(self.articleFrame)
        MainWidget.horizontalLayout.addWidget(self.mainFrame)

        self.setLayout(MainWidget.horizontalLayout)

        self.set_all_cards()
        self.mainButton.clicked.connect(self.set_all_cards)

        self.hotButton.clicked.connect(self.set_hot_cards)
        self.recentButton.clicked.connect(self.set_recent_cards)
        self.politicButton.clicked.connect(self.set_politic_cards)
        self.economyButton.clicked.connect(self.set_economy_cards)
        self.cultureButton.clicked.connect(self.set_culture_cards)
        self.sportButton.clicked.connect(self.set_sport_cards)
        self.scienceButton.clicked.connect(self.set_science_cards)
        self.healthButton.clicked.connect(self.set_health_cards)
        self.gamesButton.clicked.connect(self.set_games_cards)

        self.riaButton.clicked.connect(self.set_ria_cards)
        self.aifButton.clicked.connect(self.set_aif_cards)
        self.tassButton.clicked.connect(self.set_tass_cards)

        MainWidget.profileButton.clicked.connect(self.set_login_layout)


    '''Создание кнопок категорий'''
    def create_category_btn(self, id, icon):
        sqlite_connection = sqlite3.connect('echo_database.db')
        cursor = sqlite_connection.cursor()
        request = f"""SELECT category_name FROM category WHERE categoryID = {id}"""
        cursor.execute(request)
        category_name = cursor.fetchone()[0]
        cursor.connection.close()

        self.Button = QtWidgets.QPushButton(category_name)
        self.Button.setMinimumSize(QtCore.QSize(0, 40))
        self.Button.setMaximumSize(QtCore.QSize(210, 40))
        self.Button.setFont(Style.font("Muller Light", 10))
        self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Button.setStyleSheet("QPushButton {\n"
                                      "    background-color: white; /* Белый фон */\n"
                                      "    border-radius: 20px; /* Скругление углов */\n"
                                      "    padding: 8px; /* Внутренние отступы */\n"
                                      "    text-align: left; /* Выравнивание текста слева */\n"
                                      "}\n"
                                      "QPushButton::icon {\n"
                                      "    padding-right: 8px; /* Отступ между иконкой и текстом */\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton::hover {\n"
                                      "    background-color: #F1F8FF; /* Цвет фона при наведении */\n"
                                      "}\n"
                                      "QPushButton::pressed {\n"
                                      "    background-color: #F1F8FF; /* Цвет фона при наведении */}\n")
        self.Button.setIcon(icon)
        self.Button.setIconSize(QtCore.QSize(32, 32))
        return self.Button
    def create_publish_btn(self, id, icon):
        sqlite_connection = sqlite3.connect('echo_database.db')
        cursor = sqlite_connection.cursor()
        request = f"""SELECT publish_name FROM publish WHERE publishID = {id}"""
        cursor.execute(request)
        publish_name = cursor.fetchone()[0]
        cursor.connection.close()

        self.Button = QtWidgets.QPushButton(publish_name)
        self.Button.setMinimumSize(QtCore.QSize(0, 40))
        self.Button.setMaximumSize(QtCore.QSize(210, 40))
        self.Button.setFont(Style.font("Muller Light", 10))
        self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Button.setStyleSheet("QPushButton {\n"
                                      "    background-color: white; /* Белый фон */\n"
                                      "    border-radius: 20px; /* Скругление углов */\n"
                                      "    padding: 8px; /* Внутренние отступы */\n"
                                      "    text-align: left; /* Выравнивание текста слева */\n"
                                      "}\n"
                                      "QPushButton::icon {\n"
                                      "    padding-right: 8px; /* Отступ между иконкой и текстом */\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton::hover {\n"
                                      "    background-color: #F1F8FF; /* Цвет фона при наведении */\n"
                                      "}\n"
                                      "QPushButton::pressed {\n"
                                      "    background-color: #F1F8FF; /* Цвет фона при наведении */}\n")
        self.Button.setIcon(icon)
        self.Button.setIconSize(QtCore.QSize(32, 32))
        return self.Button

    '''Загрузка всех карточек'''
    def set_all_cards(self):
        self.clear_layout(MainWidget.articleLayout)

        id_request = """SELECT articleID FROM article ORDER BY article_date DESC;"""
        # Создание и добавление виджета с карточками
        articles_widget = ArticlesWidget(id_request, None)
        MainWidget.articleLayout.addWidget(articles_widget)

    '''Функции для кнопок разделов'''
    def set_hot_cards(self):
        today = datetime.date.today()
        two_day_ago = today - datetime.timedelta(days=2)
        self.clear_layout(MainWidget.articleLayout)
        id_request = f"""SELECT articleID, article_date FROM article WHERE article_date >= {two_day_ago} ORDER BY article_date DESC;"""
        title_request = """SELECT category_name FROM category WHERE categoryID = 1;"""
        articles_widget = ArticlesWidget(id_request, title_request)
        MainWidget.articleLayout.addWidget(articles_widget)
    def set_recent_cards(self):
        today = datetime.date.today()
        two_day_ago = today - datetime.timedelta(days = 2)
        self.clear_layout(MainWidget.articleLayout)
        id_request = f"""SELECT articleID, article_date FROM article WHERE article_date >= {two_day_ago} ORDER BY article_date DESC;"""
        title_request = """SELECT category_name FROM category WHERE categoryID = 2;"""
        articles_widget = ArticlesWidget(id_request, title_request)
        MainWidget.articleLayout.addWidget(articles_widget)
    def set_politic_cards(self):
        self.clear_layout(MainWidget.articleLayout)
        id_request = """SELECT articleID FROM article WHERE categoryID = 3 ORDER BY article_date DESC;"""
        title_request = """SELECT category_name FROM category WHERE categoryID = 3;"""
        articles_widget = ArticlesWidget(id_request, title_request)
        MainWidget.articleLayout.addWidget(articles_widget)
    def set_economy_cards(self):
        self.clear_layout(MainWidget.articleLayout)
        id_request = """SELECT articleID FROM article WHERE categoryID = 4 ORDER BY article_date DESC;"""
        title_request = """SELECT category_name FROM category WHERE categoryID = 4;"""
        articles_widget = ArticlesWidget(id_request, title_request)
        MainWidget.articleLayout.addWidget(articles_widget)
    def set_culture_cards(self):
        self.clear_layout(MainWidget.articleLayout)
        id_request = """SELECT articleID FROM article WHERE categoryID = 5 ORDER BY article_date DESC;"""
        title_request = """SELECT category_name FROM category WHERE categoryID = 5;"""
        articles_widget = ArticlesWidget(id_request, title_request)
        MainWidget.articleLayout.addWidget(articles_widget)
    def set_sport_cards(self):
        self.clear_layout(MainWidget.articleLayout)
        id_request = """SELECT articleID FROM article WHERE categoryID = 6 ORDER BY article_date DESC;"""
        title_request = """SELECT category_name FROM category WHERE categoryID = 6;"""
        articles_widget = ArticlesWidget(id_request, title_request)
        MainWidget.articleLayout.addWidget(articles_widget)
    def set_science_cards(self):
        self.clear_layout(MainWidget.articleLayout)
        id_request = """SELECT articleID FROM article WHERE categoryID = 7 ORDER BY article_date DESC;"""
        title_request = """SELECT category_name FROM category WHERE categoryID = 7;"""
        articles_widget = ArticlesWidget(id_request, title_request)
        MainWidget.articleLayout.addWidget(articles_widget)
    def set_health_cards(self):
        self.clear_layout(MainWidget.articleLayout)
        id_request = """SELECT articleID FROM article WHERE categoryID = 8 ORDER BY article_date DESC;"""
        title_request = """SELECT category_name FROM category WHERE categoryID = 8;"""
        articles_widget = ArticlesWidget(id_request, title_request)
        MainWidget.articleLayout.addWidget(articles_widget)
    def set_games_cards(self):
            self.clear_layout(MainWidget.articleLayout)
            id_request = """SELECT articleID FROM article WHERE categoryID = 9 ORDER BY article_date DESC;"""
            title_request = """SELECT category_name FROM category WHERE categoryID = 9;"""
            articles_widget = ArticlesWidget(id_request, title_request)
            MainWidget.articleLayout.addWidget(articles_widget)

    '''Функции для кнопок издательств'''
    def set_ria_cards(self):
            self.clear_layout(MainWidget.articleLayout)
            id_request = """SELECT articleID FROM article WHERE publishID = 1 ORDER BY article_date DESC;"""
            title_request = """SELECT publish_name FROM publish WHERE publishID = 1;"""
            articles_widget = ArticlesWidget(id_request, title_request)
            MainWidget.articleLayout.addWidget(articles_widget)
    def set_aif_cards(self):
            self.clear_layout(MainWidget.articleLayout)
            id_request = """SELECT articleID FROM article WHERE publishID = 2 ORDER BY article_date DESC;"""
            title_request = """SELECT publish_name FROM publish WHERE publishID = 2;"""
            articles_widget = ArticlesWidget(id_request, title_request)
            MainWidget.articleLayout.addWidget(articles_widget)
    def set_tass_cards(self):
            self.clear_layout(MainWidget.articleLayout)
            id_request = """SELECT articleID FROM article WHERE publishID = 3 ORDER BY article_date DESC;"""
            title_request = """SELECT publish_name FROM publish WHERE publishID = 3;"""
            articles_widget = ArticlesWidget(id_request, title_request)
            MainWidget.articleLayout.addWidget(articles_widget)

    @classmethod
    def clear_layout(cls, layout):
        if layout is not None:
                for i in reversed(range(layout.count())):
                        widget = layout.itemAt(i).widget()
                        if widget:
                                widget.setParent(None)

    def set_login_layout(self):
        self.clear_layout(MainWidget.horizontalLayout)
        self.login = LoginWidget()
        MainWidget.horizontalLayout.addWidget(self.login)

    '''Открытие профиля пользователя'''
    @classmethod
    def set_profile_widget(cls):
        cls.clear_layout(MainWidget.articleLayout)
        profile = ProfileWidget(1)
        cls.articleLayout.addWidget(profile)

    @classmethod
    def createUserMainWidget(cls):
        if cls.profileButton:
            cls.profileButton.setText("Профиль")
            cls.profileButton.clicked.disconnect()
            cls.profileButton.clicked.connect(cls.set_profile_widget)


class LoginWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(650, 650))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(20)
        self.frame.setFont(font)
        self.frame.setStyleSheet(f"QFrame{{ color: {Style.blue100}; background-color: {Style.white}; border-radius: 32px;}}")
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.entranceLayout = QtWidgets.QVBoxLayout(self.frame)


        self.entranceLayout.setContentsMargins(64, 64, 64, 64)
        self.entranceLayout.setSpacing(32)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.entranceLayout.addItem(spacerItem)

        self.echoFLayout = QtWidgets.QHBoxLayout()
        self.echo = QtWidgets.QPushButton(self.frame)
        self.echo.setText("echo")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.echo.sizePolicy().hasHeightForWidth())
        self.echo.setSizePolicy(sizePolicy)
        self.echo.setMinimumSize(QtCore.QSize(164, 56))
        font = QtGui.QFont()
        font.setFamily("Cruinn")
        font.setPointSize(14)
        self.echo.setFont(font)
        self.echo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.echo.setStyleSheet(f'''QPushButton{{
                                color: {Style.white};
                                background-color: {Style.blue100};
                                border-radius: 28px;
                                }}
                                QPushButton::hover{{
                                background-color: {Style.blue110};
                                }}''')
        self.echoFLayout.addWidget(self.echo)
        self.entranceLayout.addLayout(self.echoFLayout)

        self.usernameLayout = QtWidgets.QVBoxLayout()
        self.usernameLayout.setSpacing(8)
        self.usernameLabel = QtWidgets.QLabel(self.frame)
        self.usernameLabel.setText('Имя пользователя')
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(14)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")
        self.usernameLayout.addWidget(self.usernameLabel)
        self.usernameLineEdit = QtWidgets.QLineEdit(self.frame)
        self.usernameLineEdit.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(10)
        self.usernameLineEdit.setFont(font)
        self.usernameLineEdit.setStyleSheet(Style.lineEditStyle)
        self.usernameLayout.addWidget(self.usernameLineEdit)
        self.entranceLayout.addLayout(self.usernameLayout)

        self.passwordLayout = QtWidgets.QVBoxLayout()
        self.passwordLayout.setSpacing(8)

        self.passwordLabel = QtWidgets.QLabel(self.frame)
        self.passwordLabel.setText('Пароль')
        self.passwordLabel.setFont(Style.font("Muller Light", 14))
        self.passwordLayout.addWidget(self.passwordLabel)

        self.passwordFrame = QFrame(self.frame)
        self.passwordFrame.setMaximumSize(1000, 50)
        self.passwordFrame.setMinimumSize(0, 50)
        self.passwordFrame.setStyleSheet(f'''QFrame{{ color: {Style.black}; 
                                            background-color: {Style.white}; 
                                            border: 1px solid {Style.blue50}; 
                                            border-radius: 25px;
                                            padding-left: 10px;
                                            padding-right: 10px;}}''')
        self.passwordFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.passwordFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.passwordLayout2 = QHBoxLayout(self.frame)
        self.passwordLayout2.setContentsMargins(0, 5, 0, 5)

        self.passwordLineEdit = QtWidgets.QLineEdit(self.passwordFrame)
        self.passwordLineEdit.setMaximumSize(QtCore.QSize(1000, 46))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(10)
        self.passwordLineEdit.setFont(font)
        self.passwordLineEdit.setStyleSheet(
            '''QLineEdit{ color: #000000; background-color: #ffffff; border: 0px solid #B1D5FF; border-radius: 23px;
            padding-left: 10px;
            padding-right: 10px;}''')
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLayout2.addWidget(self.passwordLineEdit)

        self.hideButton = QPushButton(self.passwordFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.hideButton.sizePolicy().hasHeightForWidth())
        self.hideButton.setSizePolicy(sizePolicy)
        self.hideButton.setMinimumSize(QtCore.QSize(40, 40))
        self.hideButton.setMaximumSize(QtCore.QSize(40, 40))
        self.hideButton.setStyleSheet('''QPushButton{ background-color: #ffffff; border: 0px solid #B1D5FF; border-radius: 20px;
            padding-left: 10px;
            padding-right: 10px;}
            QPushButton::hover{
            background-color: #E5F1FF;}''')
        self.hideButton.setIcon(QIcon('gui/icons/eyeClosed.png'))
        self.hideButton.setIconSize(QSize(24, 24))
        self.hideButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.passwordLayout2.addWidget(self.hideButton)
        self.passwordFrame.setLayout(self.passwordLayout2)
        self.passwordLayout.addWidget(self.passwordFrame)
        self.entranceLayout.addLayout(self.passwordLayout)

        self.enterBtnLayout = QVBoxLayout()
        self.enterBtnLayout.setSpacing(16)

        self.enterButton = QtWidgets.QPushButton(self.frame)
        self.enterButton.setText('Войти')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.enterButton.sizePolicy().hasHeightForWidth())
        self.enterButton.setSizePolicy(sizePolicy)
        self.enterButton.setMinimumSize(QtCore.QSize(164, 56))
        font = QtGui.QFont()
        font.setFamily("Cruinn")
        font.setPointSize(12)
        self.enterButton.setFont(font)
        self.enterButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.enterButton.setStyleSheet(f'''QPushButton{{
                                        color: {Style.white};
                                        background-color: {Style.blue100};
                                        border-radius: 28px;
                                        border: 0px solid #094065;
                                        }}
                                        QPushButton::hover{{
                                        background-color: {Style.blue110}
                                        }}''')
        self.enterBtnLayout.addWidget(self.enterButton)

        self.errorFlag = False

        self.entranceLayout.addLayout(self.enterBtnLayout)
        self.textUnderLayout = QtWidgets.QVBoxLayout()
        self.textUnderLayout.setContentsMargins(0, 0, 0, 0)
        self.textUnderLayout.setSpacing(8)

        self.label_under_form = QtWidgets.QLabel('Если еще нет аккаунта, ты можешь')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.label_under_form.sizePolicy().hasHeightForWidth())
        self.label_under_form.setSizePolicy(sizePolicy)
        self.label_under_form.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(14)
        self.label_under_form.setFont(font)
        self.label_under_form.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_under_form.setWordWrap(True)
        self.textUnderLayout.addWidget(self.label_under_form)

        self.registrationBtn = QPushButton(self.frame)
        self.registrationBtn.setText("зарегистрироваться!")
        self.registrationBtn.setFont(font)
        self.registrationBtn.setStyleSheet('''color: #2C88F0;
                                           background-color: #ffffff;
                                           border: 0px solid #094065;
                                           text-decoration: underline;''')
        self.registrationBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textUnderLayout.addWidget(self.registrationBtn)
        self.entranceLayout.addLayout(self.textUnderLayout)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.entranceLayout.addItem(spacerItem)

        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)


        self.echo.clicked.connect(self.setMainWidget)
        self.hideButton.clicked.connect(self.toggle_visibility)
        self.enterButton.clicked.connect(self.enter)
        self.registrationBtn.clicked.connect(self.startRegistration)

        self.is_visible = False

    def setMainWidget(self):
        self.clear_layout(self.layout)
        self.main = MainWidget()
        self.layout.addWidget(self.main)
    def setUserMainWidget(self):
        self.clear_layout(self.layout)
        main = MainWidget()
        MainWidget.createUserMainWidget()
        self.layout.addWidget(main)

    def enter(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        if self.check_credentials(username, password):
            self.setUserMainWidget()
        else:
            if not self.errorFlag:
                self.usernameLabel.setText('Имя пользователя *')
                self.passwordLabel.setText('Пароль *')
                self.usernameLabel.setStyleSheet(f'color: {Style.error}')
                self.passwordLabel.setStyleSheet(f'color: {Style.error}')

                self.usernameLineEdit.setStyleSheet(f'''
                color: #000000; 
                background-color: #ffffff; 
                border: 1px solid {Style.error}; 
                border-radius: 25px;
                padding-left: 20px;
                padding-right: 20px;''')
                self.passwordFrame.setStyleSheet(f'''
                color: #000000; 
                background-color: #ffffff; 
                border: 1px solid {Style.error}; 
                border-radius: 25px;
                padding-left: 10px;
                padding-right: 10px;''')
                self.errorLabel = QLabel('* Неправильный логин или пароль')
                self.errorLabel.setStyleSheet(f'''color: {Style.error};''')
                self.errorLabel.setFont(Style.font("Muller Light", 12))
                self.errorLabel.setAlignment(Qt.AlignCenter)
                self.enterBtnLayout.addWidget(self.errorLabel)
                self.errorFlag = True

    def check_credentials(self, username, password):
        conn = sqlite3.connect('echo_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username=? AND user_password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None


    def startRegistration(self):
        self.clear_layout(self.layout)
        regWidget1 = RegistrationWidget()
        self.layout.addWidget(regWidget1)



    def clear_layout(self, layout):
        if layout is not None:
                for i in reversed(range(layout.count())):
                        widget = layout.itemAt(i).widget()
                        if widget:
                                widget.setParent(None)
    def toggle_visibility(self):
        if self.is_visible:
            self.passwordLineEdit.setEchoMode(QLineEdit.Password)
            self.hideButton.setIcon(QIcon('gui/icons/eyeClosed.png'))

        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
            self.hideButton.setIcon(QIcon('gui/icons/eyeOpened.png'))

        self.is_visible = not self.is_visible


class RegistrationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.is_visible = False
        self.selected_avatar = None
        self.selected_button = None

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setFont(Style.font("Muller Light", 14))
        self.stacked_widget.setMaximumSize(QtCore.QSize(650, 650))

        # Создаем страницы для каждого этапа регистрации
        self.page1 = self.create_page1()
        self.page2 = self.create_page2()
        self.page3 = self.create_page3()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame(self)
        self.frame.setStyleSheet(
            f"QFrame{{ color: {Style.blue100}; background-color: {Style.white}; border-radius: 32px;}}")
        self.frame.setFont(Style.font("Muller Light", 14))
        self.frame.setMaximumSize(QtCore.QSize(700, 650))
        self.frameLayout = QVBoxLayout(self.frame)
        self.frameLayout.setContentsMargins(64, 64, 64, 64)
        self.frameLayout.setSpacing(32)

        self.echoLayout = QtWidgets.QHBoxLayout()
        self.echo = QtWidgets.QPushButton("echo", self.frame)
        self.echo.clicked.connect(self.setMainWidget)
        self.echo.setMinimumSize(QtCore.QSize(164, 56))
        self.echo.setMaximumSize(QtCore.QSize(164, 56))
        self.echo.setFont(Style.font("Cruinn", 14))
        self.echo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.echo.setStyleSheet(f'''QPushButton{{  
                                        color: {Style.white};  
                                        background-color: {Style.blue100};  
                                        border-radius: 28px;                                }}  
                                        QPushButton::hover{{  
                                        background-color: {Style.blue110};  
                                        }}''')
        self.echoLayout.addWidget(self.echo)

        self.layout.addWidget(self.frame)
        self.frameLayout.addLayout(self.echoLayout)
        self.frameLayout.addWidget(self.stacked_widget)

        self.setLayout(self.layout)


    def create_page1(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(32)

        progressLayout = QHBoxLayout()
        progressLayout.setSpacing(12)

        progressBtn1 = QPushButton()
        progressBtn1.setStyleSheet(f'''background-color: {Style.blue100};border-radius: 3px; border: 0px solid;''')
        progressBtn1.setMinimumHeight(6)
        progressBtn1.setMaximumHeight(6)

        progressBtn2 = QPushButton()
        progressBtn2.setStyleSheet(
            f'''background-color: {Style.white};border-radius: 3px; border: 1px solid {Style.blue40};''')
        progressBtn2.setMinimumHeight(6)
        progressBtn2.setMaximumHeight(6)

        progressBtn3 = QPushButton()
        progressBtn3.setStyleSheet(
            f'''background-color: {Style.white};border-radius: 3px; border: 1px solid {Style.blue40};''')
        progressBtn3.setMinimumHeight(6)
        progressBtn3.setMaximumHeight(6)

        progressLayout.addWidget(progressBtn1)
        progressLayout.addWidget(progressBtn2)
        progressLayout.addWidget(progressBtn3)

        layout.addLayout(progressLayout)

        self.nameLabel = QtWidgets.QLabel('Как тебя зовут?')
        self.nameLabel.setFont(Style.font("Muller Light", 14))

        self.usernameLabel = QtWidgets.QLabel('Придумай себе уникальное имя пользователя *')
        self.usernameLabel.setFont(Style.font("Muller Light", 14))

        self.name_input = QLineEdit(self)
        self.name_input.setMinimumSize(QtCore.QSize(0, 50))
        self.name_input.setFont(Style.font("Muller Light", 10))
        self.name_input.setStyleSheet(Style.lineEditStyle)

        self.username_input = QLineEdit(self)
        self.username_input.setMinimumSize(QtCore.QSize(0, 50))
        self.username_input.setFont(Style.font("Muller Light", 10))
        self.username_input.setStyleSheet(Style.lineEditStyle)

        self.error_label1 = QLabel('* Имя пользователя должно содержать только латинские символы и цифры', self)
        self.error_label1.setFont(Style.font("Muller Light", 12))
        self.error_label1.setStyleSheet(f"color: {Style.blue100};")
        self.error_label1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.error_label1.setWordWrap(True)

        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(32)

        self.next_button1 = QPushButton('Продолжить', self)
        self.next_button1.clicked.connect(self.validate_page1)
        self.next_button1.setMinimumHeight(56)
        self.next_button1.setFont(Style.font("Muller", 12))
        self.next_button1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next_button1.setStyleSheet(f'''QPushButton{{  
                                                color: {Style.white};  
                                                background-color: {Style.blue100};  
                                                border-radius: 28px;
                                                }}  
                                                QPushButton::hover{{  
                                                background-color: {Style.blue110}  
                                                }}''')

        self.back_button1 = QPushButton('Назад', self)
        self.back_button1.clicked.connect(self.back_to_login)
        self.back_button1.setMinimumSize(QSize(160, 56))
        self.back_button1.setMaximumSize(QSize(160, 56))
        self.back_button1.setFont(Style.font("Muller", 12))
        self.back_button1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.back_button1.setStyleSheet(f'''QPushButton{{  
                                                color: {Style.blue100};  
                                                background-color: {Style.blue40};  
                                                border-radius: 28px;
                                                }}  
                                                QPushButton::hover{{  
                                                background-color: {Style.blue30}  
                                                }}''')

        nameLayout = QVBoxLayout()
        nameLayout.setSpacing(8)
        nameLayout.addWidget(self.nameLabel)
        nameLayout.addWidget(self.name_input)

        usernameLayout = QVBoxLayout()
        usernameLayout.setSpacing(8)
        usernameLayout.addWidget(self.usernameLabel)
        usernameLayout.addWidget(self.username_input)

        buttonLayout.addWidget(self.back_button1)
        buttonLayout.addWidget(self.next_button1)

        layout.addLayout(nameLayout)
        layout.addLayout(usernameLayout)

        layout.addLayout(buttonLayout)
        layout.addWidget(self.error_label1)

        page.setLayout(layout)
        return page

    def create_page2(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(32)

        progressLayout = QHBoxLayout()
        progressLayout.setSpacing(12)

        progressBtn1 = QPushButton()
        progressBtn1.setStyleSheet(f'''background-color: {Style.blue100}; border-radius: 3px; border: 0px solid;''')
        progressBtn1.setMinimumHeight(6)
        progressBtn1.setMaximumHeight(6)

        progressBtn2 = QPushButton()
        progressBtn2.setStyleSheet(
            f'''background-color: {Style.blue100}; border-radius: 3px; border: 0px solid;''')
        progressBtn2.setMinimumHeight(6)
        progressBtn2.setMaximumHeight(6)

        progressBtn3 = QPushButton()
        progressBtn3.setStyleSheet(
            f'''background-color: {Style.white}; border-radius: 3px; border: 1px solid {Style.blue40};''')
        progressBtn3.setMinimumHeight(6)
        progressBtn3.setMaximumHeight(6)

        progressLayout.addWidget(progressBtn1)
        progressLayout.addWidget(progressBtn2)
        progressLayout.addWidget(progressBtn3)

        layout.addLayout(progressLayout)

        self.passwordFrame1 = QFrame(self)
        self.passwordFrame1.setMaximumSize(1000, 50)
        self.passwordFrame1.setMinimumSize(0, 50)
        self.passwordFrame1.setStyleSheet(Style.passwordFrameStyle)

        self.inputLayout1 = QHBoxLayout(self.passwordFrame1)
        self.inputLayout1.setContentsMargins(0, 5, 0, 5)

        self.password_input = QLineEdit(self)
        self.password_input.setStyleSheet('''QLineEdit{ 
            color: #000000; 
            background-color: #ffffff; 
            border: 0px solid; 
            border-radius: 23px;  
            padding-left: 10px;
            padding-right: 10px;}''')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(Style.font("Muller Light", 10))

        self.hideButton1 = QPushButton(self.passwordFrame1)
        self.hideButton1.setMinimumSize(QtCore.QSize(40, 40))
        self.hideButton1.setMaximumSize(QtCore.QSize(40, 40))
        self.hideButton1.setStyleSheet('''QPushButton{ 
        background-color: #ffffff; 
        border: 0px solid; 
        border-radius: 20px;  
        padding-left: 10px;                    
        padding-right: 10px;}                    
        QPushButton::hover{                    
        background-color: #E5F1FF;
        }''')
        self.hideButton1.setIcon(QIcon('gui/icons/eyeClosed.png'))
        self.hideButton1.setIconSize(QSize(24, 24))
        self.hideButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hideButton1.clicked.connect(self.toggle_visibility1)
        self.inputLayout1.addWidget(self.password_input)
        self.inputLayout1.addWidget(self.hideButton1)

        self.passwordFrame2 = QFrame(self)
        self.passwordFrame2.setMaximumSize(1000, 50)
        self.passwordFrame2.setMinimumSize(0, 50)
        self.passwordFrame2.setStyleSheet(Style.passwordFrameStyle)

        self.inputLayout2 = QHBoxLayout(self.passwordFrame2)
        self.inputLayout2.setContentsMargins(0, 5, 0, 5)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setStyleSheet('''QLineEdit{ 
            color: #000000; 
            background-color: #ffffff; 
            border: 0px solid; 
            border-radius: 23px;  
            padding-left: 10px;
            padding-right: 10px;}''')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setFont(Style.font("Muller Light", 10))

        self.hideButton2 = QPushButton(self.passwordFrame2)
        self.hideButton2.setMinimumSize(QtCore.QSize(40, 40))
        self.hideButton2.setMaximumSize(QtCore.QSize(40, 40))
        self.hideButton2.setStyleSheet('''QPushButton{ 
        background-color: #ffffff; 
        border: 0px solid; 
        border-radius: 20px;  
        padding-left: 10px;                    
        padding-right: 10px;}                    
        QPushButton::hover{                    
        background-color: #E5F1FF;
        }''')
        self.hideButton2.setIcon(QIcon('gui/icons/eyeClosed.png'))
        self.hideButton2.setIconSize(QSize(24, 24))
        self.hideButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hideButton2.clicked.connect(self.toggle_visibility2)
        self.inputLayout2.addWidget(self.confirm_password_input)
        self.inputLayout2.addWidget(self.hideButton2)

        passwordLayout1 = QVBoxLayout()
        passwordLayout1.setSpacing(8)
        passwordLayout2 = QVBoxLayout()
        passwordLayout2.setSpacing(8)

        self.passwordLabel1 = QtWidgets.QLabel('Придумай пароль *')
        self.passwordLabel1.setFont(Style.font("Muller Light", 14))
        self.passwordLabel2 = QtWidgets.QLabel('И продублируй его *')
        self.passwordLabel2.setFont(Style.font("Muller Light", 14))

        passwordLayout1.addWidget(self.passwordLabel1)
        passwordLayout1.addWidget(self.passwordFrame1)
        passwordLayout2.addWidget(self.passwordLabel2)
        passwordLayout2.addWidget(self.passwordFrame2)

        buttonLayout2 = QHBoxLayout()
        buttonLayout2.setSpacing(32)

        self.next_button2 = QPushButton('Продолжить', self)
        self.next_button2.setMinimumHeight(56)
        self.next_button2.setFont(Style.font("Muller", 12))
        self.next_button2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next_button2.setStyleSheet(f'''QPushButton{{  
                                                        color: {Style.white};  
                                                        background-color: {Style.blue100};  
                                                        border-radius: 28px;
                                                        }}  
                                                        QPushButton::hover{{  
                                                        background-color: {Style.blue110}  
                                                        }}''')

        self.back_button2 = QPushButton('Назад', self)
        self.back_button2.setMinimumSize(QSize(160, 56))
        self.back_button2.setMaximumSize(QSize(160, 56))
        self.back_button2.setFont(Style.font("Muller", 12))
        self.back_button2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.back_button2.setStyleSheet(f'''QPushButton{{  
                                                        color: {Style.blue100};  
                                                        background-color: {Style.blue40};  
                                                        border-radius: 28px;
                                                        }}  
                                                        QPushButton::hover{{  
                                                        background-color: {Style.blue30}  
                                                        }}''')

        buttonLayout2.addWidget(self.back_button2)
        buttonLayout2.addWidget(self.next_button2)

        self.error_label2 = QLabel('* Пароль должен содержать не менее 6 символов', self)
        self.error_label2.setFont(Style.font("Muller Light", 12))
        self.error_label2.setStyleSheet(f"color: {Style.blue100};")
        self.error_label2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.error_label2.setWordWrap(True)

        self.next_button2.clicked.connect(self.validate_page2)
        self.back_button2.clicked.connect(self.prev_page)

        layout.addLayout(passwordLayout1)
        layout.addLayout(passwordLayout2)
        layout.addLayout(buttonLayout2)
        layout.addWidget(self.error_label2)

        page.setLayout(layout)
        return page

    def create_page3(self):
        page = QWidget()
        layout = QVBoxLayout()

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(Style.scrollStyle)

        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)

        self.avatar_buttons = []

        for i in range(1, 17):
            avatar_button = QPushButton()
            avatar_button.setCheckable(True)
            pixmap = QPixmap(f'gui/avatars/avatar_{i}.png')
            icon = QIcon(pixmap)
            avatar_button.setIcon(icon)
            avatar_button.setIconSize(pixmap.size())
            avatar_button.clicked.connect(self.on_avatar_selected)
            avatar_button.setProperty('avatar_id', i)
            scroll_layout.addWidget(avatar_button, (i-1) // 4, (i-1) % 4)
            self.avatar_buttons.append(avatar_button)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)


        buttonLayout3 = QHBoxLayout(self)
        buttonLayout3.setSpacing(32)

        self.finish_button = QPushButton('Завершить', self)
        self.finish_button.setMinimumHeight(56)
        self.finish_button.setFont(Style.font("Muller", 12))
        self.finish_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.finish_button.setStyleSheet(f'''QPushButton{{  
                                                        color: {Style.white};  
                                                        background-color: {Style.blue100};  
                                                        border-radius: 28px;
                                                        }}  
                                                        QPushButton::hover{{  
                                                        background-color: {Style.blue110}  
                                                        }}''')

        self.back_button3 = QPushButton('Назад', self)
        self.back_button3.setMinimumSize(QSize(160, 56))
        self.back_button3.setMaximumSize(QSize(160, 56))
        self.back_button3.setFont(Style.font("Muller", 12))
        self.back_button3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.back_button3.setStyleSheet(f'''QPushButton{{  
                                                        color: {Style.blue100};  
                                                        background-color: {Style.blue40};  
                                                        border-radius: 28px;
                                                        }}  
                                                        QPushButton::hover{{  
                                                        background-color: {Style.blue30}  
                                                        }}''')

        buttonLayout3.addWidget(self.back_button3)
        buttonLayout3.addWidget(self.finish_button)


        self.back_button3.clicked.connect(self.prev_page)
        self.finish_button.clicked.connect(self.finish_registration)

        label = QLabel('Выберите аватар:')
        label.setFont(Style.font("Muller Light", 16))
        layout.addWidget(label)
        layout.addWidget(scroll_area)
        layout.addLayout(buttonLayout3)

        page.setLayout(layout)
        return page

    def validate_page1(self):
        import re
        name = self.name_input.text()
        username = self.username_input.text()

        if not name and not username:
            self.error_label1.setText("* Имя и имя пользователя пользователя не должны быть пустыми.")
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            self.usernameLabel.setStyleSheet(f"color: {Style.error}")
            self.username_input.setStyleSheet(Style.lineEditStyleError)
            self.nameLabel.setStyleSheet(f"color: {Style.error}")
            self.name_input.setStyleSheet(Style.lineEditStyleError)
            return

        elif not name:
            self.nameLabel.setStyleSheet(f"color: {Style.error}")
            self.name_input.setStyleSheet(Style.lineEditStyleError)
            self.error_label1.setText("* Имя не должно быть пустым.")
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            return

        elif not username:
            self.usernameLabel.setStyleSheet(f"color: {Style.error}")
            self.username_input.setStyleSheet(Style.lineEditStyleError)
            self.error_label1.setText("* Имя пользователя не должно быть пустым.")
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            return

        else:
            self.name_input.setStyleSheet(Style.lineEditStyle)
            self.nameLabel.setStyleSheet(f"color: {Style.blue100}")
            self.username_input.setStyleSheet(Style.lineEditStyle)
            self.usernameLabel.setStyleSheet(f"color: {Style.blue100}")
            self.error_label1.setStyleSheet(f'color: {Style.blue100}')

        if not username or not re.match(r'^[a-zA-Z0-9.]+$', username):
            self.username_input.setStyleSheet(Style.lineEditStyleError)
            self.usernameLabel.setStyleSheet(f'color: {Style.error}')
            self.error_label1.setText(
                "* Имя пользователя должно содержать только буквы латинского алфавита, цифры и точки.")
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            return
        else:
            self.username_input.setStyleSheet(Style.lineEditStyle)
            self.usernameLabel.setStyleSheet(f"color: {Style.blue100}")
            self.error_label1.setStyleSheet(f'color: {Style.blue100}')

        if not self.is_login_unique(username):
            self.username_input.setStyleSheet(Style.lineEditStyleError)
            self.error_label1.setText("* Логин уже занят.")
            self.usernameLabel.setStyleSheet(f'color: {Style.error}')
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            return
        else:
            self.username_input.setStyleSheet(Style.lineEditStyle)
            self.usernameLabel.setStyleSheet(f"color: {Style.blue100}")
            self.error_label1.setStyleSheet(f'color: {Style.blue100}')

        self.error_label1.setText(
            "* Имя пользователя должно содержать только буквы латинского алфавита, цифры и точки.")
        self.next_page()

    def validate_page2(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if len(password) < 6:
            self.passwordFrame1.setStyleSheet(Style.passwordFrameStyleError)
            self.passwordLabel1.setStyleSheet(f'color: {Style.error}')
            self.passwordFrame2.setStyleSheet(Style.passwordFrameStyleError)
            self.passwordLabel2.setStyleSheet(f'color: {Style.error}')
            self.error_label2.setStyleSheet(f'color: {Style.error}')
            self.error_label2.setText("* Пароль должен содержать не менее 6 символов.")
            return
        else:
            self.passwordFrame1.setStyleSheet(Style.passwordFrameStyle)
            self.passwordLabel1.setStyleSheet(f'color: {Style.blue100}')
            self.passwordFrame2.setStyleSheet(Style.passwordFrameStyle)
            self.passwordLabel2.setStyleSheet(f'color: {Style.blue100}')
            self.error_label2.setStyleSheet(f'color: {Style.blue100}')

        if password != confirm_password:
            self.passwordFrame1.setStyleSheet(Style.passwordFrameStyleError)
            self.passwordFrame2.setStyleSheet(Style.passwordFrameStyleError)
            self.passwordLabel1.setStyleSheet(f'color: {Style.error}')
            self.passwordLabel2.setStyleSheet(f'color: {Style.error}')
            self.error_label2.setText("* Пароли не совпадают.")
            self.error_label2.setStyleSheet(f'color: {Style.error}')
            return
        else:
            self.passwordFrame1.setStyleSheet(Style.passwordFrameStyle)
            self.passwordFrame2.setStyleSheet(Style.passwordFrameStyle)
            self.passwordLabel1.setStyleSheet(f'color: {Style.blue100}')
            self.passwordLabel2.setStyleSheet(f'color: {Style.blue100}')
            self.error_label2.setStyleSheet(f'color: {Style.blue100}')

        self.error_label2.setText("* Пароль должен содержать не менее 8 символов")
        self.next_page()

    def is_login_unique(self, login):
        conn = sqlite3.connect('echo_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE username = ?", (login,))
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0

    def next_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)

    def prev_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)

    def finish_registration(self):
        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if self.selected_avatar is not None:
            avatar = self.selected_avatar
            print(f'Выбранный аватар: {self.selected_avatar}')
        else:
            print('Аватар не выбран')

        # Здесь можно добавить логику сохранения данных регистрации
        print(
            f"Регистрация завершена:\nИмя пользователя: {name}\nЛогин: {username}\nПароль: {password}\nАватар: {avatar}")

    def back_to_login(self):
        self.clear_layout(self.layout)
        login = LoginWidget()
        self.layout.addWidget(login)

    def setMainWidget(self):
        self.clear_layout(self.layout)
        self.main = MainWidget()
        self.layout.addWidget(self.main)

    def setUserMainWidget(self):
        self.clear_layout(self.layout)
        main = MainWidget()
        MainWidget.createUserMainWidget()
        self.layout.addWidget(main)

    def clear_layout(self, layout):
        if layout is not None:
                for i in reversed(range(layout.count())):
                        widget = layout.itemAt(i).widget()
                        if widget:
                                widget.setParent(None)
    def toggle_visibility1(self):
        if self.is_visible:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.hideButton1.setIcon(QIcon('gui/icons/eyeClosed.png'))

        else:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.hideButton1.setIcon(QIcon('gui/icons/eyeOpened.png'))

        self.is_visible = not self.is_visible

    def toggle_visibility2(self):
        if self.is_visible:
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.hideButton2.setIcon(QIcon('gui/icons/eyeClosed.png'))

        else:
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
            self.hideButton2.setIcon(QIcon('gui/icons/eyeOpened.png'))

        self.is_visible = not self.is_visible

    def on_avatar_selected(self):
        button = self.sender()
        if self.selected_button:
            self.selected_button.setChecked(False)
        self.selected_button = button
        self.selected_avatar = button.property('avatar_id')
        print(f'Выбран аватар: {self.selected_avatar}')

    def on_finish_clicked(self):
        if self.selected_avatar is not None:
            print(f'Выбранный аватар: {self.selected_avatar}')
        else:
            print('Аватар не выбран')



class ProfileWidget(QWidget):
    layout = None
    def __init__(self, ID):
        super().__init__()

        self.id = ID
        sqlite_connection = sqlite3.connect('echo_database.db')
        cursor = sqlite_connection.cursor()

        select = f"""SELECT name, username FROM user WHERE userID = {self.id};"""
        select_avatar = f"""SELECT avatarPath FROM avatar, user WHERE user.avatarID = avatar.avatarID AND userID = {self.id}"""
        cursor.execute(select)

        user = cursor.fetchone()
        self.name = user[0]
        self.username = '@' + user[1]

        cursor.execute(select_avatar)
        avatar = cursor.fetchone()
        avatar_path = avatar[0]

        cursor.close()


        ProfileWidget.layout = QVBoxLayout()
        ProfileWidget.layout.setContentsMargins(64, 0, 64, 0)

        ProfileWidget.layout = QtWidgets.QVBoxLayout(self)
        ProfileWidget.layout.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet(Style.scrollStyle)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setStyleSheet(f'''QWidget{{ background-color: {Style.blue20};}}''')
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1377, 1256))

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(64, 0, 64, 0)

        self.profileFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.profileFrame.setMinimumSize(QtCore.QSize(0, 1256))
        self.profileFrame.setMaximumSize(QtCore.QSize(16777215, 1256))
        self.profileFrame.setStyleSheet("QFrame{\n"
                                        "background-color: #ffffff;\n"
                                        "border: 0px solid;\n"
                                        "border-radius: 32px;}\n"
                                        "")

        self.mainLayout = QtWidgets.QVBoxLayout(self.profileFrame)
        self.mainLayout.setContentsMargins(64, 64, 64, 64)
        self.mainLayout.setSpacing(32)

        self.firstLayout = QtWidgets.QHBoxLayout()
        self.firstLayout.setSpacing(32)

        self.avatarBtn = QtWidgets.QPushButton(self.profileFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.avatarBtn.sizePolicy().hasHeightForWidth())
        self.avatarBtn.setSizePolicy(sizePolicy)
        self.avatarBtn.setMinimumSize(QtCore.QSize(96, 96))
        self.avatarBtn.setMaximumSize(QtCore.QSize(96, 96))
        font = QtGui.QFont()
        font.setFamily("Cruinn")
        font.setPointSize(12)
        self.avatarBtn.setFont(font)
        self.avatarBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.avatarBtn.setStyleSheet(f"background-color: {Style.white}; border: 0px solid;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(avatar_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.avatarBtn.setIcon(icon)
        self.avatarBtn.setIconSize(QtCore.QSize(96, 96))
        self.firstLayout.addWidget(self.avatarBtn)
        self.usernameLayout = QtWidgets.QVBoxLayout()
        self.usernameLayout.setSpacing(8)

        self.name1 = QtWidgets.QLabel(self.name)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name1.sizePolicy().hasHeightForWidth())
        self.name1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(24)
        self.name1.setFont(font)
        self.usernameLayout.addWidget(self.name1, 0, QtCore.Qt.AlignTop)

        self.username1 = QtWidgets.QLabel(self.username)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username1.sizePolicy().hasHeightForWidth())
        self.username1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(16)
        self.username1.setFont(font)
        self.username1.setStyleSheet("color: #2C88F0;")
        self.usernameLayout.addWidget(self.username1, 0, QtCore.Qt.AlignTop)
        self.firstLayout.addLayout(self.usernameLayout)
        self.mainLayout.addLayout(self.firstLayout)

        self.listsLayout = QtWidgets.QHBoxLayout()
        self.listsLayout.setSpacing(16)

        self.likeListBtn = QtWidgets.QPushButton('Избранное')
        self.likeListBtn.setMinimumSize(QtCore.QSize(0, 120))
        self.likeListBtn.setMaximumSize(QtCore.QSize(16777215, 120))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(10)
        self.likeListBtn.setFont(font)
        self.likeListBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.likeListBtn.setStyleSheet("QPushButton {\n"
                                       "    color: #2C88F0;\n"
                                       "    background-color: #E5F1FF; /* Белый фон */\n"
                                       "    border-radius: 32px; /* Скругление углов */\n"
                                       "    padding: 32px; /* Внутренние отступы */\n"
                                       "    text-align: left; /* Выравнивание текста слева */\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton::icon {\n"
                                       "    padding-right: 16px; /* Отступ между иконкой и текстом */\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton::hover {\n"
                                       "    background-color: #F1F8FF; /* Цвет фона при наведении */\n"
                                       "}\n"
                                       "\n"
                                       "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("gui\\icons/heart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.likeListBtn.setIcon(icon1)
        self.likeListBtn.setIconSize(QtCore.QSize(32, 32))
        self.listsLayout.addWidget(self.likeListBtn)

        self.readLaterListBtn = QtWidgets.QPushButton('Читать позже')
        self.readLaterListBtn.setMinimumSize(QtCore.QSize(0, 120))
        self.readLaterListBtn.setMaximumSize(QtCore.QSize(16777215, 120))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(10)
        self.readLaterListBtn.setFont(font)
        self.readLaterListBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.readLaterListBtn.setStyleSheet("QPushButton {\n"
                                            "    color: #2C88F0;\n"
                                            "    background-color: #E5F1FF; /* Белый фон */\n"
                                            "    border-radius: 32px; /* Скругление углов */\n"
                                            "    padding: 32px; /* Внутренние отступы */\n"
                                            "    text-align: left; /* Выравнивание текста слева */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton::icon {\n"
                                            "    padding-right: 16px; /* Отступ между иконкой и текстом */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton::hover {\n"
                                            "    background-color: #F1F8FF; /* Цвет фона при наведении */\n"
                                            "}\n"
                                            "\n"
                                            "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("gui\\icons/bookmark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.readLaterListBtn.setIcon(icon2)
        self.readLaterListBtn.setIconSize(QtCore.QSize(32, 32))
        self.listsLayout.addWidget(self.readLaterListBtn)
        self.mainLayout.addLayout(self.listsLayout)

        self.userDataLayout = QtWidgets.QVBoxLayout()
        self.userDataLayout.setSpacing(16)

        self.userDataLadel = QtWidgets.QLabel('Личные данные')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userDataLadel.sizePolicy().hasHeightForWidth())
        self.userDataLadel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(16)
        self.userDataLadel.setFont(font)
        self.userDataLadel.setStyleSheet("color: #2C88F0;")
        self.userDataLayout.addWidget(self.userDataLadel)

        self.nameFrame = QtWidgets.QFrame(self.profileFrame)
        self.nameFrame.setStyleSheet("QFrame{\n"
                                     "background-color: #F1F8FF;\n"
                                     "border: 0 px solid;\n"
                                     "border-radius: 16px;}")
        self.nameFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nameFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.nameLayout = QtWidgets.QHBoxLayout(self.nameFrame)
        self.nameLayout.setContentsMargins(32, 16, 16, 16)
        self.nameLayout.setSpacing(8)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(12)

        self.nameLabel = QtWidgets.QLabel('Публичное имя')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(12)
        self.nameLabel.setFont(font)
        self.nameLabel.setStyleSheet("color: #2C88F0;")
        self.verticalLayout_3.addWidget(self.nameLabel)

        self.name2 = QtWidgets.QLabel(self.name)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name2.sizePolicy().hasHeightForWidth())
        self.name2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(16)
        self.name2.setFont(font)
        self.verticalLayout_3.addWidget(self.name2)
        self.nameLayout.addLayout(self.verticalLayout_3)

        self.changeNameBtn = QtWidgets.QPushButton(self.nameFrame)
        self.changeNameBtn.setMinimumSize(QtCore.QSize(48, 48))
        self.changeNameBtn.setMaximumSize(QtCore.QSize(48, 48))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(10)
        self.changeNameBtn.setFont(font)
        self.changeNameBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.changeNameBtn.setStyleSheet("QPushButton {\n"
                                         "    background-color: #2C88F0; /* Белый фон */\n"
                                         "    border-radius: 12px; /* Скругление углов */\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton::hover {\n"
                                         "    background-color: #237DE3; /* Цвет фона при наведении */\n"
                                         "}\n"
                                         "\n"
                                         "")
        self.changeNameBtn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("gui\\icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.changeNameBtn.setIcon(icon3)
        self.changeNameBtn.setIconSize(QtCore.QSize(24, 24))
        self.nameLayout.addWidget(self.changeNameBtn)
        self.userDataLayout.addWidget(self.nameFrame)

        self.usernameFrame = QtWidgets.QFrame(self.profileFrame)
        self.usernameFrame.setStyleSheet("QFrame{\n"
                                         "background-color: #F1F8FF;\n"
                                         "border: 0 px solid;\n"
                                         "border-radius: 16px;}")
        self.usernameFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.usernameFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.nameLayout_2 = QtWidgets.QHBoxLayout(self.usernameFrame)
        self.nameLayout_2.setContentsMargins(32, 16, 16, 16)
        self.nameLayout_2.setSpacing(8)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(12)

        self.usernameLabel = QtWidgets.QLabel('Имя пользователя')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameLabel.sizePolicy().hasHeightForWidth())
        self.usernameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(12)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setStyleSheet("color: #2C88F0;")
        self.verticalLayout_4.addWidget(self.usernameLabel)

        self.username2 = QtWidgets.QLabel(self.username)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username2.sizePolicy().hasHeightForWidth())
        self.username2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(16)
        self.username2.setFont(font)
        self.verticalLayout_4.addWidget(self.username2)
        self.nameLayout_2.addLayout(self.verticalLayout_4)

        self.changeUsernameBtn = QtWidgets.QPushButton(self.usernameFrame)
        self.changeUsernameBtn.setMinimumSize(QtCore.QSize(48, 48))
        self.changeUsernameBtn.setMaximumSize(QtCore.QSize(48, 48))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(10)
        self.changeUsernameBtn.setFont(font)
        self.changeUsernameBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.changeUsernameBtn.setStyleSheet("QPushButton {\n"
                                             "    background-color: #2C88F0; /* Белый фон */\n"
                                             "    border-radius: 12px; /* Скругление углов */\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton::hover {\n"
                                             "    background-color: #237DE3; /* Цвет фона при наведении */\n"
                                             "}\n"
                                             "\n"
                                             "")
        self.changeUsernameBtn.setText("")
        self.changeUsernameBtn.setIcon(icon3)
        self.changeUsernameBtn.setIconSize(QtCore.QSize(24, 24))
        self.nameLayout_2.addWidget(self.changeUsernameBtn)
        self.userDataLayout.addWidget(self.usernameFrame)
        self.mainLayout.addLayout(self.userDataLayout)

        self.btnsLayout = QtWidgets.QVBoxLayout()
        self.btnsLayout.setSpacing(16)

        self.changePasswordBtn = QtWidgets.QPushButton('Сменить пароль')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.changePasswordBtn.sizePolicy().hasHeightForWidth())
        self.changePasswordBtn.setSizePolicy(sizePolicy)
        self.changePasswordBtn.setMinimumSize(QtCore.QSize(250, 48))
        self.changePasswordBtn.setMaximumSize(QtCore.QSize(16777215, 48))
        font = QtGui.QFont()
        font.setFamily("Muller Regular")
        font.setPointSize(11)
        self.changePasswordBtn.setFont(font)
        self.changePasswordBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.changePasswordBtn.setStyleSheet('''QPushButton{
                                             color: rgb(255, 255, 255);
                                             background-color: rgb(44, 136, 240);
                                             border-radius: 24px;
                                             border: 0px solid;
                                             }
                                             QPushButton::hover{
                                             background-color: #237DE3;}
                                             ''')
        self.btnsLayout.addWidget(self.changePasswordBtn)

        self.exitBtn = QtWidgets.QPushButton('Выйти из аккаунта')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitBtn.sizePolicy().hasHeightForWidth())
        self.exitBtn.setSizePolicy(sizePolicy)
        self.exitBtn.setMinimumSize(QtCore.QSize(250, 48))
        self.exitBtn.setMaximumSize(QtCore.QSize(16777215, 48))
        font = QtGui.QFont()
        font.setFamily("Muller Regular")
        font.setPointSize(11)
        self.exitBtn.setFont(font)
        self.exitBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exitBtn.setStyleSheet("color: #FF56D0;\n"
                                   "background-color: #FFEBF9;\n"
                                   "border-radius: 24px;\n"
                                   "border: 0px solid;")
        self.btnsLayout.addWidget(self.exitBtn)

        self.deleteAccountBtn = QtWidgets.QPushButton('Удалить аккаунт')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteAccountBtn.sizePolicy().hasHeightForWidth())
        self.deleteAccountBtn.setSizePolicy(sizePolicy)
        self.deleteAccountBtn.setMinimumSize(QtCore.QSize(250, 48))
        self.deleteAccountBtn.setMaximumSize(QtCore.QSize(16777215, 48))
        font = QtGui.QFont()
        font.setFamily("Muller Regular")
        font.setPointSize(11)
        self.deleteAccountBtn.setFont(font)
        self.deleteAccountBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deleteAccountBtn.setStyleSheet("color: #FF56D0;\n"
                                            "background-color: #FFEBF9;\n"
                                            "border-radius: 24px;\n"
                                            "border: 0px solid;")
        self.btnsLayout.addWidget(self.deleteAccountBtn)

        self.mainLayout.addLayout(self.btnsLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.profileFrame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        ProfileWidget.layout.addWidget(self.scrollArea)


        self.likeListBtn.clicked.connect(self.set_likeList)
        self.readLaterListBtn.clicked.connect(self.set_readLaterList)

        self.changeNameBtn.clicked.connect(self.changeName)
        self.changeUsernameBtn.clicked.connect(self.changeUserName)

        self.changePasswordBtn.clicked.connect(self.changePassword)
        self.exitBtn.clicked.connect(ProfileWidget.exit)
        self.deleteAccountBtn.clicked.connect(ProfileWidget.deleteAccount)



    def set_likeList(self):
        pass
    def set_readLaterList(self):
        pass
    def changeName(self):
        pass
    def changeUserName(self):
        pass
    def changePassword(self):
        pass

    @classmethod
    def exit(cls):
        MainWidget.clear_layout(Window.horizontalLayout)
        mainWnd = MainWidget()
        Window.horizontalLayout.addWidget(mainWnd)

    @classmethod
    def deleteAccount(cls):
        pass

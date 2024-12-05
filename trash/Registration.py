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

        self.main_widget = RegistrationWidget()
        Window.horizontalLayout.addWidget(self.main_widget)

    def setMainWidget(self):
        '''self.clear_layout(self.layout)
        self.main = MainWidget()
        Window.horizontalLayout.addWidget(self.main)'''
        pass

    def setUserMainWidget(self):
        '''self.clear_layout(self.layout)
        main = MainWidget()
        MainWidget.createUserMainWidget()
        Window.horizontalLayout.addWidget(main)'''
        pass

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

        #self.stacked_widget.addWidget(self.page1)
        #self.stacked_widget.addWidget(self.page2)
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
                                        border-radius: 28px;}}  
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
        self.hideButton1.setIcon(QIcon('../gui/icons/eyeClosed.png'))
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
        self.hideButton2.setIcon(QIcon('../gui/icons/eyeClosed.png'))
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
            f'''background-color: {Style.blue100}; border-radius: 3px; border: 0px solid;''')
        progressBtn3.setMinimumHeight(6)
        progressBtn3.setMaximumHeight(6)

        progressLayout.addWidget(progressBtn1)
        progressLayout.addWidget(progressBtn2)
        progressLayout.addWidget(progressBtn3)

        layout.addLayout(progressLayout)

        scroll_area = QScrollArea(page)
        scroll_area.setStyleSheet(Style.scrollStyle)

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f'''QWidget{{background-color: {Style.blue30}; border-radius: 32px; border: 0px solid;}}''')
        scroll_layout = QGridLayout(scroll_content)

        self.avatar_buttons = []

        for i in range(1, 17):
            avatar_button = QPushButton()
            avatar_button.setCheckable(True)
            avatar_button.setMinimumSize(120, 120)
            avatar_button.setMaximumSize(120, 120)
            pixmap = QPixmap(f'gui/avatars/avatar_{i}.png')
            icon = QIcon(pixmap)
            avatar_button.setIcon(icon)
            avatar_button.setIconSize(QSize(110, 110))
            avatar_button.clicked.connect(self.on_avatar_selected)
            avatar_button.setProperty('avatar_id', i)
            avatar_button.setStyleSheet(f'''
                        QPushButton {{
                            border: 2px solid transparent;
                            border-radius: 60px;
                        }}
                        QPushButton:checked {{
                            border: 3px solid {Style.blue100};
                        }}
                    ''')
            scroll_layout.addWidget(avatar_button, (i - 1) // 4, (i - 1) % 4)
            self.avatar_buttons.append(avatar_button)

        scroll_area.setWidget(scroll_content)

        label = QLabel('Выберите аватар:')
        label.setFont(Style.font("Muller Light", 16))
        layout.addWidget(label)
        layout.addWidget(scroll_area)

        buttonLayout3 = QHBoxLayout()
        buttonLayout3.setSpacing(32)

        self.finish_button = QPushButton('Завершить')
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

        self.back_button3 = QPushButton('Назад')
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
        conn = sqlite3.connect('../echo_database.db')
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
        '''self.clear_layout(self.layout)
        login = LoginWidget()
        self.layout.addWidget(login)'''
        pass

    def setMainWidget(self):
        '''self.clear_layout(self.layout)
        self.main = MainWidget()
        self.layout.addWidget(self.main)'''
        pass

    def setUserMainWidget(self):
        '''self.clear_layout(self.layout)
        main = MainWidget()
        MainWidget.createUserMainWidget()
        self.layout.addWidget(main)'''
        pass

    def clear_layout(self, layout):
        if layout is not None:
                for i in reversed(range(layout.count())):
                        widget = layout.itemAt(i).widget()
                        if widget:
                                widget.setParent(None)
    def toggle_visibility1(self):
        if self.is_visible:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.hideButton1.setIcon(QIcon('../gui/icons/eyeClosed.png'))

        else:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.hideButton1.setIcon(QIcon('../gui/icons/eyeOpened.png'))

        self.is_visible = not self.is_visible

    def toggle_visibility2(self):
        if self.is_visible:
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.hideButton2.setIcon(QIcon('../gui/icons/eyeClosed.png'))

        else:
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
            self.hideButton2.setIcon(QIcon('../gui/icons/eyeOpened.png'))

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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
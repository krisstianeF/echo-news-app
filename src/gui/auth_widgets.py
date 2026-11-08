from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
import sqlite3

from src.style import Style
from src.core.database import Database
from src.gui.articles_widget import ArticlesWidget
from src.config import Assets
from src.config import DB_PATH, ASSETS_DIR
import os

db = Database()

class LoginWidget(QWidget):

    logo = None

    def __init__(self):
        from src.gui.main_window import Window, MainWidget
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(650, 600))
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


        LoginWidget.logo = QtWidgets.QPushButton()
        LoginWidget.logo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        LoginWidget.logo.setMinimumSize(QSize(164, 56))
        LoginWidget.logo.setMaximumSize(QSize(164, 56))

        logo_hover = Assets.LOGO_HOVER.replace('\\', '/')
        LoginWidget.logo.setStyleSheet(f'''QPushButton{{border: 0px solid;}}
                                    QPushButton:hover {{ icon: url("{logo_hover}");}}''')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Assets.LOGO_MONOCOLOR), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        LoginWidget.logo.setIcon(icon)
        LoginWidget.logo.setIconSize(QSize(164, 56))


        self.echoFLayout.addWidget(LoginWidget.logo)
        self.entranceLayout.addLayout(self.echoFLayout)

        self.usernameLayout = QtWidgets.QVBoxLayout()
        self.usernameLayout.setSpacing(8)
        self.usernameLabel = QtWidgets.QLabel(self.frame)
        self.usernameLabel.setText('Логин')
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(14)
        self.usernameLabel.setFont(font)
        self.usernameLayout.addWidget(self.usernameLabel)
        self.usernameLineEdit = QtWidgets.QLineEdit(self.frame)
        self.usernameLineEdit.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Muller Light")
        font.setPointSize(10)
        self.usernameLineEdit.setFont(font)
        self.usernameLineEdit.setStyleSheet(Style.set_line_edit_style(25, True))
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
        self.passwordFrame.setStyleSheet(Style.set_line_edit_frame_style(25, True))
        self.passwordFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.passwordFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.passwordLayout2 = QHBoxLayout(self.frame)
        self.passwordLayout2.setContentsMargins(0, 5, 0, 5)

        self.passwordLineEdit = QtWidgets.QLineEdit(self.passwordFrame)
        self.passwordLineEdit.setMaximumSize(QtCore.QSize(1000, 46))
        self.passwordLineEdit.setFont(Style.font("Muller Light", 10))
        self.passwordLineEdit.setStyleSheet(
            f'''QLineEdit{{ color: {Style.black}; background-color: {Style.white}; border: 0px solid; border-radius: 23px;
            padding-left: 10px;
            padding-right: 10px;}}''')
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLayout2.addWidget(self.passwordLineEdit)

        self.hideButton = QPushButton(self.passwordFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.hideButton.sizePolicy().hasHeightForWidth())
        self.hideButton.setSizePolicy(sizePolicy)
        self.hideButton.setMinimumSize(QtCore.QSize(40, 40))
        self.hideButton.setMaximumSize(QtCore.QSize(40, 40))
        self.hideButton.setStyleSheet(f'''QPushButton{{ background-color: {Style.white}; border: 0px solid; border-radius: 20px;
            padding-left: 10px;
            padding-right: 10px;
            }}
            QPushButton::hover{{
            background-color: {Style.blue20};}}''')
        self.hideButton.setIcon(QIcon(Assets.ICON_EYE_CLOSED))
        self.hideButton.setIconSize(QSize(24, 24))
        self.hideButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.passwordLayout2.addWidget(self.hideButton)
        self.passwordFrame.setLayout(self.passwordLayout2)
        self.passwordLayout.addWidget(self.passwordFrame)
        self.entranceLayout.addLayout(self.passwordLayout)

        self.enterBtnLayout = QVBoxLayout()
        self.enterBtnLayout.setSpacing(8)

        self.enterButton = QtWidgets.QPushButton(self.frame)
        self.enterButton.setText('Войти')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.enterButton.sizePolicy().hasHeightForWidth())
        self.enterButton.setSizePolicy(sizePolicy)
        self.enterButton.setMinimumSize(QtCore.QSize(164, 56))
        self.enterButton.setFont(Style.font("Muller", 12))
        self.enterButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.enterButton.setStyleSheet(f'''QPushButton{{
                                        color: {Style.white};
                                        background-color: {Style.blue100};
                                        border-radius: 28px;
                                        border: 0px solid;
                                        }}
                                        QPushButton::hover{{
                                        background-color: {Style.blue110}
                                        }}''')
        self.enterBtnLayout.addWidget(self.enterButton)

        self.errorLabel = QLabel("")
        self.errorLabel.setStyleSheet(f'''color: {Style.error};''')
        self.errorLabel.setFont(Style.font("Muller Light", 12))
        self.errorLabel.setAlignment(Qt.AlignCenter)
        #self.enterBtnLayout.addWidget(self.errorLabel)

        self.errorFlag = False

        self.entranceLayout.addLayout(self.enterBtnLayout)
        self.textUnderLayout = QtWidgets.QVBoxLayout()
        self.textUnderLayout.setContentsMargins(0, 0, 0, 0)
        self.textUnderLayout.setSpacing(10)

        self.textUnderLayout.addWidget(self.errorLabel)

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
        self.registrationBtn.setStyleSheet(f'''QPushButton{{color: {Style.blue100};
                                           background-color: {Style.white};
                                           border: 0px solid;
                                           text-decoration: underline;
                                           }}
                                           QPushButton::hover{{background-color: {Style.blue100};''')
        self.registrationBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textUnderLayout.addWidget(self.registrationBtn)
        self.entranceLayout.addLayout(self.textUnderLayout)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.entranceLayout.addItem(spacerItem)

        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)


        LoginWidget.logo.clicked.connect(Window.setMainWidget)
        self.hideButton.clicked.connect(self.toggle_visibility)
        self.enterButton.clicked.connect(self.enter)
        self.registrationBtn.clicked.connect(self.startRegistration)

        self.is_visible = False

    def enter(self):
        from src.gui.main_window import Window, MainWidget
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        if self.check_credentials(username, password):
            request = """SELECT userID FROM user WHERE username = ?;"""
            id = db.get_one(request, username)
            Window.setUserMainWidget(id)
        else:
            if not self.errorFlag:
                self.usernameLabel.setText('Имя пользователя *')
                self.passwordLabel.setText('Пароль *')
                self.usernameLabel.setStyleSheet(f'color: {Style.error}')
                self.passwordLabel.setStyleSheet(f'color: {Style.error}')

                self.usernameLineEdit.setStyleSheet(Style.set_line_edit_style(25, False))
                self.passwordFrame.setStyleSheet(Style.set_line_edit_frame_style(25, False))
                self.errorLabel.setText("* Неправильный логин и/или пароль")
                self.errorFlag = True

    def check_credentials(self, username, password):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username=? AND user_password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None


    def startRegistration(self):
        from src.gui.main_window import Window, MainWidget
        Window.clear_layout(self.layout)
        regWidget1 = RegistrationWidget()
        self.layout.addWidget(regWidget1)


    def toggle_visibility(self):
        if self.is_visible:
            self.passwordLineEdit.setEchoMode(QLineEdit.Password)
            self.hideButton.setIcon(QIcon(Assets.ICON_EYE_CLOSED))

        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
            self.hideButton.setIcon(QIcon(Assets.ICON_EYE_OPENED))

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
        self.echoLayout.addWidget(LoginWidget.logo)

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

        self.nameLabel = QtWidgets.QLabel('Как Вас зовут?')
        self.nameLabel.setFont(Style.font("Muller Light", 14))

        self.usernameLabel = QtWidgets.QLabel('Придумайте себе уникальный логин *')
        self.usernameLabel.setFont(Style.font("Muller Light", 14))

        self.name_input = QLineEdit(self)
        self.name_input.setMinimumSize(QtCore.QSize(0, 50))
        self.name_input.setFont(Style.font("Muller Light", 10))
        self.name_input.setStyleSheet(Style.set_line_edit_style(25, True))

        self.username_input = QLineEdit(self)
        self.username_input.setMinimumSize(QtCore.QSize(0, 50))
        self.username_input.setFont(Style.font("Muller Light", 10))
        self.username_input.setStyleSheet(Style.set_line_edit_style(25, True))

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
        self.passwordFrame1.setStyleSheet(Style.set_line_edit_frame_style(25, True))

        self.inputLayout1 = QHBoxLayout(self.passwordFrame1)
        self.inputLayout1.setContentsMargins(0, 5, 0, 5)

        self.password_input = QLineEdit(self)
        self.password_input.setStyleSheet(f'''QLineEdit{{ 
            color: {Style.black}; 
            background-color: {Style.white}; 
            border: 0px solid; 
            border-radius: 23px;  
            padding-left: 10px;
            padding-right: 10px;}}''')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(Style.font("Muller Light", 10))

        self.hideButton1 = QPushButton(self.passwordFrame1)
        self.hideButton1.setMinimumSize(QtCore.QSize(40, 40))
        self.hideButton1.setMaximumSize(QtCore.QSize(40, 40))
        self.hideButton1.setStyleSheet(f'''QPushButton{{ 
        background-color: {Style.white}; 
        border: 0px solid; 
        border-radius: 20px;  
        padding-left: 10px;                    
        padding-right: 10px;
        }}                    
        QPushButton::hover{{                    
        background-color: {Style.blue20};
        }}''')
        self.hideButton1.setIcon(QIcon(Assets.ICON_EYE_CLOSED))
        self.hideButton1.setIconSize(QSize(24, 24))
        self.hideButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hideButton1.clicked.connect(self.toggle_visibility1)
        self.inputLayout1.addWidget(self.password_input)
        self.inputLayout1.addWidget(self.hideButton1)

        self.passwordFrame2 = QFrame(self)
        self.passwordFrame2.setMaximumSize(1000, 50)
        self.passwordFrame2.setMinimumSize(0, 50)
        self.passwordFrame2.setStyleSheet(Style.set_line_edit_frame_style(25, True))

        self.inputLayout2 = QHBoxLayout(self.passwordFrame2)
        self.inputLayout2.setContentsMargins(0, 5, 0, 5)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setStyleSheet(f'''QLineEdit{{ 
            color: {Style.black}; 
            background-color: {Style.white}; 
            border: 0px solid; 
            border-radius: 23px;  
            padding-left: 10px;
            padding-right: 10px;}}''')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setFont(Style.font("Muller Light", 10))

        self.hideButton2 = QPushButton(self.passwordFrame2)
        self.hideButton2.setMinimumSize(QtCore.QSize(40, 40))
        self.hideButton2.setMaximumSize(QtCore.QSize(40, 40))
        self.hideButton2.setStyleSheet(f'''QPushButton{{ 
        background-color: {Style.white}; 
        border: 0px solid; 
        border-radius: 20px;  
        padding-left: 10px;                    
        padding-right: 10px;}}                    
        QPushButton::hover{{                    
        background-color: {Style.blue20};
        }}''')
        self.hideButton2.setIcon(QIcon(Assets.ICON_EYE_CLOSED))
        self.hideButton2.setIconSize(QSize(24, 24))
        self.hideButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hideButton2.clicked.connect(self.toggle_visibility2)
        self.inputLayout2.addWidget(self.confirm_password_input)
        self.inputLayout2.addWidget(self.hideButton2)

        passwordLayout1 = QVBoxLayout()
        passwordLayout1.setSpacing(8)
        passwordLayout2 = QVBoxLayout()
        passwordLayout2.setSpacing(8)

        self.passwordLabel1 = QtWidgets.QLabel('Придумайте пароль *')
        self.passwordLabel1.setFont(Style.font("Muller Light", 14))
        self.passwordLabel2 = QtWidgets.QLabel('И продублируйте его *')
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
        scroll_content.setStyleSheet(
            f'''QWidget{{background-color: rgba(0, 0, 0, 0); border-radius: 16px; border: 1px solid {Style.blue50};}}''')
        scroll_layout = QGridLayout(scroll_content)

        self.avatar_buttons = []

        for i in range(1, 17):
            avatar_button = QPushButton()
            avatar_button.setCheckable(True)
            avatar_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            avatar_button.setMinimumSize(120, 120)
            avatar_button.setMaximumSize(120, 120)
            pixmap = QPixmap(Assets.AVATARS[i-1])
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

        self.label = QLabel('Выберите аватар:')
        self.label.setFont(Style.font("Muller Light", 16))
        layout.addWidget(self.label)
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
            self.error_label1.setText("* Имя и логин не должны быть пустыми.")
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            self.usernameLabel.setStyleSheet(f"color: {Style.error}")
            self.username_input.setStyleSheet(Style.set_line_edit_style(25, False))
            self.nameLabel.setStyleSheet(f"color: {Style.error}")
            self.name_input.setStyleSheet(Style.set_line_edit_style(25, False))
            return

        elif not name:
            self.nameLabel.setStyleSheet(f"color: {Style.error}")
            self.name_input.setStyleSheet(Style.set_line_edit_style(25, False))
            self.error_label1.setText("* Имя не должно быть пустым.")
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            return

        elif not username:
            self.usernameLabel.setStyleSheet(f"color: {Style.error}")
            self.username_input.setStyleSheet(Style.set_line_edit_style(25, False))
            self.error_label1.setText("* Лгин не должен быть пустым.")
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            return

        else:
            self.name_input.setStyleSheet(Style.set_line_edit_style(25, True))
            self.nameLabel.setStyleSheet(f"color: {Style.blue100}")
            self.username_input.setStyleSheet(Style.set_line_edit_style(25, True))
            self.usernameLabel.setStyleSheet(f"color: {Style.blue100}")
            self.error_label1.setStyleSheet(f'color: {Style.blue100}')

        if not username or not re.match(r'^[a-zA-Z0-9.]+$', username):
            self.username_input.setStyleSheet(Style.set_line_edit_style(25, False))
            self.usernameLabel.setStyleSheet(f'color: {Style.error}')
            self.error_label1.setText(
                "* Имя пользователя должно содержать только буквы латинского алфавита, цифры и точки.")
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            return
        else:
            self.username_input.setStyleSheet(Style.set_line_edit_style(25, True))
            self.usernameLabel.setStyleSheet(f"color: {Style.blue100}")
            self.error_label1.setStyleSheet(f'color: {Style.blue100}')

        if not RegistrationWidget.is_login_unique(username):
            self.username_input.setStyleSheet(Style.set_line_edit_style(25, False))
            self.error_label1.setText("* Логин уже занят.")
            self.usernameLabel.setStyleSheet(f'color: {Style.error}')
            self.error_label1.setStyleSheet(f'color: {Style.error}')
            return
        else:
            self.username_input.setStyleSheet(Style.set_line_edit_style(25, True))
            self.usernameLabel.setStyleSheet(f"color: {Style.blue100}")
            self.error_label1.setStyleSheet(f'color: {Style.blue100}')

        self.error_label1.setText("* Имя пользователя должно содержать только буквы латинского алфавита, цифры и точки.")
        self.next_page()

    def validate_page2(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if len(password) < 6:
            self.passwordFrame1.setStyleSheet(Style.set_line_edit_frame_style(25, False))
            self.passwordLabel1.setStyleSheet(f'color: {Style.error}')
            self.passwordFrame2.setStyleSheet(Style.set_line_edit_frame_style(25, False))
            self.passwordLabel2.setStyleSheet(f'color: {Style.error}')
            self.error_label2.setStyleSheet(f'color: {Style.error}')
            self.error_label2.setText("* Пароль должен содержать не менее 6 символов.")
            return
        else:
            self.passwordFrame1.setStyleSheet(Style.set_line_edit_frame_style(25, False))
            self.passwordLabel1.setStyleSheet(f'color: {Style.blue100}')
            self.passwordFrame2.setStyleSheet(Style.set_line_edit_frame_style(25, False))
            self.passwordLabel2.setStyleSheet(f'color: {Style.blue100}')
            self.error_label2.setStyleSheet(f'color: {Style.blue100}')

        if password != confirm_password:
            self.passwordFrame1.setStyleSheet(Style.set_line_edit_frame_style(25, False))
            self.passwordFrame2.setStyleSheet(Style.set_line_edit_frame_style(25, False))
            self.passwordLabel1.setStyleSheet(f'color: {Style.error}')
            self.passwordLabel2.setStyleSheet(f'color: {Style.error}')
            self.error_label2.setText("* Пароли не совпадают.")
            self.error_label2.setStyleSheet(f'color: {Style.error}')
            return
        else:
            self.passwordFrame1.setStyleSheet(Style.set_line_edit_frame_style(25, True))
            self.passwordFrame2.setStyleSheet(Style.set_line_edit_frame_style(25, True))
            self.passwordLabel1.setStyleSheet(f'color: {Style.blue100}')
            self.passwordLabel2.setStyleSheet(f'color: {Style.blue100}')
            self.error_label2.setStyleSheet(f'color: {Style.blue100}')

        self.error_label2.setText("* Пароль должен содержать не менее 8 символов")
        self.next_page()


    @classmethod
    def is_login_unique(cls, login):
        conn = sqlite3.connect(DB_PATH)
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
        from src.gui.main_window import Window, MainWidget
        from database import SELECT
        if self.selected_avatar is None:
            self.label.setStyleSheet(f'color: {Style.error}')
            return
        else:
            self.label.setStyleSheet(f'color: {Style.blue100}')


        max_id = db.user_max_id()
        self.new_id = max_id + 1
        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        avatarID = self.selected_avatar

        db.insert_user_data(self.new_id, name, username, password, avatarID)

        Window.setUserMainWidget(self.new_id)

    def back_to_login(self):
        from src.gui.main_window import Window, MainWidget
        Window.clear_layout(self.layout)
        login = LoginWidget()
        self.layout.addWidget(login)

    def toggle_visibility1(self):
        if self.is_visible:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.hideButton1.setIcon(QIcon(Assets.ICON_EYE_CLOSED))

        else:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.hideButton1.setIcon(QIcon(Assets.ICON_EYE_OPENED))

        self.is_visible = not self.is_visible

    def toggle_visibility2(self):
        if self.is_visible:
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.hideButton2.setIcon(QIcon(Assets.ICON_EYE_CLOSED))

        else:
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
            self.hideButton2.setIcon(QIcon(Assets.ICON_EYE_OPENED))

        self.is_visible = not self.is_visible

    def on_avatar_selected(self):
        button = self.sender()
        if self.selected_button:
            self.selected_button.setChecked(False)
        self.selected_button = button
        self.selected_avatar = button.property('avatar_id')
        #print(f'Выбран аватар: {self.selected_avatar}')


class ProfileWidget(QWidget):
    layout = None
    msg_box = None
    def __init__(self):
        from src.gui.main_window import Window, MainWidget
        super().__init__()

        self.name = db.get_user_data(MainWidget.userID)[0]
        self.username = '@' + db.get_user_data(MainWidget.userID)[1]
        avatar_path = db.get_avatar_path(MainWidget.userID)


        ProfileWidget.layout = QVBoxLayout()
        ProfileWidget.layout.setContentsMargins(64, 0, 64, 0)

        ProfileWidget.layout = QtWidgets.QVBoxLayout(self)
        ProfileWidget.layout.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet(Style.scrollStyle)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setStyleSheet(f'''QWidget{{ background-color: rgba(0, 0, 0, 0);}}''')
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1377, 1256))

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(64, 0, 64, 64)

        self.profileFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.profileFrame.adjustSize()
        self.profileFrame.setStyleSheet("QFrame{\n"
                                        f"background-color: {Style.white};\n"
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
        sizePolicy.setHeightForWidth(self.avatarBtn.sizePolicy().hasHeightForWidth())
        self.avatarBtn.setSizePolicy(sizePolicy)
        self.avatarBtn.setMinimumSize(QtCore.QSize(110, 110))
        self.avatarBtn.setMaximumSize(QtCore.QSize(110, 110))
        self.avatarBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.avatarBtn.setStyleSheet(f"""QPushButton{{ background-color: {Style.white}; border: 0px solid; border-radius: 55px;}}
                                        QPushButton::hover{{ border: 3px solid {Style.blue100};}}""")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(avatar_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.avatarBtn.setIcon(icon)
        self.avatarBtn.setIconSize(QtCore.QSize(100, 100))
        self.firstLayout.addWidget(self.avatarBtn)

        self.usernameLayout = QtWidgets.QVBoxLayout()
        self.usernameLayout.setContentsMargins(0, 6, 0, 6)
        self.usernameLayout.setSpacing(2)

        self.name1 = QtWidgets.QLabel(self.name)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name1.sizePolicy().hasHeightForWidth())
        self.name1.setSizePolicy(sizePolicy)
        self.name1.setFont(Style.font("Muller Light", 24))
        self.usernameLayout.addWidget(self.name1, 0, QtCore.Qt.AlignTop)

        self.username1 = QtWidgets.QLabel(self.username)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username1.sizePolicy().hasHeightForWidth())
        self.username1.setSizePolicy(sizePolicy)
        self.username1.setFont(Style.font("Muller Light", 14))
        self.username1.setStyleSheet(f"color: {Style.blue100};")
        self.usernameLayout.addWidget(self.username1, 0, QtCore.Qt.AlignTop)
        self.firstLayout.addLayout(self.usernameLayout)
        self.mainLayout.addLayout(self.firstLayout)


        '''----------------Пользовательские списки----------------------'''

        self.listsLayout = QtWidgets.QVBoxLayout()
        self.listsLayout.setSpacing(16)

        self.likeListBtn = QtWidgets.QPushButton('Избранное')
        self.likeListBtn.setMinimumSize(QtCore.QSize(0, 96))
        self.likeListBtn.setMaximumSize(QtCore.QSize(16666, 96))
        self.likeListBtn.setFont(Style.font("Muller", 12))
        self.likeListBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.likeListBtn.setStyleSheet(f'''QPushButton{{
                                       color: {Style.white};
                                       background-color: {Style.blue100};
                                       border-radius: 16px;
                                       padding: 32px; /* Внутренние отступы */
                                       text-align: left; /* Выравнивание текста слева */
                                       }}
                                       QPushButton::icon {{
                                       padding-right: 32px; /* Отступ между иконкой и текстом */
                                       }}
                                       QPushButton::hover {{
                                       background-color: {Style.blue110}; /* Цвет фона при наведении */
                                       }}''')
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(Assets.ICON_HEART_WHITE), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.likeListBtn.setIcon(icon1)
        self.likeListBtn.setIconSize(QtCore.QSize(40, 40))
        self.listsLayout.addWidget(self.likeListBtn)

        self.readLaterListBtn = QtWidgets.QPushButton('Читать позже')
        self.readLaterListBtn.setMinimumSize(QtCore.QSize(0, 96))
        self.readLaterListBtn.setMaximumSize(QtCore.QSize(16666, 96))
        self.readLaterListBtn.setFont(Style.font("Muller", 12))
        self.readLaterListBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.readLaterListBtn.setStyleSheet(f'''QPushButton{{
                                       color: {Style.white};
                                       background-color: {Style.blue100};
                                       border-radius: 16px;
                                       padding: 32px; /* Внутренние отступы */
                                       text-align: left; /* Выравнивание текста слева */
                                       }}
                                       QPushButton::icon {{
                                       padding-right: 23px; /* Отступ между иконкой и текстом */
                                       }}
                                       QPushButton::hover {{
                                       background-color: {Style.blue110}; /* Цвет фона при наведении */
                                       }}''')
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(Assets.ICON_BOOKMARK_WHITE), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.readLaterListBtn.setIcon(icon2)
        self.readLaterListBtn.setIconSize(QtCore.QSize(40, 40))
        self.listsLayout.addWidget(self.readLaterListBtn)
        self.mainLayout.addLayout(self.listsLayout)


        '''--------------------------Личные данные--------------------------------'''

        self.userDataLayout = QtWidgets.QVBoxLayout()
        self.userDataLayout.setSpacing(16)


        self.userDataLadel = QtWidgets.QLabel('Личные данные')
        self.userDataLadel.setFont(Style.font("Muller Light", 16))
        self.userDataLadel.setStyleSheet(f"color: {Style.blue100};")
        self.userDataLayout.addWidget(self.userDataLadel)


        # Section 1: Public Name
        self.public_name_layout = QVBoxLayout()
        self.public_name_layout.setContentsMargins(16, 24, 0, 0)
        self.public_name_layout.setSpacing(12)

        self.new_name_label = QLabel("Введите новое имя:")
        self.new_name_label.setFont(Style.font("Muller Light", 12))
        self.new_name_label.setStyleSheet(f'''color: {Style.blue100}''')

        self.new_name_input = QLineEdit()
        self.new_name_input.setMinimumSize(QSize(400, 48))
        self.new_name_input.setMaximumSize(QSize(400, 48))
        self.new_name_input.setStyleSheet(Style.set_line_edit_style(12, True))
        self.new_name_input.setFont(Style.font("Muller Light", 10))

        change_name_button = QPushButton("Подтвердить")
        change_name_button.setMinimumSize(QSize(400, 40))
        change_name_button.setMaximumSize(QSize(400, 40))
        change_name_button.setFont(Style.font("Muller", 11))
        change_name_button.setStyleSheet(f'''QPushButton{{
                            color: {Style.white};
                            background-color: {Style.blue100};
                            border-radius: 20px;}}
                            QPushButton::hover{{ background-color: {Style.blue110};}}''')
        change_name_button.clicked.connect(self.validate_new_name)

        self.success_label = QLabel("")
        self.success_label.setFont(Style.font("Muller Light", 12))
        self.success_label.setStyleSheet(f"color: {Style.blue110}; border: 0px solid;")


        self.public_name_layout.addWidget(self.new_name_label)
        self.public_name_layout.addWidget(self.new_name_input)
        self.public_name_layout.addWidget(change_name_button)
        self.public_name_layout.addWidget(self.success_label)
        self.public_name_widget = QWidget()
        self.public_name_widget.setLayout(self.public_name_layout)
        self.public_name_section = NameAccordionSection('Имя', self.name, self.public_name_widget)

        self.userDataLayout.addWidget(self.public_name_section)


        # Section 2: Username
        self.username_layout = QVBoxLayout()
        self.username_layout.setContentsMargins(16, 24, 0, 0)
        self.username_layout.setSpacing(12)

        self.new_username_label = QLabel("Введите новый логин:")
        self.new_username_label.setFont(Style.font("Muller Light", 12))
        self.new_username_label.setStyleSheet(f'''color: {Style.blue100}''')

        self.username_input = QLineEdit()
        self.username_input.setMinimumSize(QSize(400, 48))
        self.username_input.setMaximumSize(QSize(400, 48))
        self.username_input.setStyleSheet(Style.set_line_edit_style(12, True))
        self.username_input.setFont(Style.font("Muller Light", 10))

        change_username_button = QPushButton("Подтвердить")
        change_username_button.setMinimumSize(QSize(400, 40))
        change_username_button.setMaximumSize(QSize(400, 40))
        change_username_button.setFont(Style.font("Muller", 11))
        change_username_button.setStyleSheet(f'''QPushButton{{
                            color: {Style.white};
                            background-color: {Style.blue100};
                            border-radius: 20px;}}
                            QPushButton::hover{{ background-color: {Style.blue110};}}''')
        change_username_button.clicked.connect(self.validate_new_username)

        self.massage_label = QLabel("")
        self.massage_label.setFont(Style.font("Muller Light", 10))
        self.massage_label.setStyleSheet(f"color: {Style.blue110}; border: 0px solid;")

        self.username_layout.addWidget(self.new_username_label)
        self.username_layout.addWidget(self.username_input)
        self.username_layout.addWidget(change_username_button)
        self.username_layout.addWidget(self.massage_label)
        self.username_widget = QWidget()
        self.username_widget.setLayout(self.username_layout)
        self.username_section = UsernameAccordionSection('Логин', self.username, self.username_widget)

        self.userDataLayout.addWidget(self.username_section)


        # Section 3: Change Password
        """self.changePasswordBtn = QtWidgets.QPushButton('Сменить пароль')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.changePasswordBtn.sizePolicy().hasHeightForWidth())
        self.changePasswordBtn.setSizePolicy(sizePolicy)
        self.changePasswordBtn.setMinimumSize(QtCore.QSize(250, 48))
        self.changePasswordBtn.setMaximumSize(QtCore.QSize(250, 48))
        self.changePasswordBtn.setFont(Style.font("Muller Regular", 11))
        self.changePasswordBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.changePasswordBtn.setStyleSheet(f'''QPushButton{{
                                                     color: {Style.white};
                                                     background-color: {Style.blue100};
                                                     border-radius: 12px;
                                                     border: 0px solid;
                                                     }}
                                                     QPushButton::hover{{
                                                     background-color: {Style.blue110};}}
                                                     ''')
        self.changePasswordBtn.clicked.connect(self.toggleChangePassword)
        self.userDataLayout.addWidget(self.changePasswordBtn)

        self.change_password_layout = QVBoxLayout()
        self.change_password_label = QLabel('Введите новый пароль')
        self.change_password_edit = QLineEdit()
        self.change_password_button = QPushButton('Подтвердить')
        self.change_password_layout.addWidget(self.change_password_label)
        self.change_password_layout.addWidget(self.change_password_edit)
        self.change_password_layout.addWidget(self.change_password_button)

        self.change_password_widget = QWidget()
        self.change_password_widget.setLayout(self.change_password_layout)
        self.change_password_widget.setVisible(False)"""

        self.mainLayout.addLayout(self.userDataLayout)


        """------------------------------------------------------------------------"""

        spacerItem = QtWidgets.QSpacerItem(160, 160, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.mainLayout.addItem(spacerItem)


        """----------------------------Лейаут с кнопками---------------------------"""

        self.btnsLayout = QtWidgets.QVBoxLayout()
        self.btnsLayout.setSpacing(16)


        self.exitBtn = QtWidgets.QPushButton('Выйти из аккаунта')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.exitBtn.sizePolicy().hasHeightForWidth())
        self.exitBtn.setSizePolicy(sizePolicy)
        self.exitBtn.setMinimumSize(QtCore.QSize(250, 48))
        self.exitBtn.setMaximumSize(QtCore.QSize(16777215, 48))
        self.exitBtn.setFont(Style.font("Muller Regular", 11))
        self.exitBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exitBtn.setStyleSheet(f'''QPushButton{{
                                             color: {Style.blue110};
                                             background-color: {Style.blue40};
                                             border-radius: 24px;
                                             border: 0px solid;
                                             }}
                                             QPushButton::hover{{
                                             background-color: {Style.blue30};}}
                                             ''')
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
        self.deleteAccountBtn.setFont(Style.font("Muller Regular", 11))
        self.deleteAccountBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deleteAccountBtn.setStyleSheet(f'''QPushButton{{
                                             color: {Style.blue110};
                                             background-color: {Style.blue40};
                                             border-radius: 24px;
                                             border: 0px solid;
                                             }}
                                             QPushButton::hover{{
                                             background-color: {Style.blue30};}}
                                             ''')
        self.btnsLayout.addWidget(self.deleteAccountBtn)

        self.mainLayout.addLayout(self.btnsLayout)
        self.verticalLayout_2.addWidget(self.profileFrame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        ProfileWidget.layout.addWidget(self.scrollArea)


        self.likeListBtn.clicked.connect(self.set_likeList)
        self.readLaterListBtn.clicked.connect(self.set_readLaterList)

        self.exitBtn.clicked.connect(ProfileWidget.exit)
        self.deleteAccountBtn.clicked.connect(ProfileWidget.deleteAccount)


        # Диалоговое окно
        ProfileWidget.msg_box = QMessageBox()
        ProfileWidget.msg_box.setIcon(QMessageBox.Question)
        ProfileWidget.msg_box.setStyleSheet(f'''
        QMessageBox {{
            background-color: {Style.white};
            font-family: Muller Light;
            font-size: 14px;
        }}''')
        ProfileWidget.msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ProfileWidget.msg_box.setDefaultButton(QMessageBox.No)

        # Изменение стиля и текста кнопок
        yes_button = ProfileWidget.msg_box.button(QMessageBox.Yes)
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
        yes_button.setText("Да")
        no_button = ProfileWidget.msg_box.button(QMessageBox.No)
        no_button.setStyleSheet(f'''QPushButton {{
            background-color: {Style.blue100};
            color: {Style.white};
            border: none;
            padding-left: 32px;
            padding-right: 32px;
            padding-top: 8px;
            padding-bottom: 8px;
            border-radius: 4px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {Style.blue110};
        }}''')
        no_button.setText("Нет")

    def set_likeList(self):
        from src.gui.main_window import Window, MainWidget
        Window.clear_layout(ProfileWidget.layout)
        select = f"""SELECT articleID FROM interaction WHERE userID = {MainWidget.userID} AND type = 'l';"""
        id_list = db.get_ids(select)

        widget = ArticlesWidget(id_list, 'Избранное', MainWidget.userID)
        ProfileWidget.layout.addWidget(widget)

    def set_readLaterList(self):
        from src.gui.main_window import Window, MainWidget
        Window.clear_layout(ProfileWidget.layout)
        select = f"""SELECT articleID FROM interaction WHERE userID = {MainWidget.userID} AND type = 'r';"""
        id_list = db.get_ids(select)

        widget = ArticlesWidget(id_list, 'Читать позже', MainWidget.userID)
        ProfileWidget.layout.addWidget(widget)

    def toggleChangePassword(self):
        self.change_password_widget.setVisible(not self.change_password_widget.isVisible())

    def validate_new_name(self):
        from src.gui.main_window import Window, MainWidget
        if not self.new_name_input.text():
            self.new_name_label.setStyleSheet(f'''color: {Style.error}''')
            self.new_name_input.setStyleSheet(Style.set_line_edit_style(12, False))
            return
        else:
            self.new_name_label.setStyleSheet(f'''color: {Style.blue100}''')
            self.new_name_input.setStyleSheet(Style.set_line_edit_style(12, True))

        new_name = self.new_name_input.text()

        #Обновление имени в базе
        db.update_name(MainWidget.userID, new_name)

        # Обновление имени в интерфейсе
        self.name1.setText(new_name)
        self.public_name_section.data_label.setText(new_name)

        self.success_label.setText("Имя изменено успешно")


    def validate_new_username(self):
        from src.gui.main_window import Window, MainWidget
        import re

        username = self.username_input.text()
        if not username or not re.match(r'^[a-zA-Z0-9.]+$', username):
            self.username_input.setStyleSheet(Style.set_line_edit_style(12, False))
            self.new_username_label.setStyleSheet(f'color: {Style.error}')
            self.massage_label.setText(
                "* Имя пользователя должно содержать только буквы латинского алфавита, цифры и точки.")
            self.massage_label.setStyleSheet(f'color: {Style.error}; border: 0px solid;')
            return
        elif not RegistrationWidget.is_login_unique(username):
            self.username_input.setStyleSheet(Style.set_line_edit_style(12, False))
            self.massage_label.setText("* Логин уже занят.")
            self.new_username_label.setStyleSheet(f'color: {Style.error}')
            self.massage_label.setStyleSheet(f'color: {Style.error}; border: 0px solid;')
            return
        else:
            self.username_input.setStyleSheet(Style.set_line_edit_style(12, True))
            self.new_username_label.setStyleSheet(f"color: {Style.blue100}")
            self.massage_label.setStyleSheet(f'color: {Style.blue100}; border: 0px solid;')

        new_username = self.username_input.text()

        # Обновление имени в базе
        db.update_username(MainWidget.userID, new_username)
        # Обновление имени в интерфейсе
        self.username1.setText('@' + new_username)
        self.username_section.data_label.setText('@' + new_username)

        self.massage_label.setText("Логин изменён успешно")
    def validate_new_password(self):
        pass

    @classmethod
    def exit(cls):
        from src.gui.main_window import Window, MainWidget
        ProfileWidget.msg_box.setWindowTitle("Подтверждение выхода")
        ProfileWidget.msg_box.setText(f"Вы уверены, что хотите выйти из аккаунта?")

        reply = ProfileWidget.msg_box.exec_()

        if reply == QMessageBox.Yes:
            Window.setMainWidget()
        else:
            return

    @classmethod
    def deleteAccount(cls):
        from src.gui.main_window import Window, MainWidget
        ProfileWidget.msg_box.setWindowTitle("Подтверждение удаления")
        ProfileWidget.msg_box.setText(f"Вы уверены, что хотите удалить аккаунт?")

        reply = ProfileWidget.msg_box.exec_()

        if reply == QMessageBox.Yes:
            db.delete_user_data(MainWidget.userID)
            Window.setMainWidget()
        else:
            return

class NameAccordionSection(QWidget):
    data_label = None
    def __init__(self, title, data, content_widget, parent=None):
        super(NameAccordionSection, self).__init__(parent)
        self.title = title
        self.data = data
        self.content_widget = content_widget
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.header = QWidget()
        self.header.setStyleSheet("QWidget{\n"
                                     f"background-color: {Style.blue10};\n"
                                     "border: 0 px solid;\n"
                                     "border-radius: 16px;}")
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(24, 16, 16, 16)
        self.header_layout.setSpacing(8)
        self.header.setLayout(self.header_layout)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(8)

        self.label = QtWidgets.QLabel(self.title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setFont(Style.font("Muller Light", 11))
        self.label.setStyleSheet(f"color: {Style.blue100};")
        self.verticalLayout.addWidget(self.label)

        NameAccordionSection.data_label = QtWidgets.QLabel(self.data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NameAccordionSection.data_label.sizePolicy().hasHeightForWidth())
        NameAccordionSection.data_label.setSizePolicy(sizePolicy)
        NameAccordionSection.data_label.setFont(Style.font("Muller Light", 16))
        self.verticalLayout.addWidget(NameAccordionSection.data_label)

        self.header_layout.addLayout(self.verticalLayout)

        self.button = QtWidgets.QPushButton()
        self.button.setMinimumSize(QtCore.QSize(48, 48))
        self.button.setMaximumSize(QtCore.QSize(48, 48))
        self.button.setFont(Style.font("Muller Light", 10))
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button.setStyleSheet("QPushButton {\n"
                                         f"    background-color: {Style.blue100};\n"
                                         "    border-radius: 12px; /* Скругление углов */\n"
                                         "}\n"
                                         "QPushButton::hover {\n"
                                         f"    background-color: {Style.blue110};\n"
                                         "}\n")
        self.button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(Assets.ICON_SETTINGS), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(icon3)
        self.button.setIconSize(QtCore.QSize(24, 24))
        self.button.clicked.connect(self.toggleContent)

        self.header_layout.addWidget(self.button)

        self.layout.addWidget(self.header)
        self.content_widget.setVisible(False)
        self.layout.addWidget(self.content_widget)


        self.setLayout(self.layout)

    def toggleContent(self):
        if self.content_widget.isVisible():
            self.button.setIcon(QIcon(Assets.ICON_SETTINGS))
        else:
            self.button.setIcon(QIcon(Assets.ICON_CROSS))
        self.content_widget.setVisible(not self.content_widget.isVisible())
class UsernameAccordionSection(QWidget):
    data_label = None
    def __init__(self, title, data, content_widget, parent=None):
        super(UsernameAccordionSection, self).__init__(parent)
        self.title = title
        self.data = data
        self.content_widget = content_widget
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.header = QWidget()
        self.header.setStyleSheet("QWidget{\n"
                                     f"background-color: {Style.blue10};\n"
                                     "border: 0 px solid;\n"
                                     "border-radius: 16px;}")
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(24, 16, 16, 16)
        self.header_layout.setSpacing(8)
        self.header.setLayout(self.header_layout)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(8)

        self.label = QtWidgets.QLabel(self.title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setFont(Style.font("Muller Light", 11))
        self.label.setStyleSheet(f"color: {Style.blue100};")
        self.verticalLayout.addWidget(self.label)

        UsernameAccordionSection.data_label = QtWidgets.QLabel(self.data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UsernameAccordionSection.data_label.sizePolicy().hasHeightForWidth())
        UsernameAccordionSection.data_label.setSizePolicy(sizePolicy)
        UsernameAccordionSection.data_label.setFont(Style.font("Muller Light", 16))
        self.verticalLayout.addWidget(UsernameAccordionSection.data_label)

        self.header_layout.addLayout(self.verticalLayout)

        self.button = QtWidgets.QPushButton()
        self.button.setMinimumSize(QtCore.QSize(48, 48))
        self.button.setMaximumSize(QtCore.QSize(48, 48))
        self.button.setFont(Style.font("Muller Light", 10))
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button.setStyleSheet("QPushButton {\n"
                                         f"    background-color: {Style.blue100};\n"
                                         "    border-radius: 12px; /* Скругление углов */\n"
                                         "}\n"
                                         "QPushButton::hover {\n"
                                         f"    background-color: {Style.blue110};\n"
                                         "}\n")
        self.button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(Assets.ICON_SETTINGS), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(icon3)
        self.button.setIconSize(QtCore.QSize(24, 24))
        self.button.clicked.connect(self.toggleContent)

        self.header_layout.addWidget(self.button)

        self.layout.addWidget(self.header)
        self.content_widget.setVisible(False)
        self.layout.addWidget(self.content_widget)


        self.setLayout(self.layout)

    def toggleContent(self):
        if self.content_widget.isVisible():
            self.button.setIcon(QIcon(Assets.ICON_SETTINGS))
        else:
            self.button.setIcon(QIcon(Assets.ICON_CROSS))
        self.content_widget.setVisible(not self.content_widget.isVisible())

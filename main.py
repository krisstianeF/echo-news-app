from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from gui import Ui_MainWindow, LoginWidget
from database import INSERT

#INSERT()
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1400, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(1400, 640))
        self.setStyleSheet("background-color: rgb(249, 252, 255);")
        self.setWindowTitle("echo")
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.centralwidget.setLayout(self.horizontalLayout)


        '''-----------------login------------------'''

        self.login = LoginWidget()
        self.horizontalLayout.addWidget(self.login)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    '''MainWindow = Ui_MainWindow()
    MainWindow.show()'''

    main = Window()
    main.show()
    sys.exit(app.exec_())

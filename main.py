from PyQt5 import QtWidgets
from gui import Ui_MainWindow, LoginWindow
from database import INSERT

#INSERT()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = LoginWindow()
    MainWindow.show()
    sys.exit(app.exec_())
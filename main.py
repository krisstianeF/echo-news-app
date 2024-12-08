from PyQt5 import QtWidgets
from gui import Window
from database import INSERT

#INSERT()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()

    MainWindow.show()
    sys.exit(app.exec_())

from PyQt5 import QtWidgets
from gui import Window

#INSERT()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()

    MainWindow.show()
    sys.exit(app.exec_())

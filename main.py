from PyQt5 import QtWidgets
from gui import Window

try:
    print("Запуск парсинга новостей... Это может занять время.")
    from database import INSERT
    #INSERT()
    print("Парсинг завершен успешно.")
except Exception as e:
    print(f"Ошибка при парсинге: {e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()

    MainWindow.show()
    sys.exit(app.exec_())

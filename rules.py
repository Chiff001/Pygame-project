import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidgettt(QMainWindow): # Правила игры
    def __init__(self):
        super().__init__()
        uic.loadUi('rules.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidgettt()
    ex.show()
    sys.exit(app.exec_())
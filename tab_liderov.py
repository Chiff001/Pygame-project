import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidgett(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Таблица лидеров.ui', self)
        self.select_data()
        self.pushButton.clicked.connect(self.push)

    def select_data(self): # показываем список всеех игроков и их результаты
        self.connection = sqlite3.connect("tab_liderov.sqlite")
        res = self.connection.cursor().execute(
            """SELECT nik, lvl, res FROM liders""").fetchall()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Ник игрока', 'Уровень сложности', "Результат"])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def push(self): # Поиск по нику игрока
        if self.lineEdit.text() != '':
            nikk = str(self.lineEdit.text())
            self.connection = sqlite3.connect("tab_liderov.sqlite")
            res = self.connection.execute("SELECT * FROM liders WHERE nik=?", (nikk,)).fetchall()
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setHorizontalHeaderLabels(['Ник игрока', 'Уровень сложности', "Результат"])
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
        else:
            self.select_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidgett()
    ex.show()
    sys.exit(app.exec_())
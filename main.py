import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        result = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.modified = {}
        self.titles = None
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in self.cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()
        self.modified = {}
        self.pushButton.clicked.connect(self.click)
        self.pushButton_2.clicked.connect(self.update_table)

    def click(self):
        self.showdatabase = ShowDatabase()
        self.showdatabase.show()

    def update_table(self):
        result = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.modified = {}
        self.titles = None
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in self.cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()
        self.modified = {}


class ShowDatabase(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        result = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.modified = {}
        self.titles = None
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in self.cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()
        self.modified = {}
        self.pushButton.clicked.connect(self.add_str)
        self.pushButton_2.clicked.connect(self.del_str)
        self.pushButton_3.clicked.connect(self.save_results)

    def add_str(self):
        self.tableWidget.setRowCount(
            self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(str(self.tableWidget.rowCount())))
        self.tableWidget.resizeColumnsToContents()

    def del_str(self):
        self.tableWidget.setRowCount(
            self.tableWidget.rowCount() - 1)
        self.tableWidget.resizeColumnsToContents()

    def save_results(self):
        zagolovok = ['id', 'name', 'roasting', 'density', 'taste', 'price', 'volume']
        if self.tableWidget.rowCount() < len(self.cur.execute(f"""SELECT * FROM coffee""").fetchall()):
            self.cur.execute(f"""DELETE from coffee where id > {self.tableWidget.rowCount()}""").fetchall()
        for i in range(self.tableWidget.rowCount()):
            row = []
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                row.append(item.text())
            row[0] = int(row[0])
            row[5] = int(row[5])
            row[6] = int(row[6])
            if i + 1 > len(self.cur.execute(f"""SELECT * FROM coffee""").fetchall()):
                self.cur.execute(f"""INSERT INTO coffee({zagolovok[0]}, {zagolovok[1]}, {zagolovok[2]}, {zagolovok[3]}, 
                {zagolovok[4]}, {zagolovok[5]}, {zagolovok[6]})
                 VALUES({row[0]}, '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', {row[5]}, {row[6]})""")
                self.con.commit()
            else:
                self.cur.execute(f"""UPDATE coffee
                 SET {zagolovok[0]} = {row[0]}, {zagolovok[1]} = '{row[1]}', {zagolovok[2]} = '{row[2]}',
                 {zagolovok[3]} = '{row[3]}', {zagolovok[4]} = '{row[4]}', {zagolovok[5]} = {row[5]},
                 {zagolovok[6]} = {row[6]}
                 WHERE id = {i + 1}""")
                self.con.commit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLineEdit, QDialogButtonBox, QFormLayout, QTableWidget, QTableWidgetItem, QCalendarWidget, QComboBox
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QInputDialog, QDialog
import sys
import sqlite3


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1128, 904)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 60, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 60, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 60, 101, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(40, 120, 621, 741))
        self.tableWidget.setLineWidth(10)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        #self.tableWidget.setDisabled(True)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(690, 120, 101, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.hide()
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(690, 120, 101, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.hide()
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(690, 120, 101, 41))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.hide()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(690, 180, 101, 41))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(690, 240, 101, 41))
        self.pushButton_8.setObjectName("pushButton_8")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Счета"))
        self.pushButton_2.setText(_translate("MainWindow", "Расходы"))
        self.pushButton_3.setText(_translate("MainWindow", "Доходы"))
        self.pushButton_4.setText(_translate("MainWindow", "Добавить счёт"))
        self.pushButton_5.setText(_translate("MainWindow", "Добавить расход"))
        self.pushButton_6.setText(_translate("MainWindow", "Добавить доход"))
        self.pushButton_7.setText(_translate("MainWindow", "Изменить данные"))
        self.pushButton_8.setText(_translate("MainWindow", "Удалить данные"))


class MyWidget(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        c = open('login.txt', 'r', encoding='utf8')
        data = c.readlines()
        if len(data) == 0:
            self.login()
        n = open('check.txt', encoding='utf8')

        r = n.read().split('\n')[0]
        n.close()
        if r == '':
            self.make_first_check()
        else:
            self.conn = sqlite3.connect(r)

            self.cur = self.conn.cursor()
        self.pushButton.clicked.connect(self.show_cheks)
        self.pushButton_4.clicked.connect(self.make_new_check)
        self.pushButton_2.clicked.connect(self.show_expense)
        self.pushButton_5.clicked.connect(self.make_new_expanse)
        self.pushButton_6.clicked.connect(self.make_new_income)
        self.pushButton_3.clicked.connect(self.show_income)
        self.pushButton_7.clicked.connect(self.change)
        self.pushButton_8.clicked.connect(self.delete)

    def change(self):

        b = int(self.tableWidget.currentRow() + 1)

        if self.pushButton_5.isHidden() != True:

            c = self.cur.execute("SELECT Сумма, Счет FROM Расходы WHERE id = {} ".format(b)).fetchall()
            m = c[0][0]
            d = c[0][1]
            s = ChangeInput()
            s.exec_()
            a = int(s.getInputs())
            n = a - m
            self.cur.execute("UPDATE Счета SET Расход = Расход + ?, Остаток = Остаток - ?  WHERE Название = ?",
                            (n, n, d))

            self.cur.execute("UPDATE Расходы SET Сумма = {} WHERE id = {}".format(a, b))
            self.show_expense()
            self.conn.commit()

        else:

            c = self.cur.execute("SELECT Сумма, Счет FROM Доходы WHERE id = {} ".format(b)).fetchall()
            m = c[0][0]
            d = c[0][1]
            s = ChangeInput()
            s.exec_()
            a = int(s.getInputs())
            n = a - m
            self.cur.execute("UPDATE Счета SET Доход = Доход + ?, Остаток = Остаток + ?  WHERE Название = ?",
                             (n, n, d))

            self.cur.execute("UPDATE Доходы SET Сумма = {} WHERE id = {}".format(a, b))
            self.show_income()
            self.conn.commit()

    def delete(self):
        b = int(self.tableWidget.currentRow() + 1)
        if self.pushButton_5.isHidden() != True:

            c = self.cur.execute("SELECT Сумма, Счет FROM Расходы WHERE id = {} ".format(b)).fetchall()
            m = c[0][0]
            d = c[0][1]
            self.cur.execute("UPDATE Счета SET Расход = Расход - ?, Остаток = Остаток + ?  WHERE Название = ?",
                            (m, m, d))

            self.cur.execute("DELETE FROM Расходы WHERE id = {}".format(b))
            self.show_expense()
            self.conn.commit()

        else:

            c = self.cur.execute("SELECT Сумма, Счет FROM Доходы WHERE id = {} ".format(b)).fetchall()
            m = c[0][0]
            d = c[0][1]

            self.cur.execute("UPDATE Счета SET Доход = Доход - ?, Остаток = Остаток - ?  WHERE Название = ?",
                             (m, m, d))

            self.cur.execute("DELETE FROM Доходы WHERE id = {}".format(b))
            self.show_income()
            self.conn.commit()
    def show_cheks(self):
        self.pushButton_5.hide()
        self.pushButton_4.show()
        self.pushButton_6.hide()
        res = self.cur.execute("SELECT * FROM Счета").fetchall()

        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['Название', 'Расход', 'Доход', 'Остаток'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def show_expense(self):

        self.pushButton_5.show()
        self.pushButton_4.hide()
        self.pushButton_6.hide()

        res = self.cur.execute("SELECT Счет, Категория, Дата, Сумма, Примечание FROM Расходы").fetchall()

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)

        self.tableWidget.setHorizontalHeaderLabels(['Счет', 'Категория', 'Дата', 'Сумма', 'Примечание'])

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))



    def show_income(self):

        self.pushButton_5.hide()
        self.pushButton_4.hide()
        self.pushButton_6.show()

        res = self.cur.execute("SELECT Счет, Категория, Дата, Сумма, Примечание FROM Доходы").fetchall()

        self.tableWidget.clear()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['Счет', 'Категория', 'Дата', 'Сумма', 'Примечание'])

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def make_new_expanse(self):
        dialog = ExpanseInput(self.cur)
        dialog.exec_()

        a, b, c, d, e = dialog.getInputs()
        if (d != ''):
            a = '-'.join(list(map(str, a)))

            self.cur.execute("INSERT INTO Расходы  VALUES(NULL, ?, ?, ?, ?, ?) ", (b, c, a, d, e))
            print(9)
            self.cur.execute("UPDATE Счета SET Расход = Расход + ?, Остаток = Остаток - ?  WHERE Название = ?", (d, d, b))
            self.conn.commit()
            self.show_expense()

    def make_new_income(self):
        dialog = IncomeInput(self.cur)
        dialog.exec_()

        a, b, c, d, e = dialog.getInputs()
        if (d != ''):
            a = '-'.join(list(map(str, a)))

            self.cur.execute("INSERT INTO Доходы (Счет, Категория, Дата, Сумма, Примечание) VALUES(?, ?, ?, ?, ?) ",
                             (b, c, a, d, e))
            self.cur.execute("UPDATE Счета SET Доход = Доход + ?, Остаток = Остаток + ?  WHERE Название = ?", (d, d, b))
            self.conn.commit()

        self.show_income()
    def make_new_check(self):
        dialog = CheckInput()
        dialog.exec_()
        a, b = dialog.getInputs()

        if (a != ''):
            self.cur.execute("INSERT INTO Счета (Название, Расход, Доход, Остаток) VALUES(?, ?, ?, ?) ", (a, 0, 0, b))
            self.conn.commit()
            self.show_cheks()

    def login(self):
        name, ok_pressed = QInputDialog.getText(self, "", "Введите имя пользователя")
        if ok_pressed:
            c = open('login.txt', 'w', encoding='utf-8')
            c.write(name)
            c.close()

    def closeEvent(self, event):
        self.conn.close()

    def make_first_check(self):

        c = open('check.txt', 'w', encoding='utf-8')
        dialog = CheckInput()
        dialog.exec_()
        a, b = dialog.getInputs()
        c.write(a)
        c.write('\n')
        c.write(b)
        c = open('check.txt', 'r', encoding='utf-8')

        self.conn = sqlite3.connect(a)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Счета (Название STRING, Расход INT, Доход INT, Остаток INT)".format(a))
        self.cur.execute("INSERT INTO Счета (Название, Расход, Доход, Остаток) VALUES(?, ?, ?, ?) ", (a, 0, 0, b))
        self.conn.commit()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Расходы (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , Счет STRING, Категория  STRING, Дата DATE, Сумма INT, Примечание STRING)")

        self.conn.commit()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Доходы (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , Счет STRING, Категория  STRING, Дата DATE, Сумма STRING, Примечание STRING)")
        self.conn.commit()


class CheckInput(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Введите название счета", self.first)
        layout.addRow("Введите количество денег на счету", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())

class ChangeInput(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Введите сумму", self.first)

        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return self.first.text()
class ExpanseInput(QDialog):
    def __init__(self, cur, parent=None):
        super().__init__(parent)
        s = cur.execute("SELECT Название FROM Счета").fetchall()
        self.setFixedSize(640, 480)

        self.first = QCalendarWidget(self)
        self.second = QComboBox(self)
        self.category = QComboBox(self)
        self.post = QLineEdit(self)
        self.sum = QLineEdit(self)
        for i in s:
            self.second.addItem(i[0])

        self.category.addItems(['Автомобиль', 'Комиссия', 'Коммунальные услуги', 'Мебель', 'Медицина', 'Одежда', 'Продукты питания', 'Развлечения', 'Хозяйственные товары', 'Техника'])
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Выберите дату", self.first)
        layout.addRow("Выберите счёт", self.second)
        layout.addRow("Выберите категорию", self.category)
        layout.addRow("Сумма", self.sum)
        layout.addRow("Примечание", self.post)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.selectedDate().getDate(), self.second.currentText(), self.category.currentText(), self.sum.text(), self.post.text())

class IncomeInput(QDialog):
    def __init__(self, cur, parent=None):
        super().__init__(parent)
        s = cur.execute("SELECT Название FROM Счета").fetchall()
        self.setFixedSize(640, 480)

        self.first = QCalendarWidget(self)
        self.second = QComboBox(self)
        self.category = QComboBox(self)
        self.post = QLineEdit(self)
        self.sum = QLineEdit(self)
        for i in s:
            self.second.addItem(i[0])

        self.category.addItems(['Зарплата', 'Дивиденды', 'Лотерея', 'Материальная помощь', 'Наследство', 'Находка', 'Пенсия', 'Подарок', 'Продажа имущества', 'Страховка'])
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Выберите дату", self.first)
        layout.addRow("Выберите счёт", self.second)
        layout.addRow("Выберите категорию", self.category)
        layout.addRow("Сумма", self.sum)
        layout.addRow("Примечание", self.post)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.selectedDate().getDate(), self.second.currentText(), self.category.currentText(), self.sum.text(), self.post.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()

    ex.show()
    sys.exit(app.exec_())


from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLineEdit, QDialogButtonBox, QFormLayout, \
    QTableWidget, QListWidget, QListWidgetItem, QTableWidgetItem, QCalendarWidget, QComboBox, QAbstractItemView, \
    QInputDialog
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QDialog

import sys
import sqlite3
import datetime
import matplotlib.pyplot as plt

#Инициализация интерфейса
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
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setEnabled(True)
        self.pushButton_4.setGeometry(QtCore.QRect(690, 120, 101, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(690, 120, 101, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(690, 120, 101, 41))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(690, 180, 101, 41))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(690, 240, 101, 41))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(690, 305, 180, 41))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(40, 10, 130, 41))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(200, 10, 130, 41))
        self.pushButton_11.setObjectName("pushButton_11")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(700, 30, 141, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(660, 30, 100, 21))
        self.label_2.setText("Дата:")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Тексты кнопкам
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
        self.pushButton_9.setText(_translate("MainWindow", "Посмотреть статистику по времени"))
        self.pushButton_10.setText(_translate("MainWindow", "Сменить пользователя"))
        self.pushButton_11.setText(_translate("MainWindow", "Добавить пользователя"))

#Наш основной класс
class MyWidget(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        #Инициализируем интерфейс
        self.setupUi(self)

        self.label.setText(str(datetime.date.today()))
        # Логин, пароль, первый счет
        c = open('login.txt', 'r', encoding='utf8')
        data = c.readlines()
        if len(data) == 0:
            self.answer = self.login()
        else:
            dialog = ChangeUser()
            dialog.exec_()
            self.answer = dialog.getInputs()

        n = open('check.txt', encoding='utf8')

        r = n.read().split('\n')[0]

        n.close()
        if r == '':
            self.make_first_check(self.answer)
        else:
            self.conn = sqlite3.connect(self.answer)

            self.cur = self.conn.cursor()
            self.show_cheks()
        # Назначение кнопок
        self.pushButton.clicked.connect(self.show_cheks)
        self.pushButton_4.clicked.connect(self.make_new_check)
        self.pushButton_2.clicked.connect(self.show_expense)
        self.pushButton_5.clicked.connect(self.make_new_expanse)
        self.pushButton_6.clicked.connect(self.make_new_income)
        self.pushButton_3.clicked.connect(self.show_income)
        self.pushButton_7.clicked.connect(self.change)
        self.pushButton_8.clicked.connect(self.delete)
        self.pushButton_9.clicked.connect(self.time_statistics)
        self.pushButton_10.clicked.connect(self.change_user)
        self.pushButton_11.clicked.connect(self.add_user)

    # Добавить пользователя
    def add_user(self):
        dialog = AddUser()
        dialog.exec_()
        a = dialog.getInputs()
        if len(a) != 0:
            c = open('login.txt', 'a', encoding='utf8')
            c.write(a + "\n")
            c.close()
            c = open('login.txt', 'r', encoding='utf8')
            x = c.readlines()

            self.make_first_check(x[len(x) - 1][0:len(x[len(x) - 1]) - 1])



    #Поменять пользователя
    def change_user(self):
        dialog = ChangeUser()
        dialog.exec_()
        a = dialog.getInputs()
        if len(a) != 0:

            self.conn = sqlite3.connect(a)
            self.cur = self.conn.cursor()
            self.show_cheks()


    #Функция изменения данных в таблице
    def change(self):
        #Поле не выбрано
        if self.tableWidget.currentRow() == -1:
            a = QMessageBox(self)

            a.setText("Выберите поле!")
            a.exec()

        else:

            b = int(self.tableWidget.currentRow() + 1)
            #Если мы находимся на экране с расходами
            if self.pushButton_5.isHidden() != True:

                c = self.cur.execute("SELECT Сумма, Счет, id FROM Расходы WHERE id = {} ".format(b)).fetchall()

                m = c[0][0]

                d = c[0][1]

                s = ChangeInput()

                s.exec_()

                a = int(s.getInputs())

                n = a - m
                # Обновляем базу данных
                self.cur.execute("UPDATE Счета SET Расход = Расход + ?, Остаток = Остаток - ?  WHERE Название = ?",
                                 (n, n, d))

                self.cur.execute("UPDATE Расходы SET Сумма = {} WHERE id = {}".format(a, b))
                self.show_expense()
                self.conn.commit()
            # Если мы находимся на экране с доходами
            else:

                c = self.cur.execute("SELECT Сумма, Счет FROM Доходы WHERE id = {} ".format(b)).fetchall()
                m = c[0][0]
                d = c[0][1]
                s = ChangeInput()
                s.exec_()
                a = int(s.getInputs())
                n = a - m
                # Обновляем базу данных
                self.cur.execute("UPDATE Счета SET Доход = Доход + ?, Остаток = Остаток + ?  WHERE Название = ?",
                                 (n, n, d))

                self.cur.execute("UPDATE Доходы SET Сумма = {} WHERE id = {}".format(a, b))
                self.show_income()
                self.conn.commit()


    # Функция удаления строки в базе
    def delete(self):
        # Если не выбрано поле
        if self.tableWidget.currentRow() == -1:
            a = QMessageBox(self)
            a.setText("Выберите поле!")
            a.exec()
        else:
            b = int(self.tableWidget.currentRow() + 1)
            # Если выбрана таблица расходов
            if self.pushButton_5.isHidden() != True:


                c = self.cur.execute("SELECT Сумма, Счет FROM Расходы WHERE id = {} ".format(b)).fetchall()

                m = c[0][0]
                d = c[0][1]
                # Обновляем базу данных
                self.cur.execute("UPDATE Счета SET Расход = Расход - ?, Остаток = Остаток + ?  WHERE Название = ?",
                                 (m, m, d))

                self.cur.execute("DELETE FROM Расходы WHERE id = {}".format(b))



                self.cur.execute("update Расходы set id = id-1 where id > {}".format(b))
                self.conn.commit()
                self.show_expense()


            # Если выбрана таблица доходов
            else:


                c = self.cur.execute("SELECT Сумма, Счет FROM Доходы WHERE id = {} ".format(b)).fetchall()

                m = c[0][0]
                d = c[0][1]

                self.cur.execute("UPDATE Счета SET Доход = Доход - ?, Остаток = Остаток - ?  WHERE Название = ?",
                                 (m, m, d))

                self.cur.execute("DELETE FROM Доходы WHERE id = {}".format(b))
                self.cur.execute("update Доходы set id = id-1 where id > {}".format(b))
                self.show_income()
                self.conn.commit()


    # Функция отображения счетов
    def show_cheks(self):
        self.pushButton_5.hide()
        self.pushButton_4.show()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        self.pushButton_8.hide()
        res = self.cur.execute("SELECT * FROM Счета").fetchall()

        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['Название', 'Расход', 'Доход', 'Остаток'])
        # Заполнение таблицы
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):

                self.tableWidget.setItem(
                    i, j - 1, QTableWidgetItem(str(elem)))


    #Функция отображения расходов
    def show_expense(self):
        self.pushButton_7.show()
        self.pushButton_8.show()
        self.pushButton_5.show()
        self.pushButton_4.hide()
        self.pushButton_6.hide()

        res = self.cur.execute("SELECT Счет, Категория, Дата, Сумма, Примечание FROM Расходы").fetchall()

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)

        self.tableWidget.setHorizontalHeaderLabels(['Счет', 'Категория', 'Дата', 'Сумма', 'Примечание'])
        # Заполнение таблицы
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


    # Функция отображения доходов
    def show_income(self):
        self.pushButton_7.show()
        self.pushButton_8.show()
        self.pushButton_5.hide()
        self.pushButton_4.hide()
        self.pushButton_6.show()

        res = self.cur.execute("SELECT Счет, Категория, Дата, Сумма, Примечание FROM Доходы").fetchall()

        self.tableWidget.clear()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['Счет', 'Категория', 'Дата', 'Сумма', 'Примечание'])
        # Заполнение таблицы
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


    # Функция добавления расходов
    def make_new_expanse(self):
        dialog = ExpanseInput(self.cur)
        dialog.exec_()

        a, b, c, d, e = dialog.getInputs()
        # Преобразование даты в нормальный вид например 2020-05-07
        if (d != ''):
            a = list(a)

            if a[1] < 10:
                a[1] = '0' + str(a[1])
            if a[2] < 10:
                a[2] = '0' + str(a[2])

            a = '-'.join(list(map(str, a)))
            k = self.cur.execute("SELECT COUNT(*) FROM Расходы").fetchall()

            # Вставляем данные в таблицу
            self.cur.execute("INSERT INTO Расходы (id, Счет, Категория, Дата , Сумма, Примечание) VALUES(?, ?, ?, ?, ?, ?)", (int(k[0][0]) + 1, b, c, a, d, e))

            self.cur.execute("UPDATE Счета SET Расход = Расход + ?, Остаток = Остаток - ?  WHERE Название = ?",
                             (d, d, b))
            self.conn.commit()
            self.show_expense()


    # Функция добавления доходов
    def make_new_income(self):
        dialog = IncomeInput(self.cur)
        dialog.exec_()

        a, b, c, d, e = dialog.getInputs()
        # Преобразование даты в нормальный вид например 2020-05-07
        if (d != ''):
            a = list(a)

            if a[1] < 10:
                a[1] = '0' + str(a[1])
            if a[2] < 10:
                a[2] = '0' + str(a[2])

            a = '-'.join(list(map(str, a)))
            k = self.cur.execute("SELECT COUNT(*) FROM Доходы").fetchall()
            # Вставляем данные в таблицу
            self.cur.execute("INSERT INTO Доходы (id, Счет, Категория, Дата, Сумма, Примечание) VALUES(?, ?, ?, ?, ?, ?) ",
                             (int(k[0][0]) + 1, b, c, a, d, e))
            self.cur.execute("UPDATE Счета SET Доход = Доход + ?, Остаток = Остаток + ?  WHERE Название = ?", (d, d, b))
            self.conn.commit()

        self.show_income()


    # Функция добавления нового счета
    def make_new_check(self):
        dialog = CheckInput()
        dialog.exec_()
        a, b = dialog.getInputs()
        # Вставляем данные в таблицу
        if (a != ''):
            c = self.cur.execute("SELECT COUNT(*) FROM Счета").fetchall()



            self.cur.execute("INSERT INTO Счета (id, Название, Расход, Доход, Остаток) VALUES(?, ?, ?, ?, ?) ", (int(c[0][0]), a, 0, 0, b))
            self.conn.commit()
            self.show_cheks()


    # Первый логин
    def login(self):
        name, ok_pressed = QInputDialog.getText(self, "", "Введите имя пользователя")
        if ok_pressed:
            c = open('login.txt', 'w', encoding='utf-8')
            c.write(name + "\n")
            c.close()
        return name

    def closeEvent(self, event):
        self.conn.close()

    # Первый счет
    def make_first_check(self, k):
        c = open('check.txt', 'a', encoding='utf-8')
        dialog = CheckInput()
        dialog.exec_()
        a, b = dialog.getInputs()
        c.write(a)
        c.write('\n')

        c = open('check.txt', 'r', encoding='utf-8')

        self.conn = sqlite3.connect(k)
        self.cur = self.conn.cursor()
        # Создаем наши таблицы
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Счета (id INT, Название STRING, Расход INT, Доход INT, Остаток INT)".format(a))
        self.cur.execute("INSERT INTO Счета (id, Название, Расход, Доход, Остаток) VALUES(?, ?, ?, ?, ?) ", (0, a, 0, 0, b))
        self.conn.commit()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Расходы (id INT, Счет STRING, Категория STRING, Дата TEXT, Сумма INT, Примечание STRING)")


        self.conn.commit()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Доходы (id INT, Счет STRING, Категория STRING, Дата TEXT, Сумма STRING, Примечание STRING)")
        self.conn.commit()
        self.show_cheks()


    #Функция просчета статистики по времени
    def time_statistics(self):
        if self.pushButton_5.isHidden() is not True:
            dialog = TimeStatisticsExpanseInput(self.cur)
            dialog.exec_()
            a, b, c, tup = dialog.getInputs()

            dialog = showstat(a, b, c, tup, self.cur, True)
            dialog.exec_()

        else:

            dialog = TimeStatisticsIncomeInput(self.cur)
            dialog.exec_()
            a, b, c, tup = dialog.getInputs()

            dialog = showstat(a, b, c, tup, self.cur, False)
            dialog.exec_()
            pass


#Диалог ввода информации о счете
class CheckInput(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Введите название счета", self.first)
        layout.addRow("Введите количество денег на счету", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())


#Диалог ввода изменения значения
class ChangeInput(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self)

        layout = QFormLayout(self)
        layout.addRow("Введите сумму", self.first)

        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)

    def getInputs(self):
        return self.first.text() if len(self.first.text()) != 0 else '0'


#Диалог ввода информации о трате
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

        self.category.addItems(
            ['Автомобиль', 'Комиссия', 'Коммунальные услуги', 'Мебель', 'Медицина', 'Одежда', 'Продукты питания',
             'Развлечения', 'Хозяйственные товары', 'Техника'])
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

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
        return (
            self.first.selectedDate().getDate(), self.second.currentText(), self.category.currentText(),
            self.sum.text(),
            self.post.text())


#Диалог ввода информации о заработке
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

        self.category.addItems(
            ['Зарплата', 'Дивиденды', 'Лотерея', 'Материальная помощь', 'Наследство', 'Находка', 'Пенсия', 'Подарок',
             'Продажа имущества', 'Страховка'])
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

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
        return (
            self.first.selectedDate().getDate(), self.second.currentText(), self.category.currentText(),
            self.sum.text(),
            self.post.text())


#Диалог подсчета статистики по расходам
class TimeStatisticsExpanseInput(QDialog):
    def __init__(self, cur, parent=None):
        super().__init__(parent)

        s = cur.execute("SELECT Название FROM Счета").fetchall()
        self.setFixedSize(640, 480)
        a = ['Автомобиль', 'Комиссия', 'Коммунальные услуги', 'Мебель', 'Медицина', 'Одежда', 'Продукты питания',
             'Развлечения', 'Хозяйственные товары', 'Техника']
        self.first = QCalendarWidget(self)
        self.first_end = QCalendarWidget(self)
        self.second = QComboBox(self)
        self.choice = QListWidget(self)
        self.choice.setSelectionMode(QAbstractItemView.ExtendedSelection)

        for i in s:

            self.second.addItem(i[0])
        for i in a:
            self.choice.addItem(i)



        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Выберите начальную дату", self.first)
        layout.addRow("Выберите конечную дату", self.first_end)
        layout.addRow("Выберите счёт", self.second)
        layout.addRow("Выберите категорию(и)", self.choice)

        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)


    def getInputs(self):
        return (self.first.selectedDate().getDate(), self.first_end.selectedDate().getDate(), self.second.currentText(), self.choice.selectedItems())


#Диалог со сменой пользователя
class AddUser(QDialog):
    def __init__(self):
        super().__init__(parent=None)

        self.setFixedSize(640, 480)
        self.second = QLineEdit(self)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout = QFormLayout(self)
        layout.addRow("Имя пользователя", self.second)
        layout.addWidget(buttonBox)

    def getInputs(self):
        return self.second.text()


#Диалог со сменой пользователя
class ChangeUser(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        c = open('login.txt', 'r', encoding="utf-8")
        x = c.readlines()

        self.setFixedSize(640, 480)
        self.second = QComboBox(self)
        for i in x:
            self.second.addItem(i[0:len(i) - 1])

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)

        layout = QFormLayout(self)
        layout.addRow("Выберите пользователя", self.second)


        layout.addWidget(buttonBox)

    def getInputs(self):
        return self.second.currentText()


#Диалог подсчета статистики по доходам
class TimeStatisticsIncomeInput(QDialog):
    def __init__(self, cur, parent=None):
        super().__init__(parent)

        s = cur.execute("SELECT Название FROM Счета").fetchall()
        self.setFixedSize(640, 480)
        a = ['Зарплата', 'Дивиденды', 'Лотерея', 'Материальная помощь', 'Наследство', 'Находка', 'Пенсия', 'Подарок',
             'Продажа имущества', 'Страховка']
        self.first = QCalendarWidget(self)
        self.first_end = QCalendarWidget(self)
        self.second = QComboBox(self)
        self.choice = QListWidget(self)
        self.choice.setSelectionMode(QAbstractItemView.ExtendedSelection)

        for i in s:
            self.second.addItem(i[0])
        for i in a:
            self.choice.addItem(i)



        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Выберите начальную дату", self.first)
        layout.addRow("Выберите конечную дату", self.first_end)
        layout.addRow("Выберите счёт", self.second)
        layout.addRow("Выберите категорию(и)", self.choice)

        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)


    def getInputs(self):

        return (self.first.selectedDate().getDate(), self.first_end.selectedDate().getDate(), self.second.currentText(), self.choice.selectedItems())


#Вывод статистики
class showstat(QDialog):

    def __init__(self, strt_date, end_date, check, category, cur, exp, parent=None):

        super().__init__(parent)
        lst = []
        for i in category:
            lst.append(i.text())
        strt_date = list(strt_date)
        end_date = list(end_date)

        if strt_date[1] < 10:
            strt_date[1] = '0' + str(strt_date[1])
        if strt_date[2] < 10:
            strt_date[2] = '0' + str(strt_date[2])

        strt_date = '-'.join(list(map(str, strt_date)))

        if end_date[1] < 10:
            end_date[1] = '0' + str(end_date[1])
        if end_date[2] < 10:
            end_date[2] = '0' + str(end_date[2])

        end_date = str('-'.join(list(map(str, end_date))))

        self.setFixedSize(800, 700)
        self.stat = QTableWidget(self)
        k = str(lst)[1:len(str(lst)) - 1]

        if exp:

            sql = f"SELECT Счет, Категория, Дата, Сумма, Примечание from Расходы where Категория in ({k}) and Счет = '{check}' and Дата BETWEEN '{strt_date}' and '{end_date}' "
            res = cur.execute(f"{sql}").fetchall()
        else:

            sql = f"SELECT Счет, Категория, Дата, Сумма, Примечание from Доходы where Категория in ({k}) and Счет = '{check}' and Дата BETWEEN '{strt_date}' and '{end_date}' "
            res = cur.execute(f"{sql}").fetchall()

        categories = []

        stat_categories = []
        j = -1
        for i in res:

            if i[1] not in categories:
                categories.append(i[1])
                stat_categories.append(int(i[3]))

                j += 1
            else:

                stat_categories[j] += int(i[3])



        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

            return my_autopct

        fig1, ax1 = plt.subplots()
        ax1.pie(stat_categories, labels=categories, autopct=make_autopct(stat_categories))
        plt.savefig('pict.png')
        self.pixmap = QtGui.QPixmap('pict.png')
        self.image = QLabel(self)
        self.image.resize(0,0)
        self.image.setPixmap(self.pixmap)
        self.stat.setColumnCount(5)
        self.stat.setRowCount(0)
        self.stat.setHorizontalHeaderLabels(['Счет', 'Категория', 'Дата', 'Сумма', 'Примечание'])

        for i, row in enumerate(res):
            self.stat.setRowCount(
                self.stat.rowCount() + 1)

            for j, elem in enumerate(row):
                self.stat.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        layout = QFormLayout(self)
        layout.addRow("Статистика", self.stat)
        layout.addRow('Круговая диаграмма числовых значений', self.image)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()

    ex.show()
    sys.exit(app.exec_())

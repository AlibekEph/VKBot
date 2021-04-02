import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
from threading import Thread
import time
from PyQt5 import QtCore, QtGui, QtWidgets

from UI.MainWindow import Ui_MainWindow
from UI.AddAccount import Ui_AddAccount
from UI.Publics import Ui_Public
from UI.AddPublic import Ui_AddPublic
from UI.Error_Form import Ui_Error_Form
from UI.AutoActions import Ui_AutoActions

from Assets.database import DB
from Assets.account import Account
from Assets.row import Row
from Assets.others import *
#from Assets.autolike import autolike
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, QTimer
from Assets.task import Task

ACCOUNTS = []
ROWS = []

#def autolike():
#    while stop:
#        print('Work')
#        time.sleep(1)

def autolike():
    start = 0
    while stop:
        if start == 0:
            db = DB()
            sql = "SELECT id, name, link, last_post FROM publics"
            res = db.query(sql).fetchall()
            options = webdriver.ChromeOptions()
            browser = webdriver.Chrome(executable_path=os.path.abspath('chromedriver.exe'), options=options)
            need_to_like = []
            for pub in res:
                browser.get(pub[2])
                last_post = browser.find_elements_by_css_selector('#page_wall_posts .post')[0].get_attribute('id')

                posts = browser.find_element_by_id('page_wall_posts')
                posts = posts.find_elements_by_class_name('post')
                for i in posts:
                    if i.get_attribute('id') == pub[3]:
                        break
                    else:
                        link = i.find_element_by_class_name('post_link').get_attribute('href')[1:]
                        link = pub[2] + '?w=' + link[14:]
                        print(link)
                        need_to_like.append(link)
                sql = f"UPDATE publics SET last_post = '{last_post}' WHERE id = {pub[0]}"
                db.query(sql)
                db.close()
            browser.quit()
            sql = "SELECT id FROM accounts"
            res = db.query(sql).fetchall()
            db.close()
            delay = 0
            for i in need_to_like:
                for j in res:
                    task = Task(Account(j[0]), 'Лайк', i, delay)
                    task.start()
                    delay += 0.5
        time.sleep(1)
        start += 1
        print(start)
        if start == 3600:
            start = 0
    print('stop')

class Main(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        self.setupUi(self)
        open_auto_actions = QAction('Открыть окно автодействий', self)
        open_auto_actions.triggered.connect(self.open_auto_actions)
        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&Действия')
        fileMenu.addAction(open_auto_actions)
        self.table.setRowHeight(0, 5000)
        self.db = DB()
        self.AddAccounts.clicked.connect(self.open_add_account)
        self.Publics.clicked.connect(self.open_publics)
        self.DelBtn.clicked.connect(self.del_account)
        self.update()

    def closeEvent(self, event):
        print("Stop")
        global stop
        stop = False
        autoliking.join()
        event.accept()

    def del_account(self):
        id = self.DelSelect.currentText()
        id = int(id[:id.find('@')])
        print(id)
        sql = f"DELETE FROM accounts WHERE id = {id}"
        self.db.query(sql)
        for i in ROWS:
            i.destroy_row()
        self.update()

    def update(self):
            for i in ROWS:
                i.destroy_row()
            self.table.setRowCount(0)
            sql = "SELECT id, login, password, name FROM accounts"
            res = self.db.query(sql).fetchall()
            self.db.close()
            print(res)
            names = [str(i[0]) + '@' + i[3] for i in res]
            self.DelSelect.clear()
            self.DelSelect.addItems(names)
            for i in res:
                for j in ACCOUNTS:
                    if j.get_id() == i[0]:
                        continue
                ACCOUNTS.append(Account(i[0]))
                ROWS.append(Row(self, ACCOUNTS[-1]))

    def add_row(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        button = QPushButton("Начать")
        self.table.setCellWidget(rowPosition, 0, button)
        like_check = QCheckBox()
        like_check.setStyleSheet("QCheckBox{margin:auto};")
        self.table.setCellWidget(rowPosition, 2, like_check)
        comm_check = QCheckBox()
        comm_check.setStyleSheet("QCheckBox{margin:auto};")
        self.table.setCellWidget(rowPosition, 3, comm_check)
        timer = QTimeEdit()
        self.table.setCellWidget(rowPosition, 6, timer)
        account = QTableWidgetItem("Example")
        account.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table.setItem(rowPosition, 1, account)
        status = QTableWidgetItem("Ожидает")
        status.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table.setItem(rowPosition, 7, status)

    @pyqtSlot()
    def open_add_account(self):
        self.cams = AddAccount(self)
        self.cams.show()

    def open_publics(self):
        self.cams = Publics()
        self.cams.show()

    def open_auto_actions(self):
        self.cams = AutoActions()
        self.cams.show()


class AddAccount(Ui_AddAccount, QDialog):
    def __init__(self, oself):
        super().__init__()
        self.setupUi(self)
        self.AddAccountBtn.clicked.connect(self.add)
        self.db = DB()
        self.oself = oself

    @pyqtSlot()
    def add(self):
        try:
            ls = [self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit.text(),
                  self.lineEdit_4.text(), self.lineEdit_6.text(), self.lineEdit_5.text()]
            for i in ls:
                check_field(i)
            ac = Account(self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit.text(),
                         self.lineEdit_4.text(),self.lineEdit_6.text(),self.lineEdit_5.text())
            ROWS.append(Row(self.oself, ac))
            ex.update()
            self.close()
        except Exception as e:
            print(e)
            self.cams = ErrorForm()
            self.cams.show()
            self.close()


class Publics(Ui_Public, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.AddPublic.clicked.connect(self.open_add_public)
        self.db = DB()
        self.update()
        self.DeletePublic.clicked.connect(self.del_account)

    def update(self):
        sql = "SELECT * FROM publics"
        res = self.db.query(sql).fetchall()
        self.db.close()
        #self.list.clear()
        self.list.setRowCount(0)
        names = [str(i[0]) + '@' + i[1] for i in res]
        self.DeletSelect.clear()
        self.DeletSelect.addItems(names)
        for i in res:
            rowPosition = self.list.rowCount()
            self.list.insertRow(rowPosition)
            for j in range(len(i)):
                    self.list.setItem(rowPosition, j, QTableWidgetItem(str(i[j])))

    def del_account(self):
        id = self.DeletSelect.currentText()
        id = int(id[:id.find('@')])
        print(id)
        sql = f"DELETE FROM publics WHERE id = {id}"
        self.db.query(sql)
        self.update()


    @pyqtSlot()
    def open_add_public(self):
        self.cams = AddPublic()
        self.cams.show()
        self.close()


class AddPublic(Ui_AddPublic, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add)
        self.db = DB()

    @pyqtSlot()
    def add(self):
        options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(executable_path=os.path.abspath('chromedriver.exe'), options=options)
        link = self.lineEdit_2.text()
        browser.get(link)
        name = self.lineEdit.text()
        last_post = browser.find_elements_by_css_selector('#page_wall_posts .post')[0].get_attribute('id')
        print(last_post)
        browser.quit()
        sql = f"INSERT INTO publics (id, name, link, last_post) VALUES (NULL, '{name}', '{link}', '{last_post}')"
        self.db.query(sql)
        self.db.close()
        self.cams = Publics()
        self.cams.show()
        self.close()


class ErrorForm(Ui_Error_Form, QDialog):
    type = 'Sec'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_main_window)

    @pyqtSlot()
    def open_main_window(self):
        self.close()

class AutoActions(Ui_AutoActions, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setLink.clicked.connect(self.SetLinkToRows)
        self.like.clicked.connect(self.SetLikeToRows)
        self.comm.clicked.connect(self.SetCommToRows)
        self.start.clicked.connect(self.StartRows)


    def SetLikeToRows(self):
        for i in ROWS:
            i.set_like_checked()

    def SetCommToRows(self):
        for i in ROWS:
            i.set_comm_checked()

    def SetLinkToRows(self):
        for i in ROWS:
            i.set_link(self.link.text())

    def StartRows(self):
        for i in ROWS:
            i.start_task()



if __name__ == '__main__':
    stop = True
    autoliking = threading.Thread(target=autolike)
    autoliking.start()
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())

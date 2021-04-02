from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Assets.task import Task
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, QTimer

class Row(QWidget):
    def __init__(self, oself, account):
        super().__init__()
        print('Created Row')
        self.start = False
        rowPosition = oself.table.rowCount()
        self.row = rowPosition
        oself.table.insertRow(rowPosition)
        oself.table.setRowHeight(rowPosition, 70)
        self.button = QPushButton("Начать")
        self.button.clicked.connect(self.start_task)
        oself.table.setCellWidget(rowPosition, 0, self.button)
        self.proxy = QTableWidgetItem(str(account.get_proxy()[0]))
        self.proxy.setFlags(QtCore.Qt.ItemIsEnabled)
        oself.table.setItem(rowPosition, 1, self.proxy)
        self.like_check = QCheckBox()
        self.like_check.setStyleSheet("QCheckBox{margin:auto};")
        oself.table.setCellWidget(rowPosition, 3, self.like_check)
        self.comm_check = QCheckBox()
        self.comm_check.setStyleSheet("QCheckBox{margin:auto};")
        oself.table.setCellWidget(rowPosition, 4, self.comm_check)
        self.timer = CustomTimer()
        oself.table.setCellWidget(rowPosition, 7, self.timer)
        self.account_name = QTableWidgetItem(account.get_name())
        self.account_name.setFlags(QtCore.Qt.ItemIsEnabled)
        oself.table.setItem(rowPosition, 2, self.account_name)
        self.status = QTableWidgetItem("Не запущен")
        self.status.setFlags(QtCore.Qt.ItemIsEnabled)
        oself.table.setItem(rowPosition, 8, self.status)
        self.link = QTableWidgetItem("")
        oself.table.setItem(rowPosition, 5, self.link)
        self.comm_text = QTableWidgetItem("")
        oself.table.setItem(rowPosition, 6, self.comm_text)
        self.account = account
        self.oself = oself
#        self.timer = QTimer(self, interval=1000, timeout=self.updateTime)
#        self.timer.start()

    def set_like_checked(self):
        self.like_check.setCheckState(Qt.Checked)

    def set_comm_checked(self):
        self.comm_check.setCheckState(Qt.Checked)

    def set_link(self, link):
        self.link = QTableWidgetItem(link)
        self.oself.table.setItem(self.row, 5, self.link)
#    def updateTime(self):
#        for i in [[self.link, 4], [self.status, 7], [self.comm_text, 5]]:
#            i[0] = QTableWidgetItem(i[0].text())
#            self.oself.table.setItem(self.row, i[1], i[0])

    def start_task(self):
        if self.start:
            self.stop()
            return 0
        print('Start task')
        self.button.setText('В работе')
        self.status.setText('Ожидает')
        self.start = True

        if self.like_check.isChecked() and self.comm_check.isChecked():
            self.task1 = Task(self.account, 'Оба', self.link.text(),
                              self.timer.get_minutes(),
                              self.comm_text.text())
        elif self.comm_check.isChecked() and not self.like_check.isChecked():
            self.task1 = Task(self.account, 'Коментарий', self.link.text(),
                              self.timer.get_minutes(),
                              self.comm_text.text())
        elif self.like_check.isChecked() and not self.comm_check.isChecked():
            self.task1 = Task(self.account, 'Лайк', self.link.text(),
                              self.timer.get_minutes())
        self.block_fields()
        self.task1.setWaitingTrigger(lambda time: self.waiting_status(time))
        self.task1.setMiddlePoint(lambda: self.start_status())
        self.task1.setEndPoint(lambda: self.unlock_field())
        self.task1.start()

    def waiting_status(self, time):
        self.status = QTableWidgetItem('Осталось ' + time)
        self.status.setFlags(QtCore.Qt.ItemIsEnabled)
        self.oself.table.setItem(self.row, 8, self.status)



    def start_status(self):
        self.status.setText('Выполняется')

    def block_fields(self):
        self.like_check.setEnabled(False)
        self.comm_check.setEnabled(False)
        self.status.setFlags(QtCore.Qt.ItemIsEnabled)
        self.link.setFlags(QtCore.Qt.ItemIsEnabled)
        self.comm_text.setFlags(QtCore.Qt.ItemIsEnabled)
        self.timer.block()

    def unlock_field(self):
        self.like_check.setEnabled(True)
        self.comm_check.setEnabled(True)
        self.link = QTableWidgetItem(self.link.text())
        self.oself.table.setItem(self.row, 5, self.link)
        self.comm_text = QTableWidgetItem(self.comm_text.text())
        self.oself.table.setItem(self.row, 6, self.comm_text)
        self.timer.unlock()
        self.button.setText('Начать')
        self.status.setText('Закончена')
        self.start = False

    def stop(self, reason='Остановлена'):
        print('stop task')
        self.task1.stop()
        self.button.setText('Начать')
        self.status.setText(reason)
        self.start = False

    def destroy_row(self):
        try:
            self.task1.stop()
        except:
            pass
        self.start = False




class CustomTimer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.layout2 = QHBoxLayout()
        self.hours = QSpinBox()
        self.minutes = QSpinBox()
        self.layout2.addWidget(self.hours)
        self.layout2.addWidget(self.minutes)
        self.layout3 = QHBoxLayout()
        self.hoursL = QLabel("Часы", self)
        self.minutesL = QLabel("Минуты", self)
        self.layout3.addWidget(self.hoursL)
        self.layout3.addWidget(self.minutesL)
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.layout3)
        self.layout.addLayout(self.layout2)

    def get_minutes(self):
        return self.hours.value() * 60 + self.minutes.value()

    def block(self):
        self.minutes.setEnabled(False)
        self.hours.setEnabled(False)

    def unlock(self):
        self.minutes.setEnabled(True)
        self.hours.setEnabled(True)

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AutoActions.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AutoActions(object):
    def setupUi(self, AutoActions):
        AutoActions.setObjectName("AutoActions")
        AutoActions.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(AutoActions)
        self.gridLayout.setContentsMargins(-1, 45, -1, 45)
        self.gridLayout.setObjectName("gridLayout")
        self.link = QtWidgets.QLineEdit(AutoActions)
        self.link.setObjectName("link")
        self.gridLayout.addWidget(self.link, 0, 0, 1, 1)
        self.setLink = QtWidgets.QPushButton(AutoActions)
        self.setLink.setObjectName("setLink")
        self.gridLayout.addWidget(self.setLink, 1, 0, 1, 1)
        self.start = QtWidgets.QPushButton(AutoActions)
        self.start.setObjectName("start")
        self.gridLayout.addWidget(self.start, 5, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AutoActions)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.like = QtWidgets.QPushButton(AutoActions)
        self.like.setObjectName("like")
        self.horizontalLayout.addWidget(self.like)
        self.comm = QtWidgets.QPushButton(AutoActions)
        self.comm.setObjectName("comm")
        self.horizontalLayout.addWidget(self.comm)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.retranslateUi(AutoActions)
        QtCore.QMetaObject.connectSlotsByName(AutoActions)

    def retranslateUi(self, AutoActions):
        _translate = QtCore.QCoreApplication.translate
        AutoActions.setWindowTitle(_translate("AutoActions", "Form"))
        self.setLink.setText(_translate("AutoActions", "Вставить ссылку"))
        self.start.setText(_translate("AutoActions", "Запустить все"))
        self.label.setText(_translate("AutoActions", "Выбрать у всех"))
        self.like.setText(_translate("AutoActions", "Лайк"))
        self.comm.setText(_translate("AutoActions", "Коментарий"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auth_form.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(321, 188)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.username_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.username_line_edit.setObjectName("username_line_edit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.username_line_edit)
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        self.username_label.setObjectName("username_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.username_label)
        self.password_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.password_line_edit.setObjectName("password_line_edit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.password_line_edit)
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setObjectName("password_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.password_label)
        self.password_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.password_push_button.setObjectName("password_push_button")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.password_push_button)
        self.verticalLayout_3.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 321, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionGet_stats = QtWidgets.QAction(MainWindow)
        self.actionGet_stats.setObjectName("actionGet_stats")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menu.addAction(self.actionGet_stats)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.username_label.setText(_translate("MainWindow", "Username"))
        self.password_label.setText(_translate("MainWindow", "Password"))
        self.password_push_button.setText(_translate("MainWindow", "OK"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menu.setTitle(_translate("MainWindow", "Action"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionGet_stats.setText(_translate("MainWindow", "Get stats"))


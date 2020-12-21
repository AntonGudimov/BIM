# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'db_form.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(565, 369)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.inputComboBox = QtWidgets.QComboBox(Form)
        self.inputComboBox.setObjectName("inputComboBox")
        self.horizontalLayout.addWidget(self.inputComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.infoTableWidget = QtWidgets.QTableWidget(Form)
        self.infoTableWidget.setObjectName("infoTableWidget")
        self.infoTableWidget.setColumnCount(0)
        self.infoTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.infoTableWidget)
        self.getInfoButton = QtWidgets.QPushButton(Form)
        self.getInfoButton.setObjectName("getInfoButton")
        self.verticalLayout.addWidget(self.getInfoButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Database form"))
        self.label.setText(_translate("Form", "Type of information"))
        self.getInfoButton.setText(_translate("Form", "Get info"))


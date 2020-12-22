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
        Form.resize(643, 443)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addRowButton = QtWidgets.QPushButton(Form)
        self.addRowButton.setObjectName("addRowButton")
        self.horizontalLayout_2.addWidget(self.addRowButton)
        self.addButton = QtWidgets.QPushButton(Form)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_2.addWidget(self.addButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.editButton = QtWidgets.QPushButton(Form)
        self.editButton.setObjectName("editButton")
        self.verticalLayout.addWidget(self.editButton)
        self.deleteButton = QtWidgets.QPushButton(Form)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout.addWidget(self.deleteButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Database form"))
        self.label.setText(_translate("Form", "Type of information"))
        self.addRowButton.setText(_translate("Form", "+"))
        self.addButton.setText(_translate("Form", "Add"))
        self.editButton.setText(_translate("Form", "Edit"))
        self.deleteButton.setText(_translate("Form", "Delete"))


from DB_FormUI import Ui_Form as DB_FormUI
from PyQt5 import QtWidgets
from DataBase import DataBase
from PyQt5.QtWidgets import QTableWidgetItem


class DB_Widget(QtWidgets.QWidget, DB_FormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__db = None
        self.inputComboBox.addItems(["User", "Input speed", "Input dynamic", "Key overlaying", "Key hold", "Vector"])
        #self.getInfoButton.clicked.connect(self.get_users_info)
        self.inputComboBox.currentTextChanged.connect(self.get_users_info)

    def display_table(self):
        pass

    def initiate_types_of_info(self):
        pass

    def get_users_info(self):
        combo_box_value = self.inputComboBox.currentText()
        if combo_box_value == "User":
            self.infoTableWidget.clear()
            users = self.__db.select_users()
            self.infoTableWidget.setRowCount(len(users) + 1)
            self.infoTableWidget.setColumnCount(len(users[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("login"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("password"))

            for i in range(1, len(users) + 1):
                for j in range(len(users[i - 1])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(users[i - 1][j])))

        elif combo_box_value == "Input speed":
            self.infoTableWidget.clear()
            speed_info = self.__db.select_speed()
            self.infoTableWidget.setRowCount(len(speed_info) + 1)
            self.infoTableWidget.setColumnCount(len(speed_info[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("speed"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("day_time"))
            self.infoTableWidget.setItem(0, 3, QTableWidgetItem("user_id"))

            for i in range(1, len(speed_info) + 1):
                for j in range(len(speed_info[i - 1])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(speed_info[i - 1][j])))
        elif combo_box_value == "Input dynamic":
            self.infoTableWidget.clear()
            dynamic_info = self.__db.select_input_password_dynamic()
            self.infoTableWidget.setRowCount(len(dynamic_info) + 1)
            self.infoTableWidget.setColumnCount(len(dynamic_info[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("value"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("user_id"))

            for i in range(1, len(dynamic_info) + 1):
                for j in range(len(dynamic_info[i - 1])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(dynamic_info[i - 1][j])))
        elif combo_box_value == "Key overlaying":
            key_overlaying = self.__db.select_key_overlaying()
            self.infoTableWidget.clear()
            if len(key_overlaying):
                self.infoTableWidget.setRowCount(len(key_overlaying) + 1)
                self.infoTableWidget.setColumnCount(len(key_overlaying[0]))
                self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
                self.infoTableWidget.setItem(0, 1, QTableWidgetItem("type"))
                self.infoTableWidget.setItem(0, 2, QTableWidgetItem("user_id"))

                for i in range(1, len(key_overlaying) + 1):
                    for j in range(len(key_overlaying[i - 1])):
                        self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(key_overlaying[i - 1][j])))
            else:
                self.infoTableWidget.setRowCount(1)
                self.infoTableWidget.setColumnCount(3)
                self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
                self.infoTableWidget.setItem(0, 1, QTableWidgetItem("type"))
                self.infoTableWidget.setItem(0, 2, QTableWidgetItem("user_id"))
        elif combo_box_value == "Key hold":
            self.infoTableWidget.clear()
            key_hold = self.__db.select_key_hold()
            self.infoTableWidget.setRowCount(len(key_hold) + 1)
            self.infoTableWidget.setColumnCount(len(key_hold[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("key"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("time hold"))
            self.infoTableWidget.setItem(0, 3, QTableWidgetItem("user_id"))

            for i in range(1, len(key_hold) + 1):
                for j in range(len(key_hold[i - 1])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(key_hold[i - 1][j])))
        elif combo_box_value == "Vector":
            self.infoTableWidget.clear()
            vector = self.__db.select_vector()
            self.infoTableWidget.setRowCount(len(vector) + 1)
            self.infoTableWidget.setColumnCount(len(vector[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("value"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("user_id"))

            for i in range(1, len(vector) + 1):
                for j in range(len(vector[i - 1])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(vector[i - 1][j])))

    def set_transferred_data(self, db: DataBase):
        self.__db = db
        self.display_users()

    def display_users(self):
        self.infoTableWidget.clear()
        users = self.__db.select_users()
        self.infoTableWidget.setRowCount(len(users) + 1)
        self.infoTableWidget.setColumnCount(len(users[0]))
        self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
        self.infoTableWidget.setItem(0, 1, QTableWidgetItem("login"))
        self.infoTableWidget.setItem(0, 2, QTableWidgetItem("password"))

        for i in range(1, len(users) + 1):
            for j in range(len(users[i - 1])):
                self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(users[i - 1][j])))
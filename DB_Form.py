from DB_FormUI import Ui_Form as DB_FormUI
from PyQt5 import QtWidgets
from DataBase import DataBase
from PyQt5.QtWidgets import QTableWidgetItem


class DB_Widget(QtWidgets.QWidget, DB_FormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__db = None
        self.inputComboBox.addItems(["Input speed", "Input dynamic", "Key overlaying", "Key hold", "Vector"])
        self.getInfoButton.clicked.connect(self.get_users_info)

    def display_table(self):
        pass

    def initiate_types_of_info(self):
        pass

    def get_users_info(self):
        combo_box_value = self.inputComboBox.currentText()
        if combo_box_value == "Input speed":
            speed_info = self.__db.select_speed()
            self.infoTableWidget.setRowCount(len(speed_info))
            self.infoTableWidget.setColumnCount(len(speed_info[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("speed"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("day_time"))
            self.infoTableWidget.setItem(0, 3, QTableWidgetItem("user_id"))

            for i in range(1, len(speed_info)):
                for j in range(len(speed_info[i])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(speed_info[i][j])))
        elif combo_box_value == "Input dynamic":
            dynamic_info = self.__db.select_input_password_dynamic()
            self.infoTableWidget.setRowCount(len(dynamic_info))
            self.infoTableWidget.setColumnCount(len(dynamic_info[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("value"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("user_id"))

            for i in range(1, len(dynamic_info)):
                for j in range(len(dynamic_info[i])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(dynamic_info[i][j])))
        elif combo_box_value == "Key overlaying":
            key_overlaying = self.__db.select_key_overlaying()
            self.infoTableWidget.setRowCount(len(key_overlaying))
            self.infoTableWidget.setColumnCount(len(key_overlaying[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("type"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("user_id"))

            for i in range(1, len(key_overlaying)):
                for j in range(len(key_overlaying[i])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(key_overlaying[i][j])))
        elif combo_box_value == "Key hold":
            key_hold = self.__db.select_key_hold()
            self.infoTableWidget.setRowCount(len(key_hold))
            self.infoTableWidget.setColumnCount(len(key_hold[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("type"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("key"))
            self.infoTableWidget.setItem(0, 3, QTableWidgetItem("user_id"))

            for i in range(1, len(key_hold)):
                for j in range(len(key_hold[i])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(key_hold[i][j])))
        elif combo_box_value == "Vector":
            vector = self.__db.select_vector()
            self.infoTableWidget.setRowCount(len(vector))
            self.infoTableWidget.setColumnCount(len(vector[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("value"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("user_id"))

            for i in range(1, len(vector)):
                for j in range(len(vector[i])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(vector[i][j])))



    def set_transefered_data(self, db: DataBase):
        self.__db = db

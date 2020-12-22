from DB_FormUI import Ui_Form as DB_FormUI
from PyQt5 import QtWidgets
from DataBase import DataBase
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


class DB_Widget(QtWidgets.QWidget, DB_FormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__db = None
        self.inputComboBox.addItems(["User", "Password complexity", "Input speed", "Input dynamic", "Key overlaying", "Key hold", "Vector"])
        self.addRowButton.clicked.connect(self.add_row)
        self.addButton.clicked.connect(self.add_value)
        self.editButton.clicked.connect(self.edit_value)
        self.deleteButton.clicked.connect(self.delete_value)
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

        elif combo_box_value == "Password complexity":
            self.infoTableWidget.clear()
            password_complexity_info = self.__db.select_password_complexity()
            self.infoTableWidget.setRowCount(len(password_complexity_info) + 1)
            self.infoTableWidget.setColumnCount(len(password_complexity_info[0]))
            self.infoTableWidget.setItem(0, 0, QTableWidgetItem("id"))
            self.infoTableWidget.setItem(0, 1, QTableWidgetItem("complexity"))
            self.infoTableWidget.setItem(0, 2, QTableWidgetItem("user_id"))

            for i in range(1, len(password_complexity_info) + 1):
                for j in range(len(password_complexity_info[i - 1])):
                    self.infoTableWidget.setItem(i, j, QTableWidgetItem("{0}".format(password_complexity_info[i - 1][j])))

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

    def edit_value(self):
        try:
            curr_table = self.inputComboBox.currentText()
            if curr_table == "User":
                edited_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.edit_user(id=edited_entity[0], new_login=edited_entity[1], new_password=edited_entity[2])

            elif curr_table == "Password complexity":
                edited_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.edit_password_complexity(id=edited_entity[0], new_complexity=edited_entity[1],
                                                    new_user_id=edited_entity[2])
            elif curr_table == "Input speed":
                edited_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(4)]
                self.__db.edit_input_password_speed(id=edited_entity[0], new_speed=edited_entity[1],
                                                    new_day_time=edited_entity[2], new_user_id=edited_entity[3])
            elif curr_table == "Input dynamic":
                edited_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.edit_input_password_dynamic(id=edited_entity[0], new_value=edited_entity[1],
                                                    new_user_id=edited_entity[2])
            elif curr_table == "Key overlaying":
                edited_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.edit_input_key_overlaying(id=edited_entity[0], new_type=edited_entity[1],
                                                    new_user_id=edited_entity[2])
            elif curr_table == "Key hold":
                edited_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(4)]
                self.__db.edit_input_key_hold(id=edited_entity[0], new_key=edited_entity[1],
                                                    new_time=edited_entity[2], new_user_id=edited_entity[3])

            elif curr_table == "Vector":
                edited_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.edit_vector(id=edited_entity[0], new_value=edited_entity[1],
                                              new_user_id=edited_entity[2])
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Database error")
            msg.setWindowTitle("Error msg")
            msg.exec_()
            self.infoTableWidget.setRowCount(self.infoTableWidget.rowCount() - 1)
        finally:
            self.get_users_info()

    def add_value(self):
        try:
            curr_table = self.inputComboBox.currentText()
            if curr_table == "User":
                added_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.add_user(new_login=added_entity[1], new_password=added_entity[2])

            elif curr_table == "Password complexity":
                added_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.add_password_complexity(new_complexity=added_entity[1], new_user_id=added_entity[2])
            elif curr_table == "Input speed":
                added_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(4)]
                self.__db.add_input_password_speed(new_speed=added_entity[1], new_day_time=added_entity[2],
                                                   new_user_id=added_entity[3])
            elif curr_table == "Input dynamic":
                added_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.add_input_password_dynamic(new_value=added_entity[1], new_user_id=added_entity[2])
            elif curr_table == "Key overlaying":
                added_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.add_input_key_overlaying(new_type=added_entity[1], new_user_id=added_entity[2])
            elif curr_table == "Key hold":
                added_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(4)]
                self.__db.add_input_key_hold(new_key=added_entity[1], new_time=added_entity[2],
                                             new_user_id=added_entity[3])

            elif curr_table == "Vector":
                added_entity = [self.infoTableWidget.selectedItems()[i].text() for i in range(3)]
                self.__db.add_vector(new_value=added_entity[1], new_user_id=added_entity[2])
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Database error")
            msg.setWindowTitle("Error msg")
            msg.exec_()
            self.infoTableWidget.setRowCount(self.infoTableWidget.rowCount() - 1)
        finally:
            self.get_users_info()

    def delete_value(self):
        try:
            curr_table = self.inputComboBox.currentText()
            selected_list = self.infoTableWidget.selectedItems()
            if not len(selected_list):
                self.infoTableWidget.setRowCount(self.infoTableWidget.rowCount() - 1)
            else:
                id_to_delete = selected_list[0].text()
                if id_to_delete == "":
                    self.infoTableWidget.setRowCount(self.infoTableWidget.rowCount() - 1)
                if curr_table == "User":
                    self.__db.delete_user(id_to_delete)

                elif curr_table == "Password complexity":
                    self.__db.delete_password_compexity(id_to_delete)

                elif curr_table == "Input speed":
                    self.__db.delete_input_password_speed(id_to_delete)

                elif curr_table == "Input dynamic":
                    self.__db.delete_input_password_dynamic(id_to_delete)

                elif curr_table == "Key overlaying":
                    self.__db.delete_key_overlaying(id_to_delete)

                elif curr_table == "Key hold":
                    self.__db.delete_key_hold(id_to_delete)

                elif curr_table == "Vector":
                    self.__db.delete_vector_element(id_to_delete)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Database error")
            msg.setWindowTitle("Error msg")
            msg.exec_()
            self.infoTableWidget.setRowCount(self.infoTableWidget.rowCount() - 1)
        finally:
            self.get_users_info()

    def add_row(self):
        self.infoTableWidget.setRowCount(self.infoTableWidget.rowCount() + 1)

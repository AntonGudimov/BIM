from AuthFormUI import Ui_MainWindow as AuthFormUI
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QFileDialog, QTableWidgetItem, QMessageBox, QInputDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from KeyboardLogic import KeyboardLogic
from FileLogic import FileLogic
from GraphicForm import MainWindow as GraphicWindow
from DataBase import DataBase
from DB_Form import DB_Widget as DBWindow

import time


def determine_day_time():
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    if "00:00:00" <= curr_time < "06:00:00":
        return "night"
    elif "06:00:00" <= curr_time < "12:00:00":
        return "morning"
    elif "12:00:00" <= curr_time < "18:00:00":
        return "afternoon"
    else:
        return "evening"


class AuthForm(QMainWindow, AuthFormUI):
    def __init__(self):
        super(AuthForm, self).__init__()
        self.setupUi(self)
        self.__keyboard_logic = KeyboardLogic()
        self.__graphic_window = GraphicWindow()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        # Переопределение событий нажатия и отпускания клавиш
        self.password_line_edit.keyPressEvent = self.keyPressEvent
        self.password_line_edit.keyReleaseEvent = self.keyReleaseEvent
        # Подключение сигналов к слотам
        self.password_push_button.clicked.connect(self.clicked_on_password_push_button)
        self.actionMorning.triggered.connect(self.get_entering_speed_password_stats)
        self.actionDay.triggered.connect(self.get_entering_speed_password_stats)
        self.actionEvening.triggered.connect(self.get_entering_speed_password_stats)
        self.actionNight.triggered.connect(self.get_entering_speed_password_stats)
        self.actionEntering_password_dynamic.triggered.connect(self.get_input_password_dynamic)
        #  self.actionInsert.triggered.connect(self.data_base_func)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionExit.triggered.connect(self.close)
        self.registrationRadioButton.toggled.connect(self.prepare_user)
        self.identificationRadioButton.toggled.connect(self.prepare_user)
        # self.verificationRadioButton.toggled.connect(self.set_login_and_password_lines_enabled)
        self.verificationRadioButton.toggled.connect(self.show_dialog)
        self.registrationRadioButton.clicked.connect(self.prepare_user)
        self.db_action_open.triggered.connect(self.open_db)
        self.logoutPushButton.clicked.connect(self.logout)
        self.password_info_label.setVisible(False)
        self.password_info_label_2.setVisible(False)

        self.__vector = list()
        self.__err_msg = ""  # сообщение об ошибке
        self.__pressed_key = ""  # нажатая клавиша
        self.__released_key = ""  # отпущенная клавиша
        self.__pressed_key_time = 0  # время нажатия клавищи
        self.__released_key_time = 0  # время отпускания клавиши
        self.__chair_and_time_pairs = None
        self.__needed_count = 10  # неоходимое кол-во раз ввода пароля для сбора статистики
        self.__is_overlaid = False  # Булевская переменная для детектирования наложения
        self.__db = DataBase('test.db')
        self.__user_id = -1
        self.__input_id = -1
        self.__is_access_granted = False
        self.__mean_pressed_released_diff = dict()
        self.username_line_edit.setDisabled(True)
        self.password_line_edit.setDisabled(True)
        self.__transfered_data = pyqtSignal(DataBase)
        self.__db_form = None

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.text():
            self.__pressed_key_time = time.time()
            QLineEdit.keyPressEvent(self.password_line_edit, a0)
            if self.identificationRadioButton.isChecked() or self.verificationRadioButton.isChecked or (
                    self.__keyboard_logic.user.login and self.__keyboard_logic.user.password \
                    and a0.text() in self.__keyboard_logic.user.password):
                if self.__pressed_key != "":
                    self.__is_overlaid = True
                    # Детектирование наложение клавиши 1 рода
                    self.__keyboard_logic.keyboard_statistic.key_overlay_count += 1
                self.__pressed_key = a0.text()
                self.__keyboard_logic.add_pressed_key(a0.text())
                self.__keyboard_logic.add_pressed_time(self.__pressed_key_time)
                if a0.text() in self.__keyboard_logic.user.password:
                    self.__keyboard_logic.add_pressed_released_key_time_el(a0.text(),
                                                                           self.__pressed_key_time)
                self.__keyboard_logic.add_value_to_func_t()

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.text():
            self.__released_key_time = time.time()
            if self.identificationRadioButton.isChecked() or self.verificationRadioButton.isChecked or (
                    self.__keyboard_logic.user.login and self.__keyboard_logic.user.password and \
                    a0.text() in self.__keyboard_logic.user.password):
                self.__released_key = a0.text()
                if self.__pressed_key != "":
                    if self.__pressed_key != a0.text():
                        # Детектирование наложение клавиши 2 рода
                        self.__keyboard_logic.keyboard_statistic.key_overlay_count_2 += 1
                    else:
                        if self.__is_overlaid:
                            # Детектирование наложение клавиши 3 рода
                            self.__keyboard_logic.keyboard_statistic.key_overlay_count_3 += 1
                    self.__is_overlaid = False
                    self.__pressed_key = ""
                    self.__keyboard_logic.add_released_key(a0.text())
                    self.__keyboard_logic.add_released_time(self.__released_key_time)
                if a0.text() in self.__keyboard_logic.user.password:
                    self.__keyboard_logic.add_pressed_released_key_time_el(a0.text(), self.__released_key_time)

    def clicked_on_password_push_button(self):
        if self.__is_access_granted:
            pass
        elif self.registrationRadioButton.isChecked():
            self.password_info_label.clear()
            self.password_info_label.setVisible(False)
            self.__err_msg = ""
            self.password_info_label.setStyleSheet("background-color: ")
            if self.__keyboard_logic.user.login and self.__keyboard_logic.user.password:
                if self.password_line_edit.text() == self.__keyboard_logic.user.password:
                    day_time = determine_day_time()
                    self.__vector = self.__keyboard_logic.form_vector()
                    print(self.__vector)
                    self.__keyboard_logic.add_speed(day_time)
                    self.__chair_and_time_pairs = self.__keyboard_logic.calculate_input_dynamic()
                    self.__mean_pressed_released_diff = self.__keyboard_logic.calculate_key_hold()
                    # Data base
                    key_overlaying_list = (self.__keyboard_logic.keyboard_statistic.key_overlay_count,
                                           self.__keyboard_logic.keyboard_statistic.key_overlay_count_2,
                                           self.__keyboard_logic.keyboard_statistic.key_overlay_count_3)
                    self.__user_id = self.__db.register_user(self.__keyboard_logic, key_overlaying_list,
                                                             self.__chair_and_time_pairs,
                                                             self.__mean_pressed_released_diff,
                                                             self.__vector)
                    # Data base
                    self.registrationRadioButton.setDisabled(True)
                    self.identificationRadioButton.setDisabled(True)
                    self.verificationRadioButton.setDisabled(True)
                    self.display_form_stats()
                else:
                    if not self.password_line_edit.text():
                        self.__err_msg = "Enter the password"
                    else:
                        self.__err_msg = "Wrong password. Try again"
                    self.password_info_label.setText(self.__err_msg)
                    self.password_info_label.setStyleSheet("background-color: red")
                    self.password_info_label.setVisible(True)
            else:
                if self.username_line_edit.text() and self.password_line_edit.text():
                    self.__keyboard_logic.user.login = self.username_line_edit.text()
                    self.__keyboard_logic.user.password = self.password_line_edit.text()
                    if self.__db.select_user_id(self.__keyboard_logic.user) != -1:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText('User {0} already exists'.format(self.__keyboard_logic.user.login))
                        msg.setWindowTitle("Warning msg")
                        msg.exec_()
                        self.__keyboard_logic.user.login = ""
                        self.__keyboard_logic.user.password = ""
                        self.username_line_edit.clear()
                    else:
                        password_strength = self.__keyboard_logic.examine_password_for_complexity()
                        # Data base
                        user_id = self.__db.insert_user(self.__keyboard_logic.user)
                        self.__db.insert_complexity(password_strength, user_id)
                        # Data base
                        password_strength_msg = QMessageBox()
                        password_strength_msg.setIcon(QMessageBox.Information)
                        password_strength_msg.setText('password is ' + password_strength)
                        password_strength_msg.setWindowTitle("Password strength message")
                        password_strength_msg.exec_()

                        count_str = "You need to input password {0} times".format(self.__needed_count)
                        self.password_info_label_2.setText(count_str)
                        self.password_info_label_2.setVisible(True)
                        self.tableWidget.setColumnCount(2)
                else:
                    self.__err_msg = "Enter input data"
                    self.password_info_label.setText(self.__err_msg)
                    self.password_info_label.setStyleSheet("background-color: red")
                    self.password_info_label.setVisible(True)
            self.password_line_edit.setText("")
            self.__keyboard_logic.pressed_keys_clear()
            self.__keyboard_logic.pressed_times_clear()
            self.__keyboard_logic.keyboard_statistic.key_overlay_count = 0
            self.__keyboard_logic.keyboard_statistic.key_overlay_count_2 = 0
            self.__keyboard_logic.keyboard_statistic.key_overlay_count_3 = 0
        elif self.identificationRadioButton.isChecked():
            self.__keyboard_logic.user.password = self.password_line_edit.text()
            self.__vector = self.__keyboard_logic.form_vector()
            print(self.__vector)
            result = self.__db.identify_user(self.__keyboard_logic.user.password, self.__vector)
            if result[0] != -1 and result[1] != "":
                self.__keyboard_logic.user.login = result[1]
                self.__is_access_granted = True
                self.registrationRadioButton.setDisabled(True)
                self.identificationRadioButton.setDisabled(True)
                self.verificationRadioButton.setDisabled(True)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText('Hello {0}\nID = {1}'.format(result[1], result[0]))
                msg.setWindowTitle("Access granted")
                msg.exec_()
            else:
                self.__is_access_granted = False
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("User is not found")
                msg.setWindowTitle("Access denied")
                msg.exec_()
            self.username_line_edit.clear()
            self.password_line_edit.clear()
            self.__keyboard_logic.pressed_keys_clear()
            self.__keyboard_logic.pressed_times_clear()
            self.__keyboard_logic.released_keys_clear()
            self.__keyboard_logic.released_times_clear()
            self.__keyboard_logic.keyboard_statistic.key_overlay_count = 0
            self.__keyboard_logic.keyboard_statistic.key_overlay_count_2 = 0
            self.__keyboard_logic.keyboard_statistic.key_overlay_count_3 = 0
            self.__keyboard_logic.pressed_released_key_times_dict_clear()

            if result[0] == -1 and result[1] == "":
                if self.request_for_registration():
                    self.logout()
                    self.registrationRadioButton.setChecked(True)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Enter your username and password")
                    msg.setWindowTitle("Info msg")
                    msg.exec_()
        elif self.verificationRadioButton.isChecked():
            self.__keyboard_logic.user.password = self.password_line_edit.text()
            self.__vector = self.__keyboard_logic.form_vector()
            print(self.__vector)
            result = self.__db.verify_user(self.__keyboard_logic.user.password, self.__vector, self.__input_id)
            if result[0]:
                self.__keyboard_logic.user.login = result[1]
                self.__is_access_granted = True
                self.registrationRadioButton.setDisabled(True)
                self.identificationRadioButton.setDisabled(True)
                self.verificationRadioButton.setDisabled(True)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText('Hello {0}'.format(result[1]))
                msg.setWindowTitle("Access granted")
                msg.exec_()
            else:
                self.__is_access_granted = False
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(result[1])
                msg.setWindowTitle("Access denied")
                msg.exec_()
            self.username_line_edit.clear()
            self.password_line_edit.clear()

            self.__keyboard_logic.pressed_keys_clear()
            self.__keyboard_logic.pressed_times_clear()
            self.__keyboard_logic.released_keys_clear()
            self.__keyboard_logic.released_times_clear()
            self.__keyboard_logic.keyboard_statistic.key_overlay_count = 0
            self.__keyboard_logic.keyboard_statistic.key_overlay_count_2 = 0
            self.__keyboard_logic.keyboard_statistic.key_overlay_count_3 = 0
            self.__keyboard_logic.pressed_released_key_times_dict_clear()

            if not result[0]:
                if self.request_for_registration():
                    self.logout()
                    self.registrationRadioButton.setChecked(True)
                    self.username_line_edit.setEnabled(True)
                    self.__keyboard_logic.user.login = ""
                    self.__keyboard_logic.user.password = ""
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Enter your username and password")
                    msg.setWindowTitle("Info msg")
                    msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Operation is not chosen")
            msg.setWindowTitle("Warning msg")
            msg.exec_()

    # Слот для сигнала на получение гистограммы скорости ввода парольной фразы
    def get_entering_speed_password_stats(self):
        if self.__keyboard_logic.user.login == "" and self.__keyboard_logic.user.password == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("There's no user")
            msg.setWindowTitle("Warning msg")
            msg.exec_()
        elif not self.__needed_count - 1:
            mean_speed_dict = self.__keyboard_logic.calculate_mean_speed()
            var_speed_dict = self.__keyboard_logic.calculate_var_speed()

            self.__graphic_window.get_entering_speed_password_stats(
                self.__keyboard_logic.keyboard_statistic.speed_dict,
                mean_speed_dict, var_speed_dict)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Unknown error")
            msg.setWindowTitle("Error msg")
            msg.exec_()

    # Слот для сигнала на получение графика динамики ввода парольной фразы
    def get_input_password_dynamic(self):
        if self.__keyboard_logic.user.login == "" and self.__keyboard_logic.user.password == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("There's no user")
            msg.setWindowTitle("Warning msg")
            msg.exec_()
        elif not self.__needed_count - 1:
            self.__graphic_window.input_password_dynamic(self.__chair_and_time_pairs)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Unknown error")
            msg.setWindowTitle("Error msg")
            msg.exec_()

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Opening keyboard_logic object", "",
                                                "Binary Files (*.bin)", options=options)
        if len(files):
            if files[0]:
                data = FileLogic.open_file(files[0])
                if isinstance(data, KeyboardLogic):
                    self.__keyboard_logic = data
                    self.username_line_edit.setText(self.__keyboard_logic.user.login)
                    self.username_line_edit.setDisabled(True)
                    self.__needed_count = 1
                    self.__chair_and_time_pairs = self.__keyboard_logic.calculate_input_dynamic()
                    self.tableWidget.setColumnCount(2)
                    self.display_form_stats()

    def save_file(self):
        if self.__keyboard_logic.user.login == "" and self.__keyboard_logic.user.password == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("There's no user")
            msg.setWindowTitle("Warning msg")
            msg.exec_()
        elif not self.__needed_count - 1:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName = QFileDialog.getSaveFileName(self, "Saving keyboard_logic object", ".bin",
                                                   "Binary Files (*.bin)", options=options)
            if fileName[0] and fileName[1]:
                FileLogic.save_file(fileName[0], self.__keyboard_logic)

    def display_form_stats(self):
        key_overlay_count = self.__keyboard_logic.keyboard_statistic.key_overlay_count
        key_overlay_count_2 = self.__keyboard_logic.keyboard_statistic.key_overlay_count_2
        key_overlay_count_3 = self.__keyboard_logic.keyboard_statistic.key_overlay_count_3

        mean_pressed_released_diff = self.__mean_pressed_released_diff
        self.__keyboard_logic.pressed_released_key_times_dict_clear()
        if not self.__needed_count - 1:
            self.password_info_label_2.setVisible(False)
            self.output_groupBox.setEnabled(True)

            self.lcdNumber.display(key_overlay_count)
            self.lcdNumber_2.display(key_overlay_count_2)
            self.lcdNumber_3.display(key_overlay_count_3)
            index = 0
            self.tableWidget.setRowCount(len(mean_pressed_released_diff.keys()))
            for k, v in mean_pressed_released_diff.items():
                self.tableWidget.setItem(index, 0, QTableWidgetItem(k))
                self.tableWidget.setItem(index, 1, QTableWidgetItem("{0}".format(round(v, 3))))
                index += 1

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Your ID is {0}".format(self.__user_id))
            msg.setWindowTitle("Info msg")
            msg.exec_()
            self.__is_access_granted = True
        else:
            self.__needed_count -= 1
            count_str = "You need to input password {0} times".format(self.__needed_count)
            self.password_info_label_2.setText(count_str)

    def show_dialog(self):
        self.__input_id = -1
        if self.verificationRadioButton.isChecked():
            while True:
                try:
                    text, ok = QInputDialog.getText(self, 'Input Dialog',
                                                    'Enter your ID:')

                    if ok:
                        self.__input_id = int(text)
                        self.username_line_edit.setDisabled(True)
                        self.password_line_edit.setEnabled(True)
                        break
                    else:
                        self.password_line_edit.setDisabled(True)
                        self.registrationRadioButton.setChecked(False)
                        break
                except ValueError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Invalid input\nInteger only")
                    msg.setWindowTitle("Error msg")
                    msg.exec_()

    def request_for_registration(self):
        if self.identificationRadioButton.isChecked() or self.verificationRadioButton.isChecked():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Would you like to register?")
            msg.setWindowTitle("Request for signing up")
            yes_button = msg.addButton("Yes", QMessageBox.AcceptRole)
            no_button = msg.addButton("No", QMessageBox.RejectRole)
            msg.exec_()
            if msg.clickedButton() == yes_button:
                return True
            elif msg.clickedButton() == no_button:
                return False

    def open_db(self):
        if self.__keyboard_logic.user.login != "" and self.__keyboard_logic.user.password != "":
            if self.__db_form is None:
                self.__db_form = DBWindow()
            self.__db_form.set_transferred_data(self.__db)
            self.__db_form.show()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Authenticate or verify first")
            msg.setWindowTitle("Access denied")
            msg.exec_()

    def prepare_user(self):
        if self.registrationRadioButton.isChecked():
            self.username_line_edit.setEnabled(True)
            self.password_line_edit.setEnabled(True)
            self.__keyboard_logic.user.login = ""
            self.__keyboard_logic.user.password = ""
            self.__needed_count = 10
        else:
            self.username_line_edit.setDisabled(True)
            self.password_line_edit.setEnabled(True)

    def logout(self):
        self.__is_access_granted = False
        self.registrationRadioButton.setEnabled(True)
        self.identificationRadioButton.setEnabled(True)
        self.verificationRadioButton.setEnabled(True)

        self.__keyboard_logic.user.login = ""
        self.__keyboard_logic.user.password = ""

        self.username_line_edit.clear()
        self.clear_form_data()

        self.registrationRadioButton.setChecked(True)

    def clear_form_data(self):
        self.lcdNumber.display(0)
        self.lcdNumber_2.display(0)
        self.lcdNumber_3.display(0)

        self.lcdNumber.setDisabled(True)
        self.lcdNumber_2.setDisabled(True)
        self.lcdNumber_3.setDisabled(True)

        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setDisabled(True)
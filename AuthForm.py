from AuthFormUI import Ui_MainWindow as AuthFormUI
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5 import QtGui
from KeyboardLogic import KeyboardLogic
import time
import matplotlib.pyplot as plt


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
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.password_line_edit.keyPressEvent = self.keyPressEvent
        self.password_line_edit.keyReleaseEvent = self.keyReleaseEvent
        self.password_push_button.clicked.connect(self.clicked_on_password_push_button)
        self.actionGet_stats.triggered.connect(self.get_stats)
        self.password_strength_label.setVisible(False)
        self.__err_msg = ""
        self.__pressed_key = ""
        self.__pressed_key_time = 0
        self.__released_key_time = 0
        self.__keyboard = "Standard keyboard"
        self.__chair_and_time_pairs = None

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.__pressed_key_time = time.time()
        QLineEdit.keyPressEvent(self.password_line_edit, a0)
        if self.__keyboard_logic.user.login and self.__keyboard_logic.user.password:
            self.__keyboard_logic.add_pressed_key(self.__keyboard, a0.text())
            self.__keyboard_logic.add_pressed_time(self.__keyboard, self.__pressed_key_time)
            self.__pressed_key = a0.text()
            if a0.text() in self.__keyboard_logic.user.password:
                self.__keyboard_logic.add_pressed_released_key_time_el(self.__keyboard, a0.text(),
                                                                       self.__pressed_key_time)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.__released_key_time = time.time()
        if self.__keyboard_logic.user.login and self.__keyboard_logic.user.password:
            if self.__pressed_key != a0.text():
                self.__keyboard_logic.keyboard_statistic[self.__keyboard].key_overlay_count += 1
            else:
                self.__pressed_key = ""
            if a0.text() in self.__keyboard_logic.user.password:
                self.__keyboard_logic.add_pressed_released_key_time_el(self.__keyboard, a0.text(),
                                                                       self.__released_key_time)

    def clicked_on_password_push_button(self):
        self.password_strength_label.clear()
        self.password_strength_label.setVisible(False)
        self.__err_msg = ""
        self.password_strength_label.setStyleSheet("background-color: ")
        if self.__keyboard_logic.user.login and self.__keyboard_logic.user.password:
            if self.password_line_edit.text() == self.__keyboard_logic.user.password:
                day_time = determine_day_time()
                self.__keyboard_logic.add_speed(self.__keyboard, day_time)
                self.__chair_and_time_pairs = self.__keyboard_logic.calculate_input_dynamic(self.__keyboard)

                key_overlay_count = self.__keyboard_logic.keyboard_statistic[self.__keyboard].key_overlay_count
                mean_pressed_released_diff = self.__keyboard_logic.calculate_mean_time_diff(self.__keyboard)

                print("Number of key overlay: {0}".format(key_overlay_count))
                print("Mean value of mean pressed-released time difference:\n{0}".format(mean_pressed_released_diff))
            else:
                if not self.password_line_edit.text():
                    self.__err_msg = "Enter the password"
                else:
                    self.__err_msg = "Wrong password. Try again"
                self.password_strength_label.setText(self.__err_msg)
                self.password_strength_label.setStyleSheet("background-color: red")
                self.password_strength_label.setVisible(True)
        else:
            if self.username_line_edit.text() and self.password_line_edit.text():
                self.__keyboard_logic.user.login = self.username_line_edit.text()
                self.__keyboard_logic.user.password = self.password_line_edit.text()
                self.__keyboard_logic.add_keyboard(self.__keyboard)
                password_strength = self.__keyboard_logic.examine_password_for_complexity()
                self.password_strength_label.setText(password_strength)
                self.password_strength_label.setVisible(True)
                self.username_line_edit.setDisabled(True)
            else:
                self.__err_msg = "Enter input data"
                self.password_strength_label.setText(self.__err_msg)
                self.password_strength_label.setStyleSheet("background-color: red")
                self.password_strength_label.setVisible(True)
        self.password_line_edit.setText("")
        self.__keyboard_logic.pressed_keys_clear(self.__keyboard)
        self.__keyboard_logic.pressed_times_clear(self.__keyboard)
        self.__keyboard_logic.keyboard_statistic[self.__keyboard].key_overlay_count = 0

    def get_stats(self):
        mean_speed_dict = self.__keyboard_logic.calculate_mean_speed(self.__keyboard)
        var_speed_dict = self.__keyboard_logic.calculate_var_speed(self.__keyboard)

        for k, v in self.__keyboard_logic.keyboard_statistic[self.__keyboard].speed_dict.items():
            plt.bar(range(1, len(v) + 1), v)
            title = "Speed of the entering the password. Daytime = {0}\nmean speed = {1}\nvar speed = {2}".format(
                k, mean_speed_dict[k], var_speed_dict[k])
            plt.title(title)
            plt.ylabel("speed of the entering the password")
            plt.xlabel("number of entering the password")
            plt.show()
        plt.plot(self.__chair_and_time_pairs[0], self.__chair_and_time_pairs[1])
        plt.title("Dynamic of the entering the password")
        plt.xlabel("char pairs")
        plt.ylabel("time difference")
        plt.grid(True)
        plt.show()



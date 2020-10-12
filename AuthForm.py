from AuthFormUI import Ui_MainWindow as AuthFormUI
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5 import QtGui
from PasswordLogic import PasswordLogic
import time
import matplotlib.pyplot as plt
import numpy as np


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
        self.__password_logic = PasswordLogic()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.password_line_edit.keyPressEvent = self.keyPressEvent
        self.password_push_button.clicked.connect(self.clicked_on_password_push_button)
        self.actionGet_stats.triggered.connect(self.get_stats)
        self.password_strength_label.setVisible(False)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        QLineEdit.keyPressEvent(self.password_line_edit, a0)
        if self.__password_logic.user_name and self.__password_logic.password:
            curr_time = time.time()
            self.__password_logic.add_pressed_key(a0.text())
            self.__password_logic.add_pressed_time(curr_time)

    def clicked_on_password_push_button(self):
        self.password_strength_label.clear()
        self.password_strength_label.setVisible(False)
        if self.__password_logic.user_name and self. __password_logic.password:
            if self.password_line_edit.text() == self.__password_logic.password:
                day_time = determine_day_time()
                self.__password_logic.add_speed(day_time, self.__password_logic.calculate_speed())
                self.__password_logic.calculate_input_dynamic()
                self.__password_logic.add_mean_speed(day_time, np.mean(self.__password_logic.speed_dict[day_time]))
                self.__password_logic.add_var_speed(day_time, np.var(self.__password_logic.speed_dict[day_time]))
            else:
                self.password_strength_label.setText("Wrong password. Try again")
                self.password_strength_label.setStyleSheet("background-color: red")
                self.password_strength_label.setVisible(True)
        else:
            if self.username_line_edit.text() and self.password_line_edit.text():
                self.__password_logic.user_name = self.username_line_edit.text()
                self.__password_logic.password = self.password_line_edit.text()
                password_strength = self.__password_logic.examine_password_for_complexity()
                self.password_strength_label.setText(password_strength)
                self.password_strength_label.setVisible(True)
                self.username_line_edit.setDisabled(True)
        self.password_line_edit.setText("")
        self.__password_logic.clear_pressed_keys()
        self.__password_logic.clear_pressed_times()

    def get_stats(self):
        for k, v in self.__password_logic.speed_dict.items():
            plt.bar(range(1, len(v) + 1), v)
            title = "Speed of the entering the password. Daytime = {0}\nmean speed = {1}\nvar speed = {2}".format(
                k, self.__password_logic.mean_speed_dict[k], self.__password_logic.var_speed_dict[k])
            plt.title(title)
            plt.ylabel("speed of the entering the password")
            plt.xlabel("number of entering the password")
            plt.show()
        arr = self.__password_logic.get_char_pairs_from_password()
        plt.plot(arr, self.__password_logic.time_pairs)
        plt.grid(True)
        plt.show()

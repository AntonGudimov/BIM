from AuthFormUI import Ui_MainWindow as AuthFormUI
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5 import QtGui
from Logic import Logic
import time
import matplotlib.pyplot as plt
import numpy as np


class AuthForm(QMainWindow, AuthFormUI):
    def __init__(self):
        super(AuthForm, self).__init__()
        self.setupUi(self)
        self.__password_logic = Logic()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.password_line_edit.keyPressEvent = self.keyPressEvent
        self.password_push_button.clicked.connect(self.clicked_on_password_push_button)
        self.actionGet_stats.triggered.connect(self.get_stats)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        QLineEdit.keyPressEvent(self.password_line_edit, a0)
        if self.__password_logic.user_name and self.__password_logic.password:
            if not self.__password_logic.start_time:
                self.__password_logic.start_time = time.time()
            else:
                self.__password_logic.end_time = time.time()

    def clicked_on_password_push_button(self):
        if self.__password_logic.user_name and self. __password_logic.password:
            if self.username_line_edit.text() and self.password_line_edit.text() and \
                    self.password_line_edit.text() == self.__password_logic.password:
                self.__password_logic.add_speed(self.__password_logic.calculate_speed())
                self.__password_logic.mean_speed = np.mean(self.__password_logic.speed_list)
                self.__password_logic.var_speed = np.var(self.__password_logic.speed_list)
        else:
            if self.username_line_edit.text() and self.password_line_edit.text():
                self.__password_logic.user_name = self.username_line_edit.text()
                self.__password_logic.password = self.password_line_edit.text()
        self.password_line_edit.setText("")

    def get_stats(self):
        plt.bar(range(len(self.__password_logic.speed_list)), self.__password_logic.speed_list)
        plt.ylabel("speed of the entering the password")
        plt.xlabel("number of entering the password")
        plt.show()
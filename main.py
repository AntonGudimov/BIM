from PyQt5.QtWidgets import QApplication
from AuthForm import AuthForm
import sys


def main():
    app = QApplication(sys.argv)
    form = AuthForm()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

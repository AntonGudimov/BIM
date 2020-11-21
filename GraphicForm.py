from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

    def get_entering_speed_password_stats(self, speed_dict, mean_speed_dict, var_speed_dict):
        sender = self.sender().text()
        day_time = ""
        if sender == "Morning":
            day_time = "morning"
        elif sender == "Day":
            day_time = "afternoon"
        elif sender == "Evening":
            day_time = "evening"
        elif sender == "Night":
            day_time = "night"
        else:
            pass

        if len(speed_dict[day_time]):
            title = "Speed of the entering the password. Daytime = {0}\nmean speed = {1}\nvar speed = {2}".format(
                sender, mean_speed_dict[day_time], var_speed_dict[day_time])
            x_label = "number of entering the password"
            y_label = "speed of the entering the password"

            # Create the maptlotlib FigureCanvas object,
            # which defines a single set of axes as self.axes.
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.bar(range(1, len(speed_dict[day_time]) + 1), speed_dict[day_time])

            sc.axes.set_ylim([0, max(speed_dict[day_time]) + 1])
            sc.axes.set_xlim([0.5, len(speed_dict[day_time]) + 0.5])
            sc.axes.set_title(title)
            sc.axes.set_xlabel(x_label)
            sc.axes.set_ylabel(y_label)

            self.setCentralWidget(sc)
            self.setWindowTitle("Entering speed password stats")
            self.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Collection is empty")
            msg.setWindowTitle("Warning msg")
            msg.exec_()

    def input_password_dynamic(self, chair_and_time_pairs):
        if len(chair_and_time_pairs[1]):
            title = "Dynamic of the entering the password"
            x_label = "char pairs"
            y_label = "time difference [seconds]"

            # Create the maptlotlib FigureCanvas object,
            # which defines a single set of axes as self.axes.
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.plot(chair_and_time_pairs[0], chair_and_time_pairs[1])

            sc.axes.set_title(title)
            sc.axes.set_xlabel(x_label)
            sc.axes.set_ylabel(y_label)

            self.setCentralWidget(sc)
            self.setWindowTitle("Input password dynamic")
            self.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Collection is empty")
            msg.setWindowTitle("Warning msg")
            msg.exec_()



from PyQt5.QtWidgets import *
from gui.widgets.home import Home


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.widgets_dict = {
            "home": 0
        }

        self.stack_widget = QStackedWidget()

        self.stack_widget.addWidget(Home())
        self.setCentralWidget(self.stack_widget)

        self.set_active_widget("home")
        self.setFixedSize(300, 300)
        self.setWindowTitle("Quoridor")

    def set_active_widget(self, widget_name):
        self.stack_widget.setCurrentIndex(self.widgets_dict[widget_name])

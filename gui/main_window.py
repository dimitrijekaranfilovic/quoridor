from PyQt5.QtWidgets import *
from gui.widgets.home import Home
from gui.widgets.board import Board


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.widgets_dict = {
            "home": 0,
            "board": 1
        }

        self.stack_widget = QStackedWidget()
        self.home = Home()
        self.board = Board()

        self.stack_widget.addWidget(self.home)
        self.stack_widget.addWidget(self.board)
        self.setCentralWidget(self.stack_widget)

        self.set_active_widget("home")
        # self.setFixedSize(300, 300)

        self.setWindowTitle("Quoridor")
        self.set_up_events()

    def set_up_events(self):
        self.home.play_btn.clicked.connect(self.get_game_config)

    def get_game_config(self):
        config = self.home.get_configuration()
        player_vs_computer = len(config) == 1
        self.set_active_widget("board")

    def set_active_widget(self, widget_name):
        width = 500
        height = 500
        if widget_name == "home":
            width = 300
            height = 200
        elif widget_name == "board":
            width = 700
            height = 700

        self.setFixedSize(width, height)
        self.stack_widget.setCurrentIndex(self.widgets_dict[widget_name])

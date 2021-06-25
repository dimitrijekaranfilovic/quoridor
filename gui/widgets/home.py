from PyQt5.QtWidgets import *


class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        # 
        # 
        #
        #
        self.select = QComboBox()
        self.play_btn = QPushButton("Play")
        self.choose_players_algorithms = QVBoxLayout()
        self.choose_computer_algorithm = QVBoxLayout()

        self.choose_players_algorithms_widgets = []
        self.choose_computer_algorithm_widgets = []
        self.widgets = []
        self.v_main = QVBoxLayout()

        self.player_one_alg = QComboBox()
        self.player_two_alg = QComboBox()

        self.computer_alg = QComboBox()

        self.algorithm_selection_options = []

        self.algorithms = ["minimax", "minimax with alpha beta", "expectimax", "monte carlo tree search"]
        self.combo_box1 = QComboBox()
        self.combo_box2 = QComboBox()
        self.combo_box3 = QComboBox()

        self.set_up()

    def set_up(self):
        label = QLabel("Quoridor")
        label.setStyleSheet("font-size: 18px;font-family:sans-serif;")
        # select = QComboBox()

        h1 = QHBoxLayout()

        h1.addStretch()
        h1.addWidget(label)
        h1.addStretch()

        self.select.setToolTip("Choose play mode")
        self.select.addItem("Player vs computer")
        self.select.addItem("Simulation")

        h2 = QHBoxLayout()
        h2.addStretch()
        h2.addWidget(self.select)
        h2.addStretch()

        h3 = QHBoxLayout()
        h3.addStretch()
        h3.addWidget(self.play_btn)
        h3.addStretch()

        ### Part to choose algorithms for simulation ###
        h4 = QHBoxLayout()
        label2 = QLabel("Choose player algorithms")
        self.choose_players_algorithms_widgets.append(label2)
        h4.addStretch()
        h4.addWidget(label2)
        h4.addStretch()
        h5 = QHBoxLayout()
        h5.addStretch()
        label3 = QLabel("Player 1")
        self.choose_players_algorithms_widgets.append(label3)
        h5.addWidget(label3)
        h5.addStretch()
        label4 = QLabel("Player 2")
        self.choose_players_algorithms_widgets.append(label4)
        h5.addWidget(label4)
        h5.addStretch()

        h6 = QHBoxLayout()
        h6.addStretch()

        self.combo_box1.addItems(self.algorithms)
        self.choose_players_algorithms_widgets.append(self.combo_box1)

        self.combo_box2.addItems(self.algorithms)
        self.choose_players_algorithms_widgets.append(self.combo_box2)

        h6.addWidget(self.combo_box1)
        h6.addStretch()
        h6.addWidget(self.combo_box2)
        h6.addStretch()

        self.choose_players_algorithms.addLayout(h4)
        self.choose_players_algorithms.addLayout(h5)
        self.choose_players_algorithms.addLayout(h6)

        ### Part to choose opponent algorithm in player vs computer
        h7 = QHBoxLayout()
        h7.addStretch()
        label5 = QLabel("Choose computer algorithm")
        self.choose_computer_algorithm_widgets.append(label5)
        h7.addWidget(label5)
        h7.addStretch()

        h8 = QHBoxLayout()
        self.choose_computer_algorithm_widgets.append(self.combo_box3)
        self.combo_box3.addItems(self.algorithms)

        h8.addStretch()
        h8.addWidget(self.combo_box3)
        h8.addStretch()

        self.choose_computer_algorithm.addLayout(h7)
        self.choose_computer_algorithm.addLayout(h8)

        s1 = QFrame()
        s1.setFrameShape(QFrame.HLine)
        s1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        s1.setLineWidth(1)

        s2 = QFrame()
        s2.setFrameShape(QFrame.HLine)
        s2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        s2.setLineWidth(1)

        self.v_main.addLayout(h1)
        self.v_main.addLayout(h2)

        self.v_main.addWidget(s1)

        self.choose_computer_algorithm.setObjectName("choose_computer_algorithm")
        self.choose_players_algorithms.setObjectName("choose_players_algorithms")

        self.v_main.addItem(self.choose_computer_algorithm)
        self.v_main.addItem(self.choose_players_algorithms)
        self.v_main.addWidget(s2)
        self.v_main.addLayout(h3)
        self.v_main.addStretch()

        self.setLayout(self.v_main)

        self.algorithm_selection_options.append(self.choose_computer_algorithm)
        self.algorithm_selection_options.append(self.choose_players_algorithms)

        self.widgets.append(self.choose_computer_algorithm_widgets)
        self.widgets.append(self.choose_players_algorithms_widgets)
        self.change_algorithm_selection()
        self.set_up_events()

    def set_up_events(self):
        self.select.currentIndexChanged.connect(self.change_algorithm_selection)

    def change_algorithm_selection(self):
        for i in range(2):
            if i == self.select.currentIndex():
                for widget in self.widgets[i]:
                    widget.setHidden(False)
            else:
                for widget in self.widgets[i]:
                    widget.setHidden(True)

    def get_configuration(self):
        algorithms = []
        if self.select.currentIndex() == 0:
            algorithms.append(self.combo_box3.currentText())
        else:
            algorithms.append(self.combo_box1.currentText())
            algorithms.append(self.combo_box2.currentText())
        return algorithms

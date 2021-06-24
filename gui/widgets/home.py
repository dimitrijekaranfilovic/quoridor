from PyQt5.QtWidgets import *


class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        self.h1 = QHBoxLayout()
        self.h2 = QHBoxLayout()
        self.h3 = QHBoxLayout()
        self.select = QComboBox()

        self.choose_players_algorithms = QVBoxLayout()
        self.choose_computer_algorithm = QVBoxLayout()
        self.v_main = QVBoxLayout()

        self.player_one_alg = QComboBox()
        self.player_two_alg = QComboBox()

        self.computer_alg = QComboBox()

        self.player_one = ""
        self.player_two = ""
        self.computer = ""

        self.algorithm_selection_options = []

        self.algorithms = ["minimax", "minimax with alpha beta", "expectimax", "monte carlo tree search"]

        self.set_up()

    def set_up(self):
        label = QLabel("Quoridor")
        label.setStyleSheet("font-size: 18px;font-family:sans-serif;")

        self.h1.addStretch()
        self.h1.addWidget(label)
        self.h1.addStretch()

        self.h2.addStretch()

        self.select.setToolTip("Choose play mode")
        self.select.addItem("Player vs computer")
        self.select.addItem("Simulation")
        self.select.currentIndexChanged.connect(self.change_algorithm_selection)

        self.h2.addWidget(self.select)
        self.h2.addStretch()

        play_btn = QPushButton("Play")
        self.h3.addStretch()
        self.h3.addWidget(play_btn)
        self.h3.addStretch()

        ### Part to choose algorithms for simulation ###
        h4 = QHBoxLayout()
        label2 = QLabel("Choose player algorithms")
        h4.addStretch()
        h4.addWidget(label2)
        h4.addStretch()
        h5 = QHBoxLayout()
        h5.addStretch()
        h5.addWidget(QLabel("Player 1"))
        h5.addStretch()
        h5.addWidget(QLabel("Player 2"))
        h5.addStretch()

        h6 = QHBoxLayout()
        h6.addStretch()

        combo_box1 = QComboBox()
        combo_box1.addItems(self.algorithms)

        combo_box2 = QComboBox()
        combo_box2.addItems(self.algorithms)

        h6.addWidget(combo_box1)
        h6.addStretch()
        h6.addWidget(combo_box2)
        h6.addStretch()

        self.choose_players_algorithms.addLayout(h4)
        self.choose_players_algorithms.addLayout(h5)
        self.choose_players_algorithms.addLayout(h6)

        h7 = QHBoxLayout()
        h7.addStretch()
        h7.addWidget(QLabel("Choose computer algorithm"))
        h7.addStretch()

        h8 = QHBoxLayout()
        combo_box3 = QComboBox()
        combo_box3.addItems(self.algorithms)

        h8.addStretch()
        h8.addWidget(combo_box3)
        h8.addStretch()

        self.choose_computer_algorithm.addLayout(h7)
        self.choose_computer_algorithm.addLayout(h8)

        # self.choose_players_algorithms.setEnabled(False)

        s1 = QFrame()
        s1.setFrameShape(QFrame.HLine)
        s1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        s1.setLineWidth(1)

        s2 = QFrame()
        s2.setFrameShape(QFrame.HLine)
        s2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        s2.setLineWidth(1)

        self.v_main.addLayout(self.h1)
        self.v_main.addLayout(self.h2)

        self.v_main.addWidget(s1)

        self.choose_computer_algorithm.setObjectName("choose_computer_algorithm")
        self.choose_players_algorithms.setObjectName("choose_players_algorithms")

        self.v_main.addItem(self.choose_computer_algorithm)
        self.v_main.addItem(self.choose_players_algorithms)
        self.v_main.addWidget(s2)
        self.v_main.addLayout(self.h3)
        self.v_main.addStretch()

        self.setLayout(self.v_main)

        self.algorithm_selection_options.append(self.choose_computer_algorithm)
        self.algorithm_selection_options.append(self.choose_players_algorithms)

        self.change_algorithm_selection()

    def change_algorithm_selection(self):
        # print("EVO ME!")

        if self.select.currentIndex() == 0:
            name = "choose_computer_algorithm"
            other_name = "choose_players_algorithm"
        else:
            name = "choose_players_algorithms"
            other_name = "choose_computer_algorithm"
        
        if self.v_main.findChild(QVBoxLayout, other_name):
            self.v_main.removeItem(self.algorithm_selection_options[(self.select.currentIndex() + 1) % 2])
            for i in range(self.algorithm_selection_options[(self.select.currentIndex() + 1) % 2]):
                self.algorithm_selection_options[(self.select.currentIndex() + 1) % 2].
            print("Micem ", other_name)
        if not self.v_main.findChild(QVBoxLayout, name):
            self.v_main.insertLayout(3, self.algorithm_selection_options[self.select.currentIndex()])
            print("Dodajem ", name)
        print("==========")
from gui.widgets.board_grid import BoardGrid
from PyQt5.QtWidgets import QWidget


class Board(QWidget):
    def __init__(self):
        super(Board, self).__init__()
        self.board_grid = BoardGrid()

        self.setLayout(self.board_grid)


from PyQt5.QtWidgets import *
from gui.tiles.figure_placement_tile import FigurePlacementTile
from gui.tiles.wall_placement_tile import WallPlacementTile


class BoardGrid(QGridLayout):
    def __init__(self):
        super(BoardGrid, self).__init__()
        self.setSpacing(0)
        # self.board = [[0] * 17, [0] * 17, [0] * 17, [0] * 17, [0] * 17, [0] * 17, [0] * 17, [0] * 17]
        self.board = []
        for i in range(17):
            self.board.append([0] * 17)
        self.generate_tiles()
        # self.setMargin(10)

    def generate_tiles(self):
        for i in range(17):
            for j in range(17):
                ##5e3901 -> wall
                ##ffffff -> figure
                if i % 2 == 0 and j % 2 == 0:
                    self.board[i][j] = FigurePlacementTile("#ffffff", i, j)
                    self.addWidget(self.board[i][j], i, j)
                else:
                    color = "#333"
                    self.board[i][j] = WallPlacementTile("#ff9945", i, j)
                    self.board[i][j].set_cursor_pointing(True)
                    self.addWidget(self.board[i][j], i, j)
                # self.board[i][j] = Tile(color, i, j)
                self.addWidget(self.board[i][j], i, j)

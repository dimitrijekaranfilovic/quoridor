from console.elements.piece import Piece
from console.elements.wall import Wall
import numpy as np
from console.elements.element import Element


class Board:
    def __init__(self, player_one_starting_pos, player_two_starting_pos):
        # self.board = []
        self.player_one_starting_pos = player_one_starting_pos
        self.player_two_starting_pos = player_two_starting_pos
        self.board = np.zeros((17, 17), dtype=Element)
        self.set_up_board()

    def set_up_board(self):
        for i in range(17):
            for j in range(17):
                # self.board.append([])
                if i % 2 == 0 and j % 2 == 0:
                    if i == self.player_one_starting_pos[0] and j == self.player_one_starting_pos[1]:
                        # self.board[i].append(Piece(True, "P1"))
                        self.board[i][j] = Piece(True, "P1")
                    elif i == self.player_two_starting_pos[0] and j == self.player_two_starting_pos[1]:
                        # self.board[i].append(Piece(True, "P2"))
                        self.board[i][j] = Piece(True, "P2")
                    else:
                        self.board[i][j] = (Piece())
                else:
                    self.board[i][j] = (Wall())

    def print_board(self):
        for i in range(17):
            for j in range(17):
                if i % 2 == 0 and j % 2 == 0:
                    if not self.board[i][j].is_occupied:
                        print("{0:4}".format(""), end="")
                    else:
                        print(" {0:2} ".format(self.board[i][j].name), end="")
                if i % 2 == 1 and j % 2 == 0:
                    if not self.board[i][j].is_occupied:
                        end = " "
                        if j != 16:
                            end = "x"
                        print("----", end=end)
                    else:
                        end = "  "
                        if j != 16:
                            end = "xx"
                        print("====", end=end)
                if i % 2 == 0 and j % 2 == 1:
                    if not self.board[i][j].is_occupied:
                        print("|", end="")
                    else:
                        print("||", end="")
            print()

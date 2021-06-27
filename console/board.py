from console.elements.piece import Piece
from console.elements.wall import Wall
import numpy as np
from console.elements.element import Element
from console.util.color import Color


class Board:
    def __init__(self, player_one_starting_pos, player_two_starting_pos):
        # self.board = []
        self.rows = 17
        self.cols = 17
        self.player_one_starting_pos = player_one_starting_pos
        self.player_two_starting_pos = player_two_starting_pos
        self.board = np.zeros((17, 17), dtype=Element)
        self.input_mappings = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10,
                               "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16}
        self.input_mappings_reversed = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J",
                                        10: "K",
                                        11: "L", 12: "M", 13: "N", 14: "O", 15: "P", 16: "Q"}
        self.input_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"]
        self.set_up_board()

    def set_up_board(self):
        wall_num = 0
        for i in range(self.rows):
            for j in range(self.cols):
                # self.board.append([])
                if i % 2 == 0 and j % 2 == 0:
                    if i == self.player_one_starting_pos[0] and j == self.player_one_starting_pos[1]:
                        self.board[i][j] = Piece(True, "P1")
                    elif i == self.player_two_starting_pos[0] and j == self.player_two_starting_pos[1]:
                        self.board[i][j] = Piece(True, "P2")
                    else:
                        self.board[i][j] = (Piece())
                else:
                    # if i == self.input_mappings["P"] and j == self.input_mappings["G"] or \
                    #         i == self.input_mappings["P"] and j == self.input_mappings["Q"]:
                    #     val = True
                    # else:
                    #     val = False
                    # if (i == 15 and j == 0) or (i == 14 and j == 1) or (i == 0 and j == 1):
                    #     val = True
                    # else:
                    #     val = False
                    self.board[i][j] = (Wall())
                    wall_num += 1

    def print_board(self):
        taken_wall_color = Color.YELLOW
        player_one_color = Color.GREEN
        player_two_color = Color.RED
        free_wall_color = Color.BLACK
        free_piece_place_color = Color.WHITE
        wall_column_color = Color.YELLOW

        for i in range(0, len(self.input_letters), 2):
            end_num = i + 1
            if i == 0:
                print(wall_column_color + "    {0:<1}".format(self.input_letters[i]) + Color.RESET,
                      end=free_piece_place_color + self.input_letters[i + 1].lower() + Color.RESET)

            elif end_num < 16:

                print(wall_column_color + "{0:<1}".format(self.input_letters[i]) + Color.RESET,
                      end=free_piece_place_color + self.input_letters[i + 1].lower() + Color.RESET)
            else:
                print(Color.MAGENTA + "{0:<3}".format(self.input_letters[i]) + Color.RESET, end=" ")
        print()

        for i in range(self.rows):
            if i % 2 == 0:
                print(free_piece_place_color + "{0:>2}  ".format(self.input_letters[i]) + Color.RESET, end="")
            else:
                print(wall_column_color + "{0:>2}  ".format(self.input_letters[i].lower()) + Color.RESET, end="")

            for j in range(self.cols):
                if i % 2 == 0 and j % 2 == 0:
                    if not self.board[i][j].is_occupied:
                        print(free_piece_place_color + u"\u25A0" + Color.RESET, end="")
                    else:
                        if self.board[i][j].name == "P1":
                            print(player_one_color + u"\u25A0" + Color.RESET, end="")
                        else:
                            print(player_two_color + u"\u25A0" + Color.RESET, end="")
                else:
                    if not self.board[i][j].is_occupied:
                        print(free_wall_color + u"\u25A0" + Color.RESET, end="")
                    else:
                        print(taken_wall_color + u"\u25A0" + Color.RESET, end="")

            print()

    # def print_board(self):
    #
    # for i in range(0, len(self.input_letters), 2):
    #     end_num = i + 1
    #     if i == 0:
    #         print("     {0:<1}  ".format(self.input_letters[i]),
    #               end=Color.YELLOW + self.input_letters[i + 1].lower() + Color.RESET)
    #
    #     elif end_num <= 16:
    #
    #         print(" {0:<1}  ".format(self.input_letters[i]),
    #               end=Color.YELLOW + self.input_letters[i + 1].lower() + Color.RESET)
    #     else:
    #         print("  {0:<3}".format(self.input_letters[i]), end=" ")
    # print()
    #
    #     for i in range(self.rows):
    #         if i % 2 == 0:
    #             print("{0:>2}  ".format(self.input_letters[i]), end="")
    #         else:
    #             print(Color.YELLOW + "{0:>2}  ".format(self.input_letters[i].lower()) + Color.RESET, end="")
    #         for j in range(self.cols):
    #             if i % 2 == 0 and j % 2 == 0:
    #                 if not self.board[i][j].is_occupied:
    #                     if j != 16:
    #                         print("{0:4}".format(""), end="")
    #                     else:
    #                         print("{0:4}".format(""), end=" ")
    #                 else:
    #                     if self.board[i][j].name == "P1":
    #                         color = Color.GREEN
    #                     else:
    #                         color = Color.RED
    #                     print(color + " {0:2} ".format(self.board[i][j].name) + Color.RESET, end="")
    #             elif i % 2 == 1 and j % 2 == 0:
    #                 if not self.board[i][j].is_occupied:
    #                     print("----", end=" ")
    #                 else:
    #                     print(Color.YELLOW + "====" + Color.RESET, end=" ")
    #             elif i % 2 == 0 and j % 2 == 1:
    #                 if not self.board[i][j].is_occupied:
    #                     print("|", end="")
    #                 else:
    #                     print(Color.YELLOW + "||" + Color.RESET, end="")
    #         print()

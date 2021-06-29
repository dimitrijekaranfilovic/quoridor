#from console.board import Board
from console.util.wall_direction import WallDirection
from exceptions.invalid_config_exception import InvalidConfigException
import numpy as np
#from console.elements.wall import Wall
from copy import copy, deepcopy
from console.search.astar import astar
from console.util.color import Color


class BoardPieceStatus:
    OCCUPIED_BY_PLAYER_1 = 1
    OCCUPIED_BY_PLAYER_2 = 2
    FREE_PLAYER = 3
    FREE_WALL = 4
    OCCUPIED_WALL = 5


class Mappings:
    INPUT_MAPPINGS = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10,
                      "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16}
    INPUT_MAPPINGS_REVERSED = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J",
                               10: "K",
                               11: "L", 12: "M", 13: "N", 14: "O", 15: "P", 16: "Q"}
    INPUT_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"]


class GameState:
    def __init__(self, config, initialize=True):
        """
        Config is a dictionary with the following keys:
            algorithms: array of algorithms used to calculate players' moves
        :param config:
        """
        # TODO: stavi 1D niz da bude tabla, pa radi shallow copy
        GameState.check_config(config)
        self.config = config
        self.is_simulation = len(config["algorithms"]) == 2

        # self.board = Board(self.player_one_pos, self.player_two_pos)
        self.player_one = True
        # self.value = 0
        self.rows = 17
        self.cols = 17

        if initialize:
            self.player_one_walls_num = 10
            self.player_two_wall_num = 10
            self.player_one_pos = np.array([16, 8])
            self.player_two_pos = np.array([0, 8])
            self.board = np.zeros((17, 17), dtype=int)
            self.set_up_board()

        # TODO: mozda stavi da imas kolekciju slobodnih mjesta za zidove, pa kad se koji zid stavi da se iz te kolekcije mice

    def copy(self):
        game_state = GameState(self.config, False)
        game_state.player_one_walls_num = self.player_one_walls_num
        game_state.player_two_wall_num = self.player_two_wall_num
        game_state.player_one_pos = np.copy(self.player_one_pos)
        game_state.player_two_pos = np.copy(self.player_two_pos)
        game_state.player_one = self.player_one
        game_state.board = np.copy(self.board)
        return game_state

    def set_up_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if i % 2 == 0 and j % 2 == 0:
                    self.board[i][j] = BoardPieceStatus.FREE_PLAYER
                else:
                    self.board[i][j] = BoardPieceStatus.FREE_WALL

        self.board[self.player_one_pos[0]][self.player_one_pos[1]] = BoardPieceStatus.OCCUPIED_BY_PLAYER_1
        self.board[self.player_two_pos[0]][self.player_two_pos[1]] = BoardPieceStatus.OCCUPIED_BY_PLAYER_2

    def print_board(self):

        for i in range(0, len(Mappings.INPUT_LETTERS), 2):
            end_num = i + 1
            if i == 0:
                print("      {0:<2} ".format(Mappings.INPUT_LETTERS[i]),
                      end=Color.YELLOW + Mappings.INPUT_LETTERS[i + 1].lower() + Color.RESET)

            elif end_num <= 16:

                print("  {0:<2} ".format(Mappings.INPUT_LETTERS[i]),
                      end=Color.YELLOW + Mappings.INPUT_LETTERS[i + 1].lower() + Color.RESET)
            else:
                print("  {0:<3}".format(Mappings.INPUT_LETTERS[i]), end=" ")
        print()

        for i in range(self.rows):
            if i % 2 == 0:
                print("{0:>2}  ".format(Mappings.INPUT_LETTERS[i]), end="")
            else:
                print(Color.YELLOW + "{0:>2}  ".format(Mappings.INPUT_LETTERS[i].lower()) + Color.RESET, end="")
            for j in range(self.cols):
                if self.board[i][j] == BoardPieceStatus.FREE_PLAYER:
                    print("{0:4}".format(""), end="")
                elif self.board[i][j] == BoardPieceStatus.OCCUPIED_BY_PLAYER_1:
                    print(Color.GREEN + " {0:2} ".format("P1") + Color.RESET, end="")
                elif self.board[i][j] == BoardPieceStatus.OCCUPIED_BY_PLAYER_2:
                    print(Color.RED + " {0:2} ".format("P2") + Color.RESET, end="")
                else:
                    if i % 2 == 1 and j % 2 == 0:
                        if self.board[i][j] == BoardPieceStatus.FREE_WALL:
                            line = ""
                            for k in range(5):
                                line += "\u23AF"
                            print(line, end="")
                        else:
                            line = ""
                            for k in range(5):
                                line += "\u2501"
                            print(Color.YELLOW + line + Color.RESET, end="")
                    elif i % 2 == 0 and j % 2 == 1:
                        if self.board[i][j] == BoardPieceStatus.FREE_WALL:
                            print(" |", end="")
                        else:
                            print(Color.YELLOW + " \u2503" + Color.RESET, end="")
                    elif i % 2 == 1 and j % 2 == 1:
                        if self.board[i][j] == BoardPieceStatus.FREE_WALL:
                            print("o", end="")
                        else:
                            print(Color.YELLOW + "O" + Color.RESET, end="")
            print()

    @staticmethod
    def check_config(config):
        if "algorithms" not in config.keys():
            raise InvalidConfigException("Config does not contain key 'algorithms'!")
        elif not isinstance(config["algorithms"], list):
            raise InvalidConfigException("Value for 'algorithms' key in config is not a list!")
        elif len(config["algorithms"]) != 1 and len(config["algorithms"]) != 2:
            raise InvalidConfigException("Invalid number of items in 'algorithms' in config!")

    def is_piece_occupied(self, i, j):
        return self.board[i][j] == BoardPieceStatus.OCCUPIED_BY_PLAYER_1 or self.board[i][
            j] == BoardPieceStatus.OCCUPIED_BY_PLAYER_2

    def is_not_piece_occupied(self, i, j):
        return not self.is_piece_occupied(i, j)

    def is_wall_occupied(self, i, j):
        return self.board[i][j] == BoardPieceStatus.OCCUPIED_WALL

    def is_not_wall_occupied(self, i, j):
        return not self.is_wall_occupied(i, j)

    # def is_occupied(self, i, j):
    #     return self.board.board[i][j].is_occupied

    # def is_not_occupied(self, i, j):
    #     return not self.board.board[i][j].is_occupied

    # def is_wall(self, i, j):
    #     return isinstance(self.board.board[i][j], Wall)
    #
    # def is_not_wall(self, i, j):
    #     return not isinstance(self.board.board[i][j], Wall)

    def is_jump(self, move):
        if self.player_one:
            return abs(self.player_one_pos[0] - move[0]) == 4
        else:
            return abs(self.player_two_pos[0] - move[0]) == 4

    def is_goal_state(self):
        if self.player_one:
            return self.player_one_pos[0] == 0
        else:
            return self.player_two_pos[0] == 16

    def get_child_states_with_moves(self):
        available_moves = self.get_available_moves()
        children = []
        for move in available_moves:
            child = copy(self)
            # child = self.copy()
            # child = deepcopy(self)
            child.move_piece(move)
            cost = 1
            if self.is_jump(move):
                cost = 0.5
            if child.player_one:
                pos = child.player_one_pos
            else:
                pos = child.player_two_pos
            # simplified_child_state = ((pos[0], pos[1]), (pos[0] - move[0], pos[1] - move[1]), cost)
            simplified_child_state = ((pos[0], pos[1]), (move[0], move[1]), cost)

            children.append((child, simplified_child_state))
        return children

    def get_all_child_states(self):
        children = []
        available_moves = self.get_available_moves()
        for move in available_moves:
            # child = deepcopy(self)
            # child = self.copy()
            child = copy(self)
            child.move_piece(move)
            child.player_one = not self.player_one
            children.append((child, (move[0], move[1])))
        # TODO: bug when calling the get_available_wall_placements function
        for child in self.get_available_wall_placements(True):
            children.append(child)
        return children

    def get_north_pos(self):
        """
        north_pos is the position one tile towards the opposite end of the board
        :param player_one: player one's turn
        :return: array which contains available move
        """

        if self.player_one:
            i, j = self.player_one_pos
            move = -2
            wall = -1
        else:
            i, j = self.player_two_pos
            move = 2
            wall = 1

        if 0 <= i + move <= 16 and 0 <= i + wall <= 16:
            # if self.is_not_occupied(i + move, j) and self.is_not_occupied(i + wall, j):
            if self.is_not_piece_occupied(i + move, j) and self.is_not_wall_occupied(i + wall, j):
                return np.array([i + move, j])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_south_pos(self):
        """
        south_pos is the position one tile towards the player's end of the board

        :param player_one: player one's turn
        :return: array which contains available move
        """

        if self.player_one:
            i, j = self.player_one_pos
            move_x = 2
            wall_x = 1
        else:
            i, j = self.player_two_pos
            move_x = -2
            wall_x = -1

        if 0 <= i + move_x <= 16 and 0 <= i + wall_x <= 16:
            # if self.is_not_occupied(i + wall_x, j) and self.is_not_occupied(i + move_x, j):
            if self.is_not_wall_occupied(i + wall_x, j) and self.is_not_piece_occupied(i + move_x, j):
                return np.array([i + move_x, j])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_west_pos(self):
        """
        west_pos is the position one tile towards the left side of the board from the player's perspective

        :param player_one: player one's turn
        :return: array which contains available move
        """

        if self.player_one:
            i, j = self.player_one_pos
            move_y = -2
            wall_y = -1
        else:
            i, j = self.player_two_pos
            move_y = 2
            wall_y = 1

        if 0 <= j + move_y <= 16 and 0 <= j + wall_y <= 16:
            # if self.is_not_occupied(i, j + move_y) and self.is_not_occupied(i, j + wall_y):
            if self.is_not_piece_occupied(i, j + move_y) and self.is_not_wall_occupied(i, j + wall_y):
                return np.array([i, j + move_y])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_east_pos(self):
        """
        east_pos is the position one tile towards the right side of the board from the player's perspective

        :param player_one: player one's turn
        :return: array which contains available move
        """

        if self.player_one:
            i, j = self.player_one_pos
            move_y = 2
            wall_y = 1
        else:
            i, j = self.player_two_pos
            move_y = -2
            wall_y = -1

        if 0 <= j + move_y <= 16 and 0 <= j + wall_y <= 16:
            # if self.is_not_occupied(i, j + move_y) and self.is_not_occupied(i, j + wall_y):
            if self.is_not_piece_occupied(i, j + move_y) and self.is_not_wall_occupied(i, j + wall_y):
                return np.array([i, j + move_y])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_jump_pos(self):
        """
        jump is available only if the north_pos is occupied by the opponent and behind him isn't a wall
        :param player_one: player one's turn
        :return: array which contains available move
        """

        if self.player_one:
            i, j = self.player_one_pos
            jump = -4
            move = -2
            wall1 = -1
            wall2 = -3
        else:
            i, j = self.player_two_pos
            jump = 4
            move = 2
            wall1 = 1
            wall2 = 3

        if 0 <= i + jump <= 16:
            # if self.is_not_occupied(i + wall1, j) and \
            #         self.is_occupied(i + move, j) and \
            #         self.is_not_occupied(i + wall2, j):
            if self.is_not_wall_occupied(i + wall1, j) and self.is_piece_occupied(i + move, j) and \
                    self.is_not_wall_occupied(i + wall2, j):
                return np.array([i + jump, j])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_northwest_pos(self):
        """
        northwest and northeast positions are only available
        :param player_one: player one's turn
        :return: array which contains available move
        """

        if self.player_one:
            i, j = self.player_one_pos
            move_x = -2
            move_y = -2
            wall_x = -1
            wall_y = -1
            occupied_x = -2
            occupied_wall = -3
        else:
            i, j = self.player_two_pos
            move_x = 2
            move_y = 2
            wall_x = 1
            wall_y = 1
            occupied_x = 2
            occupied_wall = 3

        if 0 <= i + move_x <= 16 and \
                0 <= j + move_y <= 16 and \
                0 <= i + wall_x <= 16 and \
                0 <= j + wall_y <= 16 and \
                0 <= i + occupied_x <= 16 and \
                0 <= i + occupied_wall <= 16:
            # if self.is_not_occupied(i + wall_x, j + wall_y) and \
            #         self.is_occupied(i + occupied_x, j) and \
            #         self.is_occupied(i + occupied_wall, j):
            if self.is_not_wall_occupied(i + wall_x, j + wall_y) and \
                    self.is_piece_occupied(i + occupied_x, j) and \
                    self.is_wall_occupied(i + occupied_wall, j):
                return np.array([i + move_x, j + move_y])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_northeast_pos(self):

        if self.player_one:
            i, j = self.player_one_pos
            move_x = -2
            move_y = 2
            wall_x = -1
            wall_y = 1
            occupied_x = -2
            occupied_wall = -3
        else:
            i, j = self.player_two_pos
            move_x = 2
            move_y = -2
            wall_x = 1
            wall_y = -1
            occupied_x = 2
            occupied_wall = 3

        if 0 <= i + move_x <= 16 and \
                0 <= j + move_y <= 16 and \
                0 <= i + wall_x <= 16 and \
                0 <= j + wall_y <= 16 and \
                0 <= i + occupied_x <= 16 and \
                0 <= i + occupied_wall <= 16:
            # if self.is_not_occupied(i + wall_x, j + wall_y) and \
            #         self.is_occupied(i + occupied_x, j) and \
            #         self.is_occupied(i + occupied_wall, j):
            if self.is_not_wall_occupied(i + wall_x, j + wall_y) and \
                    self.is_piece_occupied(i + occupied_x, j) and \
                    self.is_wall_occupied(i + occupied_wall, j):
                return np.array([i + move_x, j + move_y])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_available_moves(self):
        # print("Pozvao get_available_moves")
        north = self.get_north_pos()
        south = self.get_south_pos()
        east = self.get_east_pos()
        west = self.get_west_pos()
        jump = self.get_jump_pos()
        north_east = self.get_northeast_pos()
        north_west = self.get_northwest_pos()

        array = []
        if north.size != 0:
            array.append(north)
        if south.size != 0:
            array.append(south)
        if east.size != 0:
            array.append(east)
        if west.size != 0:
            array.append(west)
        if jump.size != 0:
            array.append(jump)
        if north_east.size != 0:
            array.append(north_east)
        if north_west.size != 0:
            array.append(north_west)
        return np.array(array)  # TODO: vidi je l ovdje greska, kao i u onim

    def check_wall_placement(self, starting_pos, direction):
        """

        :param starting_pos: position chosen to start a wall from
        :param direction: direction in which the second part of the wall is to be constructed
        :return: (bool, [int, int]] => bool to indicate whether the wall is possible and
        array of the coordinates of the second wall part
        """

        if self.player_one and self.player_one_walls_num == 0:
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        elif not self.player_one and self.player_two_wall_num == 0:
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        if starting_pos[0] % 2 == 1 and starting_pos[1] == 1:
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        # if self.is_occupied(starting_pos[0], starting_pos[1]):
        if self.is_wall_occupied(starting_pos[0], starting_pos[1]):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        if direction == WallDirection.NORTH:
            if starting_pos[1] % 2 == 0:
                return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
            else:
                second_piece_x = starting_pos[0] - 2
                second_piece_y = starting_pos[1]
                third_piece_x = starting_pos[0] - 1
                third_piece_y = starting_pos[1]
        elif direction == WallDirection.SOUTH:
            if starting_pos[1] % 2 == 0:
                return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
            else:
                second_piece_x = starting_pos[0] + 2
                second_piece_y = starting_pos[1]
                third_piece_x = starting_pos[0] + 1
                third_piece_y = starting_pos[1]
        elif direction == WallDirection.EAST:
            if starting_pos[1] % 2 == 1:
                return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
            else:
                second_piece_x = starting_pos[0]
                second_piece_y = starting_pos[1] + 2
                third_piece_x = starting_pos[0]
                third_piece_y = starting_pos[1] + 1

        else:  # WallDirection.WEST
            if starting_pos[1] % 2 == 1:
                return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
            else:
                second_piece_x = starting_pos[0]
                second_piece_y = starting_pos[1] - 2
                third_piece_x = starting_pos[0]
                third_piece_y = starting_pos[1] - 1

        if not 0 <= starting_pos[0] <= 16 and not 0 <= starting_pos[1] <= 16 \
                and not 0 <= second_piece_x <= 16 and not 0 <= second_piece_y <= 16 \
                and not 0 <= third_piece_x <= 16 and not 0 <= third_piece_y <= 16:
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        # if self.is_occupied(starting_pos[0], starting_pos[1]):
        #     return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        # if self.is_occupied(second_piece_x, second_piece_y):
        if self.is_wall_occupied(second_piece_x, second_piece_y):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        # if self.is_occupied(third_piece_x, third_piece_y):
        if self.is_wall_occupied(third_piece_x, third_piece_y):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        # check whether this wall blocks the opponent's last remaining path
        positions = np.array(
            [starting_pos[0], starting_pos[1], second_piece_x, second_piece_y, third_piece_x, third_piece_y])

        # copy_state = deepcopy(self)
        # copy_state = self.copy()
        copy_state = copy(self)

        if copy_state.is_wall_blocking(positions, not self.player_one):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        return True, positions

    def is_wall_blocking(self, positions, player_one):
        self.place_wall(positions)
        self.player_one = player_one
        return not astar(self, True)

    def get_available_wall_placements(self, include_state=False):
        wall_placements = []
        if self.player_one and self.player_one_walls_num == 0:
            return wall_placements
        elif not self.player_one and self.player_two_wall_num == 0:
            return wall_placements

        # vertical walls
        # for i in range(0, self.board.rows - 1, 2):
        for i in range(0, self.rows - 1, 2):
            # for j in range(1, self.board.cols, 2):
            for j in range(1, self.cols, 2):
                # if self.is_occupied(i, j):
                if self.is_wall_occupied(i, j):
                    continue
                second_part_x = i + 2
                third_part_x = i + 1
                # if self.is_occupied(second_part_x, j):
                if self.is_wall_occupied(second_part_x, j):
                    continue
                # if self.is_occupied(third_part_x, j):
                if self.is_wall_occupied(third_part_x, j):
                    continue
                positions = (i, j, second_part_x, j, third_part_x, j)
                copy_state = deepcopy(self)
                # copy_state = self.copy()
                # copy_state = copy(self)
                copy_state.place_wall(positions)
                copy_state.player_one = not self.player_one
                # if not copy_state.is_wall_blocking(positions, not self.player_one):

                if include_state:
                    wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)

        # horizontal walls
        # for i in range(1, self.board.rows, 2):
        for i in range(1, self.rows, 2):
            # for j in range(0, self.board.cols - 1, 2):
            for j in range(0, self.cols - 1, 2):
                # if self.is_occupied(i, j):
                if self.is_wall_occupied(i, j):
                    continue
                second_part_y = j + 2
                third_part_y = j + 1
                # if self.is_occupied(i, second_part_y):
                if self.is_wall_occupied(i, second_part_y):
                    continue
                # if self.is_occupied(i, third_part_y):
                if self.is_wall_occupied(i, third_part_y):
                    continue
                positions = (i, j, i, second_part_y, i, third_part_y)

                copy_state = deepcopy(self)
                # copy_state = self.copy()
                # copy_state = copy(self)
                copy_state.place_wall(positions)
                copy_state.player_one = not self.player_one
                # if not copy_state.is_wall_blocking(positions, not self.player_one):
                if include_state:
                    wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)

        return wall_placements

    def place_wall(self, positions):
        # self.board.board[positions[0]][positions[1]].is_occupied = True
        # self.board.board[positions[2]][positions[3]].is_occupied = True
        # self.board.board[positions[4]][positions[5]].is_occupied = True
        for i in range(0, 5, 2):
            self.board[positions[i]][positions[i + 1]] = BoardPieceStatus.OCCUPIED_WALL
        # self.board[positions[0]][positions[1]] = BoardPieceStatus.OCCUPIED_WALL
        # self.board[positions[]]

        if self.player_one:
            self.player_one_walls_num -= 1
        else:
            self.player_two_wall_num -= 1

    def move_piece(self, new_pos):
        new_i, new_j = new_pos

        if self.player_one:
            old_i, old_j = self.player_one_pos
            # self.player_one_pos = np.array([new_i, new_j])
            self.player_one_pos[0] = new_i
            self.player_one_pos[1] = new_j
            self.board[new_i][new_j] = BoardPieceStatus.OCCUPIED_BY_PLAYER_1
        else:
            old_i, old_j = self.player_two_pos
            # self.player_two_pos = np.array([new_i, new_j])
            self.player_two_pos[0] = new_i
            self.player_two_pos[1] = new_j
            self.board[new_i][new_j] = BoardPieceStatus.OCCUPIED_BY_PLAYER_2

        self.board[old_i][old_j] = BoardPieceStatus.FREE_PLAYER
        # self.board.board[old_i][old_j].is_occupied = False
        # self.board.board[old_i][old_j].name = ""
        #
        # self.board.board[new_i][new_j].is_occupied = True
        #
        # self.board.board[new_i][new_j].name = name

    def is_end_state(self):
        return self.player_one_pos[0] == 0 or self.player_two_pos[0] == 16

    def get_winner(self):
        if self.player_one_pos[0] == 0:
            return "P1"
        else:
            return "P2"

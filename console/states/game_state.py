from console.util.wall_direction import WallDirection
import numpy as np
from copy import copy
from console.search.astar import astar
from console.util.color import Color
import threading


# TODO: makni numpy
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
    def __init__(self, is_simulation=False, initialize=True):
        self.is_simulation = is_simulation
        self.player_one = True
        self.rows = 17
        self.cols = 17
        self.player_one_walls_num = 10
        self.player_two_wall_num = 10
        self.lock = threading.Lock()

        if initialize:
            self.player_one_pos = np.array([16, 8])
            self.player_two_pos = np.array([0, 8])

            self.board = np.zeros((289,), dtype=int)
            self.set_up_board()

    def set_up_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if i % 2 == 0 and j % 2 == 0:
                    self.board[i * self.cols + j] = BoardPieceStatus.FREE_PLAYER
                else:
                    self.board[i * self.cols + j] = BoardPieceStatus.FREE_WALL

        self.board[self.player_one_pos[0] * self.cols + self.player_one_pos[1]] = BoardPieceStatus.OCCUPIED_BY_PLAYER_1
        self.board[self.player_two_pos[0] * self.cols + self.player_two_pos[1]] = BoardPieceStatus.OCCUPIED_BY_PLAYER_2

    def copy(self):
        game_state = copy(self)
        game_state.player_one_pos = copy(self.player_one_pos)
        game_state.player_two_pos = copy(self.player_two_pos)
        game_state.board = copy(self.board)
        return game_state

    def print_game_stats(self):
        print(Color.GREEN + "{0:<15}".format("Player 1 walls") + Color.WHITE +
              "|" + Color.RED + "{0:<15}".format(
            "Player 2 walls") + Color.RESET,
              end="|\n")
        print("{0:-<15}|{1:-<15}".format("", ""), end="|\n")
        print("{0:<15}|{1:<15}|".format(self.player_one_walls_num, self.player_two_wall_num))

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
                index = i * self.cols + j
                if self.board[index] == BoardPieceStatus.FREE_PLAYER:
                    print("{0:4}".format(""), end="")
                elif self.board[index] == BoardPieceStatus.OCCUPIED_BY_PLAYER_1:
                    print(Color.GREEN + " {0:2} ".format("P1") + Color.RESET, end="")
                elif self.board[index] == BoardPieceStatus.OCCUPIED_BY_PLAYER_2:
                    print(Color.RED + " {0:2} ".format("P2") + Color.RESET, end="")
                else:
                    if i % 2 == 1 and j % 2 == 0:
                        if self.board[index] == BoardPieceStatus.FREE_WALL:
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
                        if self.board[index] == BoardPieceStatus.FREE_WALL:
                            print(" |", end="")
                        else:
                            print(Color.YELLOW + " \u2503" + Color.RESET, end="")
                    elif i % 2 == 1 and j % 2 == 1:
                        if self.board[index] == BoardPieceStatus.FREE_WALL:
                            print("o", end="")
                        else:
                            print(Color.YELLOW + "O" + Color.RESET, end="")
            print()

    def is_piece_occupied(self, i, j):
        index = i * self.cols + j
        return self.board[index] == BoardPieceStatus.OCCUPIED_BY_PLAYER_1 or self.board[
            index] == BoardPieceStatus.OCCUPIED_BY_PLAYER_2

    def is_not_piece_occupied(self, i, j):
        return not self.is_piece_occupied(i, j)

    def is_wall_occupied(self, i, j):
        return self.board[i * self.cols + j] == BoardPieceStatus.OCCUPIED_WALL

    def is_not_wall_occupied(self, i, j):
        return not self.is_wall_occupied(i, j)

    def is_jump(self, move):
        if self.player_one:
            return abs(self.player_one_pos[0] - move[0]) == 4
        else:
            return abs(self.player_two_pos[0] - move[0]) == 4

    def is_diagonal(self, move):
        if self.player_one:
            return abs(self.player_one_pos[0] - move[0]) == 2 and abs(self.player_one_pos[1] - move[1]) == 2
        else:
            return abs(self.player_two_pos[0] - move[0]) == 2 and abs(self.player_two_pos[1] - move[1]) == 2

    def is_goal_state(self):
        if self.player_one:
            return self.player_one_pos[0] == 0
        else:
            return self.player_two_pos[0] == 16

    def distance_to_goal(self):
        if self.player_one:
            return self.player_one_pos[0]
        else:
            return 16 - self.player_two_pos[0]

    def get_child_states_with_moves(self):
        available_moves = self.get_available_moves(False)
        children = []
        for move in available_moves:
            child = self.copy()
            child.move_piece(move)
            cost = 1000
            if self.is_jump(move):
                cost = 500
            elif self.is_diagonal(move):
                cost = 500
            if child.player_one:
                pos = child.player_one_pos
            else:
                pos = child.player_two_pos
            simplified_child_state = ((pos[0], pos[1]), (move[0], move[1]), cost)

            children.append((child, simplified_child_state))
        return children

    def get_all_child_states(self, player_one_maximizer, include_state=True):

        children = []
        available_moves = self.get_available_moves(include_state)
        for move in available_moves:
            children.append(move)

        available_wall_placements = []
        if not self.player_one and not player_one_maximizer:
            available_wall_placements = self.get_available_wall_placements_for_player_two(include_state)

        if self.player_one and player_one_maximizer:
            available_wall_placements = self.get_available_wall_placements_for_player_one(include_state)

        for wall_placement in available_wall_placements:
            children.append(wall_placement)

        return children

    def get_north_pos(self, include_state=True):

        if self.player_one:
            i, j = self.player_one_pos
            move = -2
            wall = -1
        else:
            i, j = self.player_two_pos
            move = 2
            wall = 1

        if 0 <= i + move <= 16 and 0 <= i + wall <= 16:
            if self.is_not_piece_occupied(i + move, j) and self.is_not_wall_occupied(i + wall, j):
                position = (i + move, j)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move_piece(position)
                    copy_state.player_one = not self.player_one
                    return copy_state, position
                else:
                    return position
            else:
                return None
        else:
            return None

    def get_south_pos(self, include_state=True):

        if self.player_one:
            i, j = self.player_one_pos
            move_x = 2
            wall_x = 1
        else:
            i, j = self.player_two_pos
            move_x = -2
            wall_x = -1

        if 0 <= i + move_x <= 16 and 0 <= i + wall_x <= 16:
            if self.is_not_wall_occupied(i + wall_x, j) and self.is_not_piece_occupied(i + move_x, j):
                position = (i + move_x, j)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move_piece(position)
                    copy_state.player_one = not self.player_one
                    return copy_state, position
                else:
                    return position
            else:
                return None
        else:
            return None

    def get_west_pos(self, include_state=True):

        if self.player_one:
            i, j = self.player_one_pos
            move_y = -2
            wall_y = -1
        else:
            i, j = self.player_two_pos
            move_y = 2
            wall_y = 1

        if 0 <= j + move_y <= 16 and 0 <= j + wall_y <= 16:
            if self.is_not_piece_occupied(i, j + move_y) and self.is_not_wall_occupied(i, j + wall_y):
                position = (i, j + move_y)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move_piece(position)
                    copy_state.player_one = not self.player_one
                    return copy_state, position
                else:
                    return position
            else:
                return None
        else:
            return None

    def get_east_pos(self, include_state=True):

        if self.player_one:
            i, j = self.player_one_pos
            move_y = 2
            wall_y = 1
        else:
            i, j = self.player_two_pos
            move_y = -2
            wall_y = -1

        if 0 <= j + move_y <= 16 and 0 <= j + wall_y <= 16:
            if self.is_not_piece_occupied(i, j + move_y) and self.is_not_wall_occupied(i, j + wall_y):
                position = (i, j + move_y)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move_piece(position)
                    copy_state.player_one = not self.player_one
                    return copy_state, position
                else:
                    return position
            else:
                return None
        else:
            return None

    def get_jump_pos(self, include_state=True):

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
            if self.is_not_wall_occupied(i + wall1, j) and self.is_piece_occupied(i + move, j) and \
                    self.is_not_wall_occupied(i + wall2, j):
                position = (i + jump, j)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move_piece(position)
                    copy_state.player_one = not self.player_one
                    return copy_state, position
                else:
                    return position
            else:
                return None
        else:
            return None

    def get_northwest_pos(self, include_state=True):

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
            if self.is_not_wall_occupied(i + wall_x, j + wall_y) and \
                    self.is_piece_occupied(i + occupied_x, j) and \
                    self.is_wall_occupied(i + occupied_wall, j):
                position = (i + move_x, j + move_y)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move_piece(position)
                    copy_state.player_one = not self.player_one
                    return copy_state, position
                else:
                    return position
            else:
                return None
        else:
            return None

    def get_northeast_pos(self, include_state=True):

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
            if self.is_not_wall_occupied(i + wall_x, j + wall_y) and \
                    self.is_piece_occupied(i + occupied_x, j) and \
                    self.is_wall_occupied(i + occupied_wall, j):
                position = (i + move_x, j + move_y)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move_piece(position)
                    copy_state.player_one = not self.player_one
                    return copy_state, position
                else:
                    return position
            else:
                return None
        else:
            return None

    def get_available_moves(self, include_state=True):
        north = self.get_north_pos(include_state)
        south = self.get_south_pos(include_state)
        east = self.get_east_pos(include_state)
        west = self.get_west_pos(include_state)
        jump = self.get_jump_pos(include_state)
        north_east = self.get_northeast_pos(include_state)
        north_west = self.get_northwest_pos(include_state)

        array = []

        if south is not None:
            array.append(south)
        if east is not None:
            array.append(east)
        if west is not None:
            array.append(west)
        if jump is not None:
            array.append(jump)
        if north_east is not None:
            array.append(north_east)
        if north_west is not None:
            array.append(north_west)
        if north is not None:
            array.append(north)
        return array

    def check_wall_placement(self, starting_pos, direction):

        if self.player_one and self.player_one_walls_num == 0:
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        elif not self.player_one and self.player_two_wall_num == 0:
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        if starting_pos[0] % 2 == 1 and starting_pos[1] == 1:
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

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
            if starting_pos[0] % 2 == 0:
                return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
            else:
                second_piece_x = starting_pos[0]
                second_piece_y = starting_pos[1] + 2
                third_piece_x = starting_pos[0]
                third_piece_y = starting_pos[1] + 1

        else:  # WallDirection.WEST
            if starting_pos[0] % 2 == 0:
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

        if self.is_wall_occupied(second_piece_x, second_piece_y):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        if self.is_wall_occupied(third_piece_x, third_piece_y):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        # check whether this wall blocks the opponent's last remaining path
        positions = np.array(
            [starting_pos[0], starting_pos[1], second_piece_x, second_piece_y, third_piece_x, third_piece_y])

        copy_state = copy(self)

        if copy_state.is_wall_blocking(positions, not self.player_one):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        return True, positions

    def is_wall_blocking(self, positions, player_one):
        self.place_wall(positions)
        self.player_one = player_one
        return not astar(self, True)

    def get_available_wall_placements_for_player_one(self, include_state=True):
        wall_placements = []

        if self.player_one_walls_num == 0:
            return wall_placements

        start_row = max(self.player_two_pos[0] - 2, 0)
        end_row = min(self.player_two_pos[0] + 3, 16)
        start_col = max(self.player_one_pos[1] - 3, 0)
        end_col = min(self.player_one_pos[1] + 3, 16)

        # horizontal
        end = end_col - 3
        if end_col == 16:
            end = end_col + 1
        start_1 = start_col + 1
        if start_col == 0:
            start_1 = start_col
            end = end_col - 2
        for i in range(start_row + 1, end_row, 2):
            for j in range(start_1, end, 2):
                if self.is_wall_occupied(i, j):
                    continue
                second_part_y = j + 2
                third_part_y = j + 1
                if not start_col <= second_part_y <= end_col:
                    continue
                if not start_col <= third_part_y <= end_col:
                    continue
                if self.is_wall_occupied(i, second_part_y):
                    continue
                if self.is_wall_occupied(i, third_part_y):
                    continue
                positions = (i, j, i, second_part_y, i, third_part_y)
                if include_state:
                    copy_state = self.copy()
                    if not copy_state.is_wall_blocking(positions, not self.player_one):
                        wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)
        # vertical
        start_2 = start_col
        if start_2 == 0:
            start_2 = start_col + 1
        for i in range(start_row, end_row - 3, 2):
            for j in range(start_2, end_col + 1, 2):
                if self.is_wall_occupied(i, j):
                    continue
                second_part_x = i + 2
                third_part_x = i + 1
                if not start_row <= second_part_x <= end_row:
                    continue
                if not start_row <= third_part_x <= end_row:
                    continue
                if self.is_wall_occupied(second_part_x, j):
                    continue
                if self.is_wall_occupied(third_part_x, j):
                    continue
                positions = (i, j, second_part_x, j, third_part_x, j)
                if include_state:
                    copy_state = self.copy()
                    if not copy_state.is_wall_blocking(positions, not self.player_one):
                        wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)

        return wall_placements

    def get_available_wall_placements_for_player_two(self, include_state=True):
        wall_placements = []

        if self.player_two_wall_num == 0:
            return wall_placements

        # TODO: vidi za vertikalne zidove

        start_row = max(self.player_one_pos[0] - 3, 0)
        end_row = min(self.player_one_pos[0] + 2, 16)
        start_col = max(self.player_one_pos[1] - 3, 0)
        end_col = min(self.player_one_pos[1] + 3, 16)
        # horizontal
        end = end_col - 3
        if end_col == 16:
            end = end_col + 1
        start_1 = start_col + 1
        if start_col == 0:
            start_1 = start_col
            end = end_col - 2
        for i in range(start_row, end_row, 2):
            for j in range(start_1, end, 2):
                if self.is_wall_occupied(i, j):
                    continue
                second_part_y = j + 2
                third_part_y = j + 1
                if not start_col <= second_part_y <= end_col:
                    continue
                if not start_col <= third_part_y <= end_col:
                    continue
                if self.is_wall_occupied(i, second_part_y):
                    continue
                if self.is_wall_occupied(i, third_part_y):
                    continue
                positions = (i, j, i, second_part_y, i, third_part_y)
                if include_state:
                    copy_state = self.copy()
                    if not copy_state.is_wall_blocking(positions, not self.player_one):
                        wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)

        # vertical
        start_2 = start_col
        if start_2 == 0 and start_row != 0:
            start_2 = start_col + 1
        if start_2 == 0 and start_row == 0:
            start_2 = start_col
        end_1 = end_col + 1
        if end_col == 16:
            end_1 = 15

        start_3 = start_row + 1
        if start_row == 0:
            start_3 = 0
        for i in range(start_3, end_row - 3, 2):
            for j in range(start_2, end_1, 2):
                if self.is_wall_occupied(i, j):
                    continue
                second_part_x = i + 2
                third_part_x = i + 1
                if not start_row <= second_part_x <= end_row:
                    continue
                if not start_row <= third_part_x <= end_row:
                    continue
                if self.is_wall_occupied(second_part_x, j):
                    continue
                if self.is_wall_occupied(third_part_x, j):
                    continue
                positions = (i, j, second_part_x, j, third_part_x, j)
                if include_state:
                    copy_state = self.copy()
                    if not copy_state.is_wall_blocking(positions, not self.player_one):
                        wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)
        return wall_placements

    def execute_action(self, action, execute_on_copy=True):
        if execute_on_copy:
            state = self.copy()
        else:
            state = self
        if len(action) == 2:
            state.move_piece(action)
        else:
            state.place_wall(action)

        if execute_on_copy:
            state.player_one = not self.player_one
        return state

    def place_wall(self, positions):
        for i in range(0, 5, 2):
            self.board[positions[i] * self.cols + positions[i + 1]] = BoardPieceStatus.OCCUPIED_WALL

        if self.player_one:
            self.player_one_walls_num -= 1
        else:
            self.player_two_wall_num -= 1

    def move_piece(self, new_pos):
        new_i, new_j = new_pos

        if self.player_one:
            old_i, old_j = self.player_one_pos
            self.player_one_pos[0] = new_i
            self.player_one_pos[1] = new_j
            self.board[new_i * self.cols + new_j] = BoardPieceStatus.OCCUPIED_BY_PLAYER_1
        else:
            old_i, old_j = self.player_two_pos
            self.player_two_pos[0] = new_i
            self.player_two_pos[1] = new_j
            self.board[new_i * self.cols + new_j] = BoardPieceStatus.OCCUPIED_BY_PLAYER_2

        self.board[old_i * self.cols + old_j] = BoardPieceStatus.FREE_PLAYER

    def is_end_state(self):
        return self.player_one_pos[0] == 0 or self.player_two_pos[0] == 16

    def game_result(self, player_one_maximizer=False):
        if player_one_maximizer:
            if self.player_one_pos[0] == 0:
                return 1
            else:
                return -1
        else:
            if self.player_two_pos[0] == 16:
                return 1
            else:
                return -1

    def get_winner(self):
        if self.player_one_pos[0] == 0:
            return "P1"
        else:
            return "P2"

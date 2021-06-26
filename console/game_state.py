from console.board import Board
from exceptions.invalid_config_exception import InvalidConfigException
import numpy as np


class GameState:
    def __init__(self, config):
        """
        Config is a dictionary with the following keys:
            algorithms: array of algorithms used to calculate players' moves
        :param config:
        """

        GameState.check_config(config)

        self.is_simulation = len(config["algorithms"]) == 2
        self.player_one_pos = np.array([16, 8])
        self.player_two_pos = np.array([0, 8])
        self.player_one_walls_num = 10
        self.player_two_wall_num = 10
        self.board = Board(self.player_one_pos, self.player_two_pos)

    @staticmethod
    def check_config(config):
        if "algorithms" not in config.keys():
            raise InvalidConfigException("Config does not contain key 'algorithms'!")
        elif not isinstance(config["algorithms"], list):
            raise InvalidConfigException("Value for 'algorithms' key in config is not a list!")
        elif len(config["algorithms"]) != 1 and len(config["algorithms"]) != 2:
            raise InvalidConfigException("Invalid number of items in 'algorithms' in config!")

    def is_occupied(self, i, j):
        return self.board.board[i][j].is_occupied

    def is_not_occupied(self, i, j):
        return not self.board.board[i][j].is_occupied

    def get_north_pos(self, player_one):
        """
        north_pos is the position one tile towards the opposite end of the board
        :param player_one: player one's turn
        :return: array which contains available move
        """

        if player_one:
            i, j = self.player_one_pos
            move = -2
            wall = -1
        else:
            i, j = self.player_two_pos
            move = 2
            wall = 1

        if 0 <= i + move <= 16 and 0 <= i + wall <= 16:
            if self.is_not_occupied(i + move, j) and self.is_not_occupied(i + wall, j):
                return np.array([i + move, j])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_south_pos(self, player_one):
        """
        south_pos is the position one tile towards the player's end of the board

        :param player_one: player one's turn
        :return: array which contains available move
        """

        if player_one:
            i, j = self.player_one_pos
            move_x = 2
            wall_x = 1
        else:
            i, j = self.player_two_pos
            move_x = -2
            wall_x = -1

        if 0 <= i + move_x <= 16 and 0 <= i + wall_x <= 16:
            if self.is_not_occupied(i + wall_x, j) and self.is_not_occupied(i + move_x, j):
                return np.array([i + move_x, j])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_west_pos(self, player_one):
        """
        west_pos is the position one tile towards the left side of the board from the player's perspective

        :param player_one: player one's turn
        :return: array which contains available move
        """

        if player_one:
            i, j = self.player_one_pos
            move_y = -2
            wall_y = -1
        else:
            i, j = self.player_two_pos
            move_y = 2
            wall_y = 1

        if 0 <= j + move_y <= 16 and 0 <= j + wall_y <= 16:
            if self.is_not_occupied(i, j + move_y) and self.is_not_occupied(i, j + wall_y):
                return np.array([i, j + move_y])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_east_pos(self, player_one):
        """
        east_pos is the position one tile towards the right side of the board from the player's perspective

        :param player_one: player one's turn
        :return: array which contains available move
        """

        if player_one:
            i, j = self.player_one_pos
            move_y = 2
            wall_y = 1
        else:
            i, j = self.player_two_pos
            move_y = -2
            wall_y = -1

        if 0 <= j + move_y <= 16 and 0 <= j + wall_y <= 16:
            if self.is_not_occupied(i, j + move_y) and self.is_not_occupied(i, j + wall_y):
                return np.array([i, j + move_y])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_jump_pos(self, player_one):
        """
        jump is available only if the north_pos is occupied by the opponent and behind him isn't a wall
        :param player_one: player one's turn
        :return: array which contains available move
        """

        if player_one:
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
            if self.is_not_occupied(i + wall1, j) and self.is_occupied(i + move, j) and self.is_not_occupied(i + wall2,
                                                                                                             j):
                return np.array([i + jump, j])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_northwest_pos(self, player_one):
        """
        northwest and northeast positions are only available
        :param player_one: player one's turn
        :return: array which contains available move
        """

        if player_one:
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

        if 0 <= i + move_x <= 16 and 0 <= j + move_y <= 16 and \
                0 <= i + wall_x <= 16 and 0 <= j + wall_y <= 16 and 0 <= i + occupied_x <= 16:
            if self.is_not_occupied(i + wall_x, j + wall_y) and self.is_occupied(i + occupied_x, j) and self.is_occupied(i + occupied_wall, j):
                return np.array([i + move_x, j + move_y])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_northeast_pos(self, player_one):

        if player_one:
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

        if 0 <= i + move_x <= 16 and 0 <= j + move_y <= 16 and 0 <= i + wall_x <= 16 and 0 <= j + wall_y <= 16 and 0 <= i + occupied_x <= 16:
            if self.is_not_occupied(i + wall_x, j + wall_y) and self.is_occupied(i + occupied_x, j) and self.is_occupied(i + occupied_wall, j):
                return np.array([i + move_x, j + move_y])
            else:
                return np.array([])
        else:
            return np.array([])

    def get_available_moves(self, player_one):
        north = self.get_north_pos(player_one)
        south = self.get_south_pos(player_one)
        east = self.get_east_pos(player_one)
        west = self.get_west_pos(player_one)
        jump = self.get_jump_pos(player_one)
        north_east = self.get_northeast_pos(player_one)
        north_west = self.get_northwest_pos(player_one)

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
        return np.array(array)

    def get_available_wall_placements(self):
        pass

    def move_piece(self, player_one, new_pos):
        new_i, new_j = new_pos

        if player_one:
            old_i, old_j = self.player_one_pos
            self.player_one_pos = np.array([new_i, new_j])
            name = "P1"
        else:
            old_i, old_j = self.player_two_pos
            self.player_two_pos = np.array([new_i, new_j])
            name = "P2"

        self.board.board[old_i][old_j].is_occupied = False
        self.board.board[old_i][old_j].name = ""

        self.board.board[new_i][new_j].is_occupied = True

        self.board.board[new_i][new_j].name = name

    def is_end_state(self):
        return self.player_one_pos[0] == 0 or self.player_two_pos[0] == 16

    def get_winner(self):
        if self.player_one_pos[0] == 0:
            return "P1"
        else:
            return "P2"

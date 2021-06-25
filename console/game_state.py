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
        self.is_game_finished = False
        # self.player_one_turn = True

    @staticmethod
    def check_config(config):
        if "algorithms" not in config.keys():
            raise InvalidConfigException("Config does not contain key 'algorithms'!")
        elif not isinstance(config["algorithms"], list):
            raise InvalidConfigException("Value for 'algorithms' key in config is not a list!")
        elif len(config["algorithms"]) != 1 and len(config["algorithms"]) != 2:
            raise InvalidConfigException("Invalid number of items in 'algorithms' in config!")

    @staticmethod
    def is_occupied(board, i, j):
        return board.board[i][j].is_occupied

    @staticmethod
    def is_not_occupied(board, i, j):
        return not board.board[i][j].is_occupied

    @staticmethod
    def get_north_pos(pos, player_one, board):
        """
        north_pos is the position one tile towards the opposite end of the board
        :param pos: position of the piece whose move is to be checked
        :param player_one: player one's turn
        :param board current board state
        :return: array which contains available move
        """
        i, j = pos

        if player_one:
            move = -2
            wall = -1
        else:
            move = 2
            wall = 1

        if GameState.is_not_occupied(board, i + move, j) and GameState.is_not_occupied(board, i + wall, j) \
                and 0 <= i + move <= 16:
            return np.array([i + move, j])
        return np.array([])

    @staticmethod
    def get_south_pos(pos, player_one, board):
        """
        south_pos is the position one tile towards the player's end of the board

        :param pos: position of the piece whose move is to be checked
        :param player_one: player one's turn
        :param board: current board state
        :return: array which contains available move
        """

        i, j = pos
        if player_one:
            move_x = 2
            wall_x = 1
        else:
            move_x = -2
            wall_x = -1
        if 0 <= i + move_x <= 16 and GameState.is_not_occupied(board, i + wall_x, j) and \
                GameState.is_not_occupied(board, i + move_x, j):
            return np.array([i + move_x, j])
        return np.array([])

    @staticmethod
    def get_west_pos(pos, player_one, board):
        """
        west_pos is the position one tile towards the left side of the board from the player's perspective

        :param pos: position of the piece whose move is to be checked
        :param player_one: player one's turn
        :param board: current board state
        :return: array which contains available move
        """

        i, j = pos
        if player_one:
            move_y = -2
            wall_y = -1
        else:
            move_y = 2
            wall_y = 1

        if 0 <= j + move_y <= 16 and GameState.is_not_occupied(board, i, j + move_y) and \
                GameState.is_not_occupied(board, i, j + wall_y):
            return np.array([i, j + move_y])

    @staticmethod
    def get_east_pos(pos, player_one, board):
        """
        east_pos is the position one tile towards the right side of the board from the player's perspective

        :param pos: position of the piece whose move is to be checked
        :param player_one: player one's turn
        :param board: current board state
        :return: array which contains available move
        """

        i, j = pos
        if player_one:
            move_y = 2
            wall_y = 1
        else:
            move_y = -2
            wall_y = -1

        if 0 <= j + move_y <= 16 and GameState.is_not_occupied(board, i, j + move_y) and \
                GameState.is_not_occupied(board, i, j + wall_y):
            return np.array([i, j + move_y])
        return np.array([])

    @staticmethod
    def get_jump_pos(pos, player_one, board):
        """
        jump is available only if the north_pos is occupied by the opponent and behind him isn't a wall
        :param pos: position of the piece whose move is to be checked
        :param player_one: player one's turn
        :param board: current board state
        :return: array which contains available move
        """
        i, j = pos

        if player_one:
            jump = -4
            move = -2
            wall1 = -1
            wall2 = -3
        else:
            jump = 4
            move = 2
            wall1 = 1
            wall2 = 3

        if GameState.is_not_occupied(board, i + wall1, j) and GameState.is_occupied(board, i + move, j) \
                and GameState.is_not_occupied(board, i + wall2, j) and 0 <= i + jump <= 16:
            return np.array([i + jump, j])
        return np.array([])

    @staticmethod
    def get_northwest_pos(pos, player_one, board):
        """
        northwest and northeast positions are only available
        :param pos: position of the piece whose move is to be checked
        :param player_one: player one's turn
        :param board: current board state
        :return: array which contains available move
        """
        i, j = pos

        if player_one:
            move_x = -2
            move_y = -2
            wall_x = -1
            wall_y = -1
            occupied_x = -2
        else:
            move_x = 2
            move_y = 2
            wall_x = 1
            wall_y = 1
            occupied_x = 2

        if 0 <= i + move_x <= 16 and 0 <= j + move_y <= 16 \
                and GameState.is_not_occupied(board, i + wall_x, j + wall_y) \
                and GameState.is_occupied(board, i + occupied_x, j):
            return np.array([i + move_x, j + move_y])
        return np.array([])

    @staticmethod
    def get_northeast_pos(pos, player_one, board):
        i, j = pos

        if player_one:
            move_x = -2
            move_y = 2
            wall_x = -1
            wall_y = 1
            occupied_x = -2
        else:
            move_x = 2
            move_y = -2
            wall_x = 1
            wall_y = -1
            occupied_x = 2
        if 0 <= i + move_x <= 16 and 0 <= j + move_y <= 16 and GameState.is_not_occupied(board, i + wall_x,
                                                                                         j + wall_y) and \
                GameState.is_occupied(board, i + occupied_x, j):
            return np.array([i + move_x, j + move_y])
        return np.array([])

    @staticmethod
    def get_available_moves(player_one, pos, board):
        north = GameState.get_north_pos(pos, player_one, board)
        south = GameState.get_south_pos(pos, player_one, board)
        east = GameState.get_east_pos(pos, player_one, board)
        west = GameState.get_west_pos(pos, player_one, board)
        jump = GameState.get_jump_pos(pos, player_one, board)
        north_east = GameState.get_northeast_pos(pos, player_one, board)
        north_west = GameState.get_northwest_pos(pos, player_one, board)

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

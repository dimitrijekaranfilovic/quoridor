from console.states.game_state import GameState
from time import time
from console.util.wall_direction import WallDirection
from console.util.color import Color
import numpy as np
from random import choice


class Game:
    def __init__(self):
        self.game_state = GameState({"algorithms": ["minmax"]})
        # self.player_one_turn = True

    def player_one_user(self):
        while True:
            value = input("Current number of walls: {0:<2}\nEnter move[Mx,y or WxV | WxH]: ".format(
                self.game_state.player_one_walls_num))
            if value == "x" or value == "X":
                exit(0)
            else:
                if value.upper().startswith("M"):
                    x_string, y_string = value[1:].split(",")
                    if x_string.upper() not in self.game_state.board.input_mappings.keys() or y_string.upper() not in self.game_state.board.input_mappings.keys():
                        Game.print_colored_output("Illegal move!", Color.RED)
                    else:
                        x_int = self.game_state.board.input_mappings[x_string.upper()]
                        y_int = self.game_state.board.input_mappings[y_string.upper()]
                        available_moves = self.game_state.get_available_moves()

                        counter = 0
                        for i in range(len(available_moves)):
                            if available_moves[i][0] == x_int and available_moves[i][1] == y_int:
                                break
                            else:
                                counter += 1

                        if counter == len(available_moves):
                            Game.print_colored_output("Illegal move!", Color.RED)
                        else:
                            # player 1 make a move
                            self.game_state.move_piece(np.array([x_int, y_int]))
                            break

                        counter = 0
                elif value.upper().startswith("W"):
                    # place a wall
                    x_string, y_string = value[1:len(value) - 1].split(",")
                    if x_string.upper() not in self.game_state.board.input_mappings.keys() or y_string.upper() not in self.game_state.board.input_mappings.keys():
                        Game.print_colored_output("Illegal wall placement!", Color.RED)
                    else:
                        dir_string = value[-1]
                        direction = WallDirection.NORTH
                        if dir_string in ["N", "S", "E", "W"]:

                            if dir_string == "S":
                                direction = WallDirection.SOUTH
                            elif dir_string == "E":
                                direction = WallDirection.EAST
                            elif dir_string == "W":
                                direction = WallDirection.WEST
                            else:
                                direction = WallDirection.NORTH

                            x_int = self.game_state.board.input_mappings[x_string.upper()]
                            y_int = self.game_state.board.input_mappings[y_string.upper()]
                            is_placement_valid, coords = self.game_state.check_wall_placement(np.array([x_int, y_int]),
                                                                                              direction)
                            if not is_placement_valid:
                                Game.print_colored_output("Illegal wall placement!", Color.RED)
                            else:
                                self.game_state.place_wall(coords)
                                break

                else:
                    Game.print_colored_output("Illegal command!", Color.RED)

    def player_one_simulation(self):
        pass

    def player_two_simulation(self):
        t1 = time()
        print("Player 2 is thinking...\n")
        available_moves = self.game_state.get_available_moves()
        move = choice(available_moves)
        self.game_state.move_piece(move)
        t2 = time()
        self.print_colored_output(
            "He moved the piece to (" + self.game_state.board.input_mappings_reversed[move[0]] + ", " +
            self.game_state.board.input_mappings_reversed[move[1]] + ")",
            Color.CYAN)
        self.print_colored_output("It took him " + str(round(t2 - t1, 2)) + " seconds.", Color.CYAN)

    def check_end_state(self):
        if self.game_state.is_end_state():
            winner = self.game_state.get_winner()
            if not self.game_state.is_simulation:
                if winner == "P1":
                    self.print_colored_output("You won!", Color.GREEN)
                else:
                    self.print_colored_output("You lost!", Color.RED)
            else:
                self.print_colored_output("The winner is " + winner, Color.CYAN)
            return True
        else:
            return False

    def play(self):
        Game.print_colored_output("### QUORIDOR ###\n\n", Color.CYAN)
        # print_rules()
        while True:
            print()
            self.game_state.board.print_board()
            print()

            if self.check_end_state():
                break

            if self.game_state.player_one:
                if not self.game_state.is_simulation:
                    self.player_one_user()
                else:
                    self.player_one_simulation()
            else:
                self.player_two_simulation()

            # self.player_one_turn = not self.player_one_turn
            self.game_state.player_one = not self.game_state.player_one

    @staticmethod
    def print_colored_output(text, color):
        print(color + text + Color.RESET)

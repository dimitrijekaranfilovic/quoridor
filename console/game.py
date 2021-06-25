from console.game_state import GameState
from time import sleep
from console.util.Color import Color
import numpy as np


class Game:
    def __init__(self):
        self.game_state = GameState({"algorithms": ["minmax"]})
        self.player_one_turn = True
        self.input_mapping = {
            1: 0,
            2: 2,
            3: 4,
            4: 6,
            5: 8,
            6: 10,
            7: 12,
            8: 14,
            9: 16
        }

    def play(self):
        Game.print_colored_output("### QUORIDOR ###\n\n", Color.CYAN)
        while True:
            Game.print_colored_output(
                "=========================================================================================", Color.CYAN)
            self.game_state.board.print_board()
            print()
            if self.player_one_turn:
                if not self.game_state.is_simulation:
                    available_moves = GameState.get_available_moves(True, self.game_state.player_one_pos,
                                                                    self.game_state.board)
                    print(available_moves)
                    value = input("Enter coordinates[x,y]: ")
                    print()
                    if value == "x" or value == "X":
                        break
                    else:
                        x_string, y_string = value.split(",")
                        x_int = int(x_string)
                        y_int = int(y_string)

                        # available_moves = GameState.get_available_moves(True, self.game_state.player_one_pos,
                        #                                                 self.game_state.board)
                        # print(available_moves)
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
                            pass
                        counter = 0
                else:
                    print("Player 1 is thinking...\n")
                    sleep(2)
            else:
                # player 2 make a move
                pass
                # print("Player 2 is thinking...\n")
                # sleep(0.5)
            # play ...
            if self.game_state.is_game_finished:
                break
            # self.player_one_turn = not self.player_one_turn
            Game.print_colored_output(
                "=========================================================================================", Color.CYAN)

    @staticmethod
    def print_colored_output(text, color):
        print(color + text + Color.RESET)

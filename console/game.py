from console.game_state import GameState
from time import sleep

class Game:
    def __init__(self):
        self.game_state = GameState({"algorithms": ["minmax", "alpha-beta"]})
        self.player_one_turn = True

    def play(self):
        print("### QUORIDOR ###\n\n")
        while True:
            self.game_state.board.print_board()
            if self.player_one_turn:
                if not self.game_state.is_simulation:
                    x = input("Enter option: ")
                    print()
                    if x == "x" or x == "X":
                        break
                else:
                    print("Player 1 is thinking...\n")
                    sleep(2)
            else:
                print("Player 2 is thinking...\n")
                sleep(3)
            ## play ...
            self.player_one_turn = not self.player_one_turn

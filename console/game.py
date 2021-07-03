from console.states.game_state import GameState, Mappings
from time import time, sleep
from console.util.wall_direction import WallDirection
from console.util.color import Color
from console.algorithms.minimax import minimax
from console.algorithms.minimax_alpha_beta_pruning import minimax_alpha_beta_pruning
from console.algorithms.expectimax import expectimax
from console.algorithms.monte_carlo_tree_search import SearchNode
import math


class Game:
    def __init__(self):

        self.player_simulation_algorithms = ["minimax", "minimax"]
        self.game_state = GameState()
        self.algorithms = ["minimax", "minimax-alpha-beta-pruning", "expectimax", "monte-carlo-tree-search"]
        self.execution_times = []

        self.initialize()

    def print_commands(self):
        print(
            "1. You can move your piece by entering" + Color.CYAN + " mx,y " + Color.RESET + "where x is the row letter and y column letter")
        print(
            "2. You can place a wall by entering" + Color.CYAN + " wx,yd " + Color.RESET + "where d represents the wall direction and")
        print("it can be one of [S, N, E, W]. They represent the south, north, east and west orientations.")
        print("3. When it's your turn, you can also press " + Color.CYAN + " x " + Color.RESET + " to exit the game.")

    def initialize(self):
        Game.print_colored_output("### WELCOME TO QUORIDOR ###", Color.CYAN)
        print("\n")
        print("First the commands [they are case insensitive]: ")
        self.print_commands()
        print("{0:-<100}".format(""))

        a = input("\nDo you want to play against a computer?[Y/n]: ")
        if a == "Y" or a == "y":
            self.game_state.is_simulation = False

            print("Choose the second player algorithm: ")
            print("1. minimax")
            print("2. minimax with alpha beta pruning")
            print("3. expectimax")
            print("4. monte carlo tree search")
            while True:
                x = input("Choose: ")
                if not x.isdigit() and x != "x" and x != "X":
                    Game.print_colored_output("Illegal input!", Color.RED)
                elif x == "x" or x == "X":
                    exit(0)
                else:
                    if 0 <= int(x) - 1 < len(self.algorithms):
                        self.player_simulation_algorithms[1] = self.algorithms[int(x) - 1]
                        Game.print_colored_output("Chosen algorithm for player 2 is {0:30}".format(
                            self.player_simulation_algorithms[1].upper()), Color.CYAN)
                        break
                    else:
                        Game.print_colored_output("Illegal input!", Color.RED)
        else:
            self.game_state.is_simulation = True
            print("Choose the players algorithms[first_player, second_player]")
            print("1. minimax")
            print("2. minimax with alpha beta pruning")
            print("3. expectimax")
            print("4. monte carlo tree search")
            while True:
                x = input("Choose: ")
                if not len(x.split(",")) == 2 and x != "x" and x != "X":
                    Game.print_colored_output("Illegal input!", Color.RED)
                elif x == "x" or x == "X":
                    exit(0)
                else:
                    one, two = x.split(",")
                    if 0 <= int(one) - 1 < len(self.algorithms) and 0 <= int(two) - 1 < len(self.algorithms):
                        self.player_simulation_algorithms[0] = self.algorithms[int(one) - 1]
                        self.player_simulation_algorithms[1] = self.algorithms[int(two) - 1]
                        Game.print_colored_output("Chosen algorithm for player 1 is {0:30}".format(
                            self.player_simulation_algorithms[0].upper()), Color.CYAN)
                        Game.print_colored_output("Chosen algorithm for player 2 is {0:30}".format(
                            self.player_simulation_algorithms[1].upper()), Color.CYAN)
                        break
                    else:
                        Game.print_colored_output("Illegal input!", Color.RED)

    def choose_action(self, d):
        if len(d.keys()) == 0:
            return None
        k = max(d)
        winner = d[k]
        action = winner[1]

        if len(action) == 2:
            self.game_state.move_piece(action)
        else:
            self.game_state.place_wall(action)
        return action

    def minimax_agent(self, player_one_minimax, is_alpha_beta):
        d = {}
        for child in self.game_state.get_all_child_states(player_one_minimax):
            if not is_alpha_beta:
                value = minimax(child[0], 3, maximizing_player=False, player_one_minimax=player_one_minimax)
            else:
                value = minimax_alpha_beta_pruning(child[0], 3, -math.inf, math.inf, maximizing_player=False,
                                                   player_one_minimax=player_one_minimax)
            d[value] = child
        return self.choose_action(d)

    def expectimax_agent(self, player_one_maximizer):
        d = {}
        for child in self.game_state.get_all_child_states(player_one_maximizer):
            value = expectimax(child[0], 2, False, player_one_maximizer)
            d[value] = child
        return self.choose_action(d)

    def player_one_user(self):
        while True:
            value = input("Enter move: ")
            if value == "x" or value == "X":
                exit(0)
            elif value.lower() == "help":
                print()
                self.print_commands()
                print()
            else:
                if value.upper().startswith("M"):
                    x_string, y_string = value[1:].split(",")
                    if x_string.upper() not in Mappings.INPUT_MAPPINGS.keys() or y_string.upper() not in Mappings.INPUT_MAPPINGS.keys():
                        Game.print_colored_output("Illegal move!", Color.RED)
                    else:
                        x_int = Mappings.INPUT_MAPPINGS[x_string.upper()]
                        y_int = Mappings.INPUT_MAPPINGS[y_string.upper()]
                        available_moves = self.game_state.get_available_moves(False)
                        move = (x_int, y_int)
                        if move not in available_moves:
                            Game.print_colored_output("Illegal move!", Color.RED)
                        else:
                            self.game_state.move_piece(move)
                            break

                elif value.upper().startswith("W"):
                    # place a wall
                    x_string, y_string = value[1:len(value) - 1].split(",")
                    if x_string.upper() not in Mappings.INPUT_MAPPINGS.keys() or y_string.upper() not in Mappings.INPUT_MAPPINGS.keys():
                        Game.print_colored_output("Illegal wall placement!", Color.RED)
                    else:
                        dir_string = value[-1]
                        if dir_string.upper() in ["N", "S", "E", "W"]:

                            if dir_string.upper() == "S":
                                direction = WallDirection.SOUTH
                            elif dir_string.upper() == "E":
                                direction = WallDirection.EAST
                            elif dir_string.upper() == "W":
                                direction = WallDirection.WEST
                            else:
                                direction = WallDirection.NORTH

                            x_int = Mappings.INPUT_MAPPINGS[x_string.upper()]
                            y_int = Mappings.INPUT_MAPPINGS[y_string.upper()]
                            is_placement_valid, coords = self.game_state.check_wall_placement((x_int, y_int),
                                                                                              direction)
                            if not is_placement_valid:
                                Game.print_colored_output("Illegal wall placement!", Color.RED)
                            else:
                                self.game_state.place_wall(coords)
                                break

                else:
                    Game.print_colored_output("Illegal command!", Color.RED)

    def player_simulation(self, player_number):
        if player_number == 1:
            index = 0
            maximizer = True
        else:
            index = 1
            maximizer = False
        t1 = time()
        print("Player {0:1} is thinking...\n".format(player_number))
        action = (0, 0)
        if self.player_simulation_algorithms[index] == "minimax":
            action = self.minimax_agent(maximizer, is_alpha_beta=False)
        elif self.player_simulation_algorithms[index] == "minimax-alpha-beta-pruning":
            action = self.minimax_agent(maximizer, is_alpha_beta=True)
        elif self.player_simulation_algorithms[index] == "expectimax":
            action = self.expectimax_agent(maximizer)
        elif self.player_simulation_algorithms[index] == "monte-carlo-tree-search":
            start = SearchNode(state=self.game_state, player_one_maximizer=maximizer)
            selected_node = start.best_action()
            action = selected_node.parent_action
            self.game_state.execute_action(action, False)

        if action is not None:
            if len(action) == 2:
                self.print_colored_output("Player {0:1} has moved his piece.".format(player_number), Color.CYAN)
            else:
                self.print_colored_output("Player {0:1} has placed a wall.".format(player_number), Color.CYAN)
            t2 = time()
            self.execution_times.append(t2 - t1)
            self.print_colored_output("It took him " + str(round(t2 - t1, 2)) + " seconds.", Color.CYAN)
            return True
        else:
            self.print_colored_output("Player {0:1} has no moves left.".format(player_number), Color.CYAN)
            return False

    def check_end_state(self):
        if self.game_state.is_end_state():
            winner = self.game_state.get_winner()
            if not self.game_state.is_simulation:
                if winner == "P1":
                    self.print_colored_output("You won!", Color.GREEN)
                else:
                    self.print_colored_output("You lost!", Color.RED)
            else:
                self.print_colored_output("The winner is " + winner + ".", Color.CYAN)
            return True
        else:
            return False

    def play(self):
        while True:
            print()
            self.game_state.print_game_stats()
            print("\n")
            self.game_state.print_board()
            print()

            if self.check_end_state():
                print("Execution average: ", sum(self.execution_times) / len(self.execution_times))
                break

            if self.game_state.player_one:
                if not self.game_state.is_simulation:
                    self.player_one_user()
                else:
                    res = self.player_simulation(1)
                    sleep(1.5)
                    if not res:
                        break
            else:
                res = self.player_simulation(2)
                if not res:
                    break

            self.game_state.player_one = not self.game_state.player_one

    @staticmethod
    def print_colored_output(text, color):
        print(color + text + Color.RESET)

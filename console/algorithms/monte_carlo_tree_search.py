from console.states.game_state import GameState
from collections import defaultdict
import numpy as np


class SearchNode:
    def __init__(self, state: GameState, parent=None, parent_action=None, player_one_maximizer=False):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1] = 0
        self._untried_actions = None
        self.player_one_maximizer = player_one_maximizer
        self._untried_actions = self.untried_actions()


    def untried_actions(self):
        self._untried_actions = self.state.get_all_child_states(player_one_maximizer=self.player_one_maximizer,
                                                                include_state=True)  # ovdje vidi za ovaj bool
        return self._untried_actions

    def q(self):
        wins = self.results[1]
        losses = self.results[-1]
        return wins - losses

    def n(self):
        return self.number_of_visits

    def expand(self):
        next_state, action = self._untried_actions.pop()
        child_node = SearchNode(next_state, parent=self, parent_action=action,
                                player_one_maximizer=self.player_one_maximizer)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_goal_state()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_goal_state():
            child_states = current_rollout_state.get_all_child_states(player_one_maximizer=self.player_one_maximizer,
                                                                      include_state=True)
            if len(child_states) == 0:
                return current_rollout_state.game_result(False)
            current_rollout_state = self.rollout_policy(child_states)[0]
        return current_rollout_state.game_result(False)

    def back_propagate(self, result):
        self.number_of_visits += 1
        self.results[result] += 1
        if self.parent:
            self.parent.back_propagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        if not self.player_one_maximizer:
            if self.state.player_two_wall_num != 0:
                simulation_no = 17
            else:
                simulation_no = 30
        else:
            if self.state.player_one_walls_num != 0:
                simulation_no = 17
            else:
                simulation_no = 30
        for i in range(simulation_no):
            v = self.tree_policy()
            reward = v.rollout()
            v.back_propagate(reward)
        return self.best_child(c_param=0.)

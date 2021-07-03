import math
from console.states.game_state import GameState
from console.heuristics.state_evaluation_heuristic import state_evaluation_heuristic


def minimax(game_state: GameState, depth, maximizing_player, player_one_minimax):
    if depth == 0:
        return state_evaluation_heuristic(game_state, player_one_minimax, False)
    if maximizing_player:
        max_eval = -math.inf
        for child in game_state.get_all_child_states(player_one_minimax):
            ev = minimax(child[0], depth - 1, False, player_one_minimax)
            max_eval = max(max_eval, ev)
        game_state.value = max_eval
        return max_eval
    else:
        min_eval = math.inf
        for child in game_state.get_all_child_states(player_one_minimax):
            ev = minimax(child[0], depth - 1, True, player_one_minimax)
            min_eval = min(min_eval, ev)
        game_state.value = min_eval
        return min_eval

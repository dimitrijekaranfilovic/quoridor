from console.states.game_state import GameState
import math
from console.heuristics.state_evaluation_heuristic import state_evaluation_heuristic


def minimax_alpha_beta_pruning(game_state: GameState, depth, alpha, beta, maximizing_player, player_one_minimax):
    if depth == 0:
        return state_evaluation_heuristic(game_state, player_one_minimax, False)
    if maximizing_player:
        max_eval = -math.inf
        for child in game_state.get_all_child_states(player_one_minimax):
            ev = minimax_alpha_beta_pruning(child[0], depth - 1, alpha, beta, False, player_one_minimax)
            max_eval = max(max_eval, ev)
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for child in game_state.get_all_child_states(player_one_minimax):
            ev = minimax_alpha_beta_pruning(child[0], depth - 1, alpha, beta, True, player_one_minimax)
            min_eval = min(min_eval, ev)
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval

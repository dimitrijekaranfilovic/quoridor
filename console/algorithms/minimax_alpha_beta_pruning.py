from console.states.game_state import GameState
import math


def minimax_alpha_beta_pruning(game_state: GameState, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_state.is_goal_state():
        # add real heuristic
        return game_state.player_one_walls_num + game_state.player_two_wall_num
    if maximizing_player:
        max_eval = -math.inf
        for child in game_state.get_all_child_states():
            ev = minimax_alpha_beta_pruning(child[0], depth - 1, alpha, beta, False)
            max_eval = max(max_eval, ev)
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        game_state.value = max_eval
        return max_eval
    else:
        min_eval = math.inf
        for child in game_state.get_all_child_states():
            ev = minimax_alpha_beta_pruning(child[0], depth - 1, alpha, beta, True)
            min_eval = min(min_eval, ev)
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval

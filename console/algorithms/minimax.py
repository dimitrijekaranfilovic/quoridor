import math
from console.states.game_state import GameState


def minimax(game_state: GameState, depth, maximizing_player):
    if depth == 0:
        # add real heuristic
        return 0
    if maximizing_player:
        max_eval = -math.inf
        for child in game_state.get_all_child_states():
            ev = minimax(child[0], depth - 1, False)
            max_eval = max(max_eval, ev)
        game_state.value = max_eval
        return max_eval
    else:
        min_eval = math.inf
        for child in game_state.get_all_child_states():
            ev = minimax(child[0], depth - 1, True)
            min_eval = min(min_eval, ev)
        game_state.value = min_eval
        return min_eval

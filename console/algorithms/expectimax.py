from console.heuristics.state_evaluation_heuristic import state_evaluation_heuristic
from console.states.game_state import GameState


def expectimax(game_state: GameState, depth, maximizing_player, player_one_maximizer):
    if depth == 0:
        return state_evaluation_heuristic(game_state, player_one_maximizer, True)
    if maximizing_player:
        return max([expectimax(child[0], False, depth - 1, player_one_maximizer) for child in
                    game_state.get_all_child_states(player_one_maximizer)])
    else:
        values = [expectimax(child[0], True, depth - 1, player_one_maximizer) for child in
                  game_state.get_all_child_states(player_one_maximizer)]
        return sum(values) / len(values)

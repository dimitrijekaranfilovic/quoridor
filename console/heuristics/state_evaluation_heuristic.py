from console.states.game_state import GameState
from console.search.astar import astar


def state_evaluation_heuristic(game_state: GameState, player_one_minimax):
    player_one_distance = game_state.player_one_pos[0]
    player_two_distance = 16 - game_state.player_two_pos[0]
    if player_one_minimax:
        player_path_len = astar(game_state, False)
        if player_path_len == 0 and game_state.player_one_pos[0] != 0:
            result = 0
        else:
            result = 1000 * player_two_distance - 100 * player_one_distance - 400 * player_path_len + (
                    game_state.player_one_walls_num - game_state.player_two_wall_num) * 100
            if game_state.player_one_pos[0] == 0:
                result += 5000
        return result
    else:
        player_path_len = astar(game_state, False)
        if player_path_len == 0 and game_state.player_two_pos[0] != 16:
            result = 0
        else:
            result = 1000 * player_one_distance - 300 * player_two_distance - 400 * player_path_len + (
                    game_state.player_two_wall_num - game_state.player_one_walls_num) * 100
            if game_state.player_two_pos[0] == 16:
                result += 5000
        return result

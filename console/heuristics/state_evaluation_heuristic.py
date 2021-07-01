from console.states.game_state import *
from console.search.astar import astar


def state_evaluation_heuristic(game_state: GameState, player_one_minimax):
    player_one_distance = game_state.player_one_pos[0]
    player_two_distance = 16 - game_state.player_two_pos[0]
    result = 0
    if player_one_minimax:
        # player_path_len = astar(game_state, False)
        # if player_path_len == 0 and game_state.player_one_pos[0] != 0:
        #     result = 0
        # else:
        #     result += 1000 * player_two_distance
        #     result -= 100 * player_one_distance
        #     result -= 400 * player_path_len
        #     result += (game_state.player_one_walls_num - game_state.player_two_wall_num) * 100
        #     if game_state.player_one_pos[0] == 0:
        #         result += 5000
        # return result
        opponent_path_len, player_path_len = 0, 0
        if game_state.player_one_walls_num != 10 and game_state.player_two_wall_num != 0:
            changed = False
            if not game_state.player_one:
                game_state.player_one = True
                changed = True
            player_path_len = astar(game_state, False)
            if changed:
                game_state.player_one = False
            opponent_path_len = astar(game_state, False)
        result += (player_two_distance + opponent_path_len - player_one_distance - player_path_len)
        if game_state.player_two_pos[0] == 16:
            result += 10000
        return result
    else:
        opponent_path_len, player_path_len = 0, 0
        if game_state.player_one_walls_num != 10 and game_state.player_two_wall_num != 0:
            changed = False
            if game_state.player_one:
                game_state.player_one = False
                changed = True
            player_path_len = astar(game_state, False)
            if changed:
                game_state.player_one = True
            opponent_path_len = astar(game_state, False)
        result += (player_one_distance + opponent_path_len - player_two_distance - player_path_len)
        if game_state.player_two_pos[0] == 16:
            result += 10000
        return result

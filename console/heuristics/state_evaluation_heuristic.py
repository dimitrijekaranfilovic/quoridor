from console.states.game_state import *
from console.search.astar import astar


def state_evaluation_heuristic(game_state: GameState, player_one_minimax):
    player_one_distance = game_state.player_one_pos[0] // 2
    player_two_distance = (16 - game_state.player_two_pos[0]) // 2
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
        # opponent_path_len, player_path_len = 0, 0
        # if game_state.player_one_walls_num != 10 and game_state.player_two_wall_num != 0:
        #     changed = False
        #     if not game_state.player_one:
        #         game_state.player_one = True
        #         changed = True
        #     player_path_len = astar(game_state, False)
        #     if changed:
        #         game_state.player_one = False
        #     opponent_path_len = astar(game_state, False)
        # result += (player_two_distance + opponent_path_len - player_one_distance - player_path_len)
        # if game_state.player_two_pos[0] == 16:
        #     result += 10000
        # return result

        opponent_path_len, player_path_len = player_two_distance, player_one_distance
        if game_state.player_one_walls_num != 10 and game_state.player_two_wall_num != 10:
            previous = game_state.player_one
            game_state.player_one = True
            player_path_len = astar(game_state, False)
            game_state.player_one = previous

        result += opponent_path_len
        result -= player_one_distance
        num = 100
        if player_path_len != 0:
            num = player_path_len
        result += round(100 / num, 2)

        # sto je manja distanca drugog igraca, to gore
        num_1 = 50
        if player_two_distance != 0:
            num_1 = player_two_distance
        result -= round(50 / num_1, 2)

        result += (game_state.player_one_walls_num - game_state.player_two_wall_num)  # mozda ovo promijeni
        if game_state.player_one_walls_num[0] == 0:
            result += 100
        if player_path_len == 0 and game_state.player_one_pos[0] != 0:
            result -= 500
        return result




    else:
        opponent_path_len, player_path_len = player_one_distance, player_two_distance
        if game_state.player_one_walls_num != 10 and game_state.player_two_wall_num != 10:
            previous = game_state.player_one
            game_state.player_one = False
            player_path_len = astar(game_state, False)
            game_state.player_one = previous

        result += opponent_path_len
        result -= player_two_distance
        num = 100
        if player_path_len != 0:
            num = player_path_len
        result += round(100 / num, 2)

        # sto je manja distanca prvog igraca, to gore
        # TODO: istestiraj za blokiranje
        num_1 = 50
        if player_one_distance != 0:
            num_1 = player_one_distance
        result -= round(50 / num_1, 2)

        result += (game_state.player_two_wall_num - game_state.player_one_walls_num)  # mozda ovo promijeni
        if game_state.player_two_pos[0] == 16:
            result += 100
        if player_path_len == 0 and game_state.player_two_pos[0] != 16:
            result -= 500
        return result

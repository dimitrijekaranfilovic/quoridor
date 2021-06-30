from console.states.game_state import GameState
from console.search.astar import astar
from console.search.astar_pathfinding import astar_pathfinding

from console.search.astar import astar


def state_evaluation_heuristic(game_state: GameState, player_one_minimax):
    # player_distance = game_state.distance_to_goal()
    # game_state.player_one = not game_state.player_one
    # opponent_distance = game_state.distance_to_goal()
    # game_state.player_one = not game_state.player_one
    # #if player_distance > 1:
    # part_1 = 1000 * player_distance
    # # else:
    # #     part_1 = 5000
    # return part_1 - 400 * opponent_distance
    player_one_distance = game_state.player_one_pos[0]
    player_two_distance = 16 - game_state.player_two_pos[0]
    if player_one_minimax:
        result = 1000 * player_two_distance - 100 * player_one_distance - 400 * astar(game_state, False)
        if game_state.player_one_pos[0] == 0:
            result += 2000
        # return 1000 * player_two_distance - 400 * player_one_distance
        return result
    else:
        result = 1000 * player_one_distance - 100 * player_two_distance - 400 * astar(game_state, False)
        if game_state.player_two_pos[0] == 16:
            result += 2000
        return result

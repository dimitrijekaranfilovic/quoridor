def simple_path_finding_heuristic(game_state):
    if game_state.is_player_one:
        return 1000 * abs(game_state.player_one_pos[0])
    else:
        return 1000 * abs(game_state.player_two_pos[0])

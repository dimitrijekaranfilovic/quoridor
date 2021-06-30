from copy import copy
from console.heuristics.simple_path_finding_heuristic import simple_path_finding_heuristic
from console.util.priority_queue_item import PriorityQueueItem
from queue import PriorityQueue


def astar_pathfinding(game_state, heuristic=simple_path_finding_heuristic):
    visited = set()

    def cost_function(path):
        actions = []
        current_cost = 0
        for state in path:
            current_cost += state[1][2]
        current_cost += len(actions)
        current_cost += heuristic(path[-1][0])
        return current_cost

    queue = PriorityQueue()
    if game_state.player_one:
        pos = game_state.player_one_pos
    else:
        pos = game_state.player_two_pos
    queue.put(PriorityQueueItem(0, [(game_state, ((pos[0], pos[1]), (0, 0), 0))]))

    while not queue.empty():
        item = queue.get()
        path = item.item
        current_state = path[-1][0]
        current_simplified_state = path[-1][1]
        if current_state.is_goal_state():
            final_path = []
            for state in path:
                final_path.append(state[1][1])
            return len(final_path[1:])
        if current_simplified_state not in visited:
            visited.add(current_simplified_state)
            for successor in current_state.get_child_states_with_moves():
                if successor[1] not in visited:
                    successor_path = copy(path)
                    successor_path.append(successor)
                    queue.put(PriorityQueueItem(cost_function(successor_path), successor_path))

    return 0

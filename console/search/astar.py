from copy import copy
from console.heuristics.simple_path_finding_heuristic import simple_path_finding_heuristic
from console.util.priority_queue_item import PriorityQueueItem
from queue import PriorityQueue


def astar(game_state, check_blockage, heuristic=simple_path_finding_heuristic):
    visited = set()

    # TODO: fix issue: encounters an infinite loop when can't find a path
    def cost_function(path):
        actions = []
        current_cost = 0
        for state in path:
            current_cost += state[2]
            # actions.append(state[1])
        current_cost += len(actions)
        current_cost += heuristic(path[-1][0])
        return current_cost

    queue = PriorityQueue()
    queue.put(PriorityQueueItem(0, [(game_state, (0, 0), 0)]))

    while not queue.empty():
        item = queue.get()
        path = item.item
        current_state = path[-1][0]
        if current_state.is_goal_state():
            if check_blockage:
                return True
            final_path = []
            for state in path:
                final_path.append(state[1])
            return final_path[1:]
        if current_state not in visited:
            visited.add(current_state)
            for successor in current_state.get_child_states_with_moves():
                if successor not in visited:
                    successor_path = copy(path)
                    successor_path.append(successor)
                    queue.put(PriorityQueueItem(cost_function(successor_path), successor_path))
    if check_blockage:
        return False

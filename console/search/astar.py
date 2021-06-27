from console.util.queue import PriorityQueueWithFunction
from copy import copy
import numpy as np
from console.heuristics.simple_path_finding_heuristic import simple_path_finding_heuristic


def astar(game_state, heuristic=simple_path_finding_heuristic):
    visited = []

    # TODO: fix issue: encounters an infinite loop when can't find a path
    def cost_function(path):
        actions = []
        current_cost = 0
        for state in path:
            current_cost += state[2]
            # actions.append(state[1])
        # current_cost += len(actions)
        # current_cost += heuristic(path[-1][0])
        return current_cost

    queue = PriorityQueueWithFunction(cost_function)
    queue.push([(game_state, (0, 0), 0)])
    while not queue.isEmpty():
        path = queue.pop()
        current_state = path[-1][0]
        if current_state.is_goal_state():
            final_path = []
            for state in path:
                final_path.append(state[1])
            return final_path[1:]
        if current_state not in set(visited):
            visited.append(current_state)
            for successor in current_state.get_child_states_with_moves():
                # print(successor)
                if successor not in set(visited):
                    successor_path = copy(path)
                    successor_path.append(successor)
                    queue.push(successor_path)
    return []

from torch import tensor
import torch


def eight_puzzle_heuristic(state, search_space):
    flattened_goal = tensor([1,2,3,4,5,6,7,8])
    flattened_state = state.flatten()
    mismatched_tiles = torch.ne(flattened_goal, flattened_state[:-1]) # ignore the blank tile
    return torch.sum(mismatched_tiles).item()
    # With a solution depth of 10, where BFS went through 102835 search nodes, A* went through 53.
    # At depth 13, BFS went through 758195 nodes. A* went through 1010. 

def food_heuristic(state, search_space):
    """potential heuristics:
    1. num remaining food pellets
    2. distance to closest pellet
    3. average distance to all remaining pellets
    4. distance to farthest pellet (better than sum of distance to all remaining pellets, which can overestimate)
    5. distance to closest pellet + Minimum Spanning Tree over remaininig pellets? --> would need to modify search space to actually store that MST
    """
    # 1. Num remaining food pellets
    # num_food = len(state[1]) # frozenset of remaining food positions
    # return num_food
    # 12385 nodes visited w/tricky maze,  food heuristic = num remaining food pellets

    pacman_pos = state[0]
    food_positions = state[1]
    if len(food_positions) == 0:
        return 0
    farthest_distance = 0
    for food_pos in food_positions:
        distance = abs(pacman_pos[0] - food_pos[0]) + abs(pacman_pos[1] - food_pos[1])  # Manhattan distance
        if distance > farthest_distance:
            farthest_distance = distance
    return farthest_distance

    # closest distance gets us 13869 nodes visited
    # avg distance gets us 11245 nodes visited
    # farthest distance gets us 9509 nodes visited
    # farthest distance + remaining food after that gets us 8389 nodes visited -- but not admissible
    



    return 0  # replace with a better heuristic!

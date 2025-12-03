from torch import tensor
import torch


def eight_puzzle_heuristic(state, search_space):
    flattened_goal = tensor([1,2,3,4,5,6,7,8])
    flattened_state = state.flatten()
    mismatched_tiles = torch.ne(flattened_goal, flattened_state[:-1]) # ignore the blank tile
    return torch.sum(mismatched_tiles).item()
    # With a solution depth of 10, where BFS went through 102835 search nodes, A* went through 53.
    # At depth 13, BFS went through 758195 nodes. A* went through 1010. 

def helperdist(search_space, a, b):
    # Try cache first
    if (a, b) in search_space.dist:
        return search_space.dist[(a, b)]
    if (b, a) in search_space.dist:
        return search_space.dist[(b, a)]
    
    # Compute and store for future use
    d = search_space.get_distance(a, b)
    search_space.dist[(a, b)] = d
    search_space.dist[(b, a)] = d
    return d

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
    
    #implementation of closest distance plus MST over remaining food
   
   
   # lots of nodes with this one...
def food_heuristic_mst(state, search_space):
    pacman_pos = state[0]
    food_positions = state[1]
    food_list = list(food_positions)
    
    if len(food_positions) == 0:
        return 0
    
    if len(food_positions) == 1:
        return helperdist(search_space, pacman_pos, food_list[0])
    
    #need to compute MST over food positions plus pacman position
    all_positions = [pacman_pos] + food_list
    return compute_mst(search_space, all_positions)

def compute_mst(search_space, positions):
    if len(positions) <= 1:
        return 0
    
    tree_cost = 0
    visited = set()
    visited.add(positions[0])
    unvisited = set()
    for pos in positions[1:]:
        unvisited.add(pos)
    
    while unvisited:
        best = float('inf')
        best_destination = None
        #goes through all nodes and finds best edge to add next to MST
        for v in visited:
            for u in unvisited:
                distance = helperdist(search_space, v, u)
                if distance < best:
                    best = distance
                    best_destination = u
        
        if best_destination is None: #to avoid errors
            break
        
        tree_cost += best
        visited.add(best_destination)
        unvisited.remove(best_destination)
    
    return tree_cost

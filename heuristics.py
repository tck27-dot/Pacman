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
    return 0  # replace with a better heuristic!

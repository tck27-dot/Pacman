from heuristics import eight_puzzle_heuristic
from search import SearchSpace, breadth_first_search, depth_first_search, a_star_search
import sys
from torch import tensor
import torch


class EightPuzzleSearchSpace(SearchSpace):

    def __init__(self, initial_board):
        self.board = initial_board

    def get_start_state(self):
        return self.board

    def is_final_state(self, state):
        return torch.equal(tensor([[1, 2, 3], [4, 5, 6], [7, 8, 0]]), state)

    """"Helper function: creates a new state by swapping the zero either vertically or horizontally."""
    def make_new_state(self, state, swap, direction, zeroLocation):
        newState = state.clone()
        if direction == 'vertical':
            newState[swap[1]][zeroLocation[1]] = state[swap[0]][zeroLocation[1]].item()
            newState[swap[0]][zeroLocation[1]] = state[swap[1]][zeroLocation[1]].item()

        if direction == 'horizontal':
            newState[zeroLocation[0]][swap[1]] = state[zeroLocation[0]][swap[0]].item()
            newState[zeroLocation[0]][swap[0]] = state[zeroLocation[0]][swap[1]].item()
            
        return newState
    
    def get_successors(self, state):
        successors = []

        # Locate the zero in the current state.
        for i in range(3):
            for j in range(3):
                if state[i][j].item() == 0:
                    row_zero = i
                    col_zero = j
        zeroLocation = (row_zero, col_zero)
        
        # Vertical swaps: up and/or down, depending on the row of the zero.
        if row_zero == 0:            
            successors.append((self.make_new_state(state,(0,1),'vertical',zeroLocation),"South",1))
        elif row_zero == 1:
            successors.append((self.make_new_state(state,(1,2),'vertical',zeroLocation),"South",1))
            successors.append((self.make_new_state(state,(1,0),'vertical',zeroLocation),"North",1))
        elif row_zero == 2:
            successors.append((self.make_new_state(state,(2,1),'vertical',zeroLocation),"North",1))

        # Horizontal swaps: left and/or right, depending on the column of the zero.
        if col_zero == 0:
            successors.append((self.make_new_state(state,(0,1),'horizontal',zeroLocation),"East",1))
        elif col_zero == 1:
            successors.append((self.make_new_state(state,(1,2),'horizontal',zeroLocation), "East", 1))
            successors.append((self.make_new_state(state,(1,0),'horizontal',zeroLocation), "West", 1))
        elif col_zero == 2:
            successors.append((self.make_new_state(state,(2,1),'horizontal',zeroLocation), "West", 1))
        
        return successors

example_eight_puzzles = [
    tensor([[1, 2, 3], [4, 5, 6], [7, 8, 0]]),
    tensor([[1, 2, 3], [4, 5, 0], [7, 8, 6]]),
    tensor([[1, 2, 3], [4, 0, 5], [7, 8, 6]]),
    tensor([[1, 0, 3], [4, 2, 5], [7, 8, 6]]),
    tensor([[0, 1, 3], [4, 2, 5], [7, 8, 6]]),
    tensor([[4, 1, 3], [0, 2, 5], [7, 8, 6]]),
    tensor([[4, 1, 3], [2, 0, 5], [7, 8, 6]]),
    tensor([[4, 1, 3], [2, 8, 5], [7, 0, 6]]),
    tensor([[4, 1, 3], [2, 8, 5], [7, 6, 0]]),
    tensor([[4, 1, 3], [2, 8, 0], [7, 6, 5]]),
    tensor([[4, 1, 0], [2, 8, 3], [7, 6, 5]]),
    tensor([[4, 0, 1], [2, 8, 3], [7, 6, 5]]),
    tensor([[0, 4, 1], [2, 8, 3], [7, 6, 5]]),
    tensor([[2, 4, 1], [0, 8, 3], [7, 6, 5]]),
]

# Running BFS at each solution depth results in an exponentially increasing number of search nodes visited
# and as such an exponentially increasing runtime. As discussed in class, at the later solution depths,
# each BFS call for a puzzle of depth n+1 will take more than twice as long as the call for depth n.

# We see some deviations from that rule in lower solution depths because it's possible to get lucky -- 
# i.e. to find the solution quickly, but that possibility decreases as the solution depth increases and
# the number of leaves increases. 
# It also might be the case that, sometimes, the branching factor is one, if a new state has only one 
# valid successor that is not its parent state.

# At depth 11, BFS took went through 102835 nodes and took 19 seconds.
# at depth 12, it took 252632 nodes and 67 seconds.
# At depth 13, it took 758195 nodes and 176 seconds.

# Using depth first search at even depth of 1 can go for essentially forever without finding a solution 
# because DFS can get stuck going down paths that do not lead to a solution, even though the search template 
# is designed to avoid cycles by tracking visited states.

# DFS also uses an absolute shitton of memory as the computer adds more and more states to the stack, so it
# eventually just crashes when the computer runs out of memory. 


if __name__ == "__main__":
    try:
        solution_depth = int(sys.argv[1])
        assert 0 <= solution_depth < len(example_eight_puzzles)
    except Exception:
        print(
            f"Usage: python eightpuzzle.py SOLUTION_DEPTH\n  where 0 <= SOLUTION_DEPTH <= {len(example_eight_puzzles)-1}"
        )
        exit()

    space = EightPuzzleSearchSpace(example_eight_puzzles[solution_depth])
    print("\nRunning breadth first search:")
    result = breadth_first_search(space)
    print(result)

    if len(sys.argv) > 2 and sys.argv[2] == "astar":
        print("\nRunning A* search with your current heuristic:")
        result = a_star_search(space, eight_puzzle_heuristic)
        print(result)

from heuristics import eight_puzzle_heuristic
from search import SearchSpace, breadth_first_search, depth_first_search, a_star_search
import sys
from torch import tensor
import torch


class EightPuzzleSearchSpace(SearchSpace):

    def __init__(self, initial_board):
        self.board = initial_board

    def get_start_state(self):
        raise NotImplementedError("Implement me!")

    def is_final_state(self, state):
        raise NotImplementedError("Implement me!")

    def get_successors(self, state):
        raise NotImplementedError("Implement me!")


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

import argparse
from zzz_pacman import readCommand, runGames

def main():
    parser = argparse.ArgumentParser(description="Pacman!")
    parser.add_argument(
        "--maze",
        type=str,
        required=True,
        help="Name of the maze layout, e.g. 'tiny', 'small', 'tricky', 'moderate', '270'",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        required=True,
        help="Search algorithm, i.e. 'bfs', 'dfs', 'ucs', or 'astar'",
    )
    args = parser.parse_args()
    mazes = {
        "tricky": "trickySearch",
        "270": "270Search",
        "moderate": "moderateSearch",
        "small": "smallSearch",
        "tiny": "tinySearch",
        "micro": "microSearch"
    }
    algorithms = {
        "bfs": "breadth_first_search",
        "dfs": "depth_first_search",
        "ucs": "uniform_cost_search",
        "astar": "a_star_search"
    }
    pacman_args = ["-l", mazes[args.maze], "-p", "SearchAgent", "-a", 
                   f"fn={algorithms[args.algorithm]},prob=FoodSearchProblem,heuristic=foodHeuristic"]
    runGames(**readCommand(pacman_args))

if __name__ == "__main__":
    main()

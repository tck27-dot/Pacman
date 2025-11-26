from search import SearchSpace
import torch
from torch import tensor 

""" We're describing each maze with a Python dictionary, tracking the maze's:
 - height (int)
 - width (int)
 - food (list of (x,y) positions)
 - walls (list of (x,y) positions)
 - pacman (x,y) position
 """

""" We're designing the state ourselves this time. What do we need to include in the state?
For sure: 
pacman position
remaining food positions 

height, width, and walls don't change. 

In the eight puzzle project the search space's only attribute was the initial board, but
the maze, the height, width, and walls will remain constant. We don't need to clutter up the state
by including them, so can store them within the search space object itself as the maze attribute.
"""
class PacmanFoodSearchSpace(SearchSpace):
    def __init__(self, dict_maze):
        """A Tensorless attempt to define the FoodSearchProblem search space. I only just realized that Sets are O(1) searches. Ah. Shit."""
        self.width = dict_maze['width']
        self.height = dict_maze['height']
        self.walls = set(dict_maze['walls'])
        self.food = frozenset(dict_maze['food']) # use frozenset so it can be included in the state tuple

        self.pac_food_state = (tuple(dict_maze['pacman']), self.food)
        # initial state is a tuple containing:
        # - pacman position as a tuple
        # - a frozenset of food positions


        """A previous attempt to do this with tensors --- saved for reference."""
        # self.maze = torch.zeros((self.width, self.height), dtype=torch.int32)
        # self.maze[tuple(zip(*dict_maze['walls']))] = 1  # set walls to 1
        # """
        # Copilot suggested this line as an alternative to a for-loop. I'm not sure how exactly this works, 
        # but as far as I can tell, it unpacks the list of (x,y) tuples into two ordered lists:
        #     one for x-values and 
        #     one for y-values. 
        # It then creates a 2-tuple of these two lists.
        # For Pytorch, a 2-tuple of lists indexes into the 2D tensor, selecting all the positions specified
        # by the (x,y) pairs and setting them to 1. 
        # """
        # # food_map = torch.zeros((dict_maze['width'], dict_maze['height']), dtype=torch.int32)
        # # food_map[tuple(zip(*dict_maze['food']))] = 2  # set food positions to 2

        # self.pac_food_state = (tensor([dict_maze['pacman'][0], dict_maze['pacman'][1]]), tuple(dict_maze['food']))  
        # """
        # The initial state is a tuple containing:
        # - [0] pacman position as a tensor
        # - [1] a list of (x,y) tuples representing the positions of remaining food.

    def get_start_state(self):
        return self.pac_food_state

    def is_final_state(self, state):
        if len(state[1]) == 0:      # if food positions list is empty --- no more food left
            return True
        return False

    def get_successors(self, state):
        """"
        Given a state (pacman position, food positions), return a list of successors. Each successor is a tuple of (new_state, direction, cost).
        Possible directions are "North", "South", "East", "West".
        Every action costs 1. 
        """
        directions_dict = {"North": (0,1), "South": (0,-1), "East": (1,0), "West": (-1,0)}
        successors = []

        for direction in directions_dict.keys():
            new_pacman = tuple([state[0][0] + directions_dict[direction][0],
                                        state[0][1] + directions_dict[direction][1]])
            
            # Bounds check
            if (0 <= new_pacman[0] < self.width) and (0 <= new_pacman[1] < self.height):
                # Wall check
                if new_pacman not in self.walls:
                    # Food check
                    if new_pacman in state[1]:  # if new position is a food position
                        new_food_positions = set(state[1])  # make a set copy of the food positions frozenset
                        new_food_positions.remove(new_pacman)  # remove eaten food
                        new_state = (new_pacman, frozenset(new_food_positions))  # update food positions
                    else:
                        new_state = (new_pacman, state[1])  # food map remains the same
                    successors.append((new_state, direction, 1))  # cost is always 1


            # new_pacman_pos = (new_pacman_tens[0].item(), new_pacman_tens[1].item())  # unpack tensor into a tuple

    
            # # Check if new position is within bounds and not a wall
            # if new_pacman_pos[0] >= 0 and new_pacman_pos[0] < self.width:
            #     if new_pacman_pos[1] >= 0 and new_pacman_pos[1] < self.height:
            #         if self.maze[new_pacman_pos] != 1: # if new position is not a wall 
            #             if new_pacman_pos in state[1]: # if new position is a food position
            #                 new_food_positions = list(state[1])  # make a list copy of the food positions tuple
            #                 new_food_positions.remove(new_pacman_pos)  # remove eaten food
            #                 new_state = (new_pacman_tens, tuple(new_food_positions))  # update food positions
            #             else:
            #                 new_state = (new_pacman_tens, state[1])  # food map remains the same
            #             successors.append((new_state, directions[i], 1))  # cost is always 1

        return successors
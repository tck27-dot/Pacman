from search import SearchSpace

class PacmanFoodSearchSpace(SearchSpace):
    def __init__(self, state):
        raise NotImplementedError('Implement me!')

    def get_start_state(self):
        raise NotImplementedError('Implement me!')

    def is_final_state(self, state):
        raise NotImplementedError('Implement me!')

    def get_successors(self, state):
        raise NotImplementedError('Implement me!')
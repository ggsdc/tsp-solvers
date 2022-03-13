"""

"""

import copy

from .base import BaseSolver


class Christofides(BaseSolver):
    # Only works on symmetric and completed graphs
    def __init__(self, graph, verbose=0):
        super().__init__()
        self.graph = graph
        self.verbose = verbose
        self.solution = None
        self.MST = None  # T
        self.odd_vertices = None  # O
        self.MWPM = None  # M

    def run(self):
        # Calculate minimum spanning tree (MST)
        # Subset O vertices of odd degree and calculate full graph
        # TODO: Construct minim weight perfect matching M
        # TODO: Unite graphs
        # TODO: Calculate Euler tour
        # TODO: Fix euler tour
        self._get_minimum_spanning_tree()
        self._get_odd_graph()
        self._get_minimum_weight_perfect_matching()
        pass

    def _get_minimum_spanning_tree(self):
        self.MST = copy.deepcopy(self.graph)
        self.MST.create_minimum_spanning_tree()

    def _get_odd_graph(self):
        self.odd_vertices = copy.deepcopy(self.MST)
        self.odd_vertices.create_full_odd_graph()
        self.odd_vertices.plot_edges()

    def _get_minimum_weight_perfect_matching(self):
        self.MWPM = copy.deepcopy(self.odd_vertices)
        self.MWPM.create_minimum_weight_perfect_matching()

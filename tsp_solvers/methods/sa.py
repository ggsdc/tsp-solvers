import sys

from ..initializers import RandomInitializer, NearestNeighbor


class SimulatedAnnealing:
    def __init__(self, graph, t_max, t_min, max_time, init="random", plot=False):
        assert t_max > t_min > 0, "t_max > t_min > 0"

        self.graph = graph
        self.t_max = t_max
        self.t_min = t_min
        self.t = self.t_max
        self.max_time = max_time
        self.init = init
        self.initializer = None
        self.plot = plot
        if self.plot:
            if "matplotlib" not in sys.modules:
                raise ModuleNotFoundError(
                    "Matplotlib has to be installed to be able to plot!"
                )

        if self.init == "random":
            self.initializer = RandomInitializer(self.graph, 1)
        elif self.init == "nearest":
            self.initializer = NearestNeighbor(self.graph, 1)

        self.solution = self.initializer.get_init()[0]
        self.cost = self.graph.get_solution_cost(self.solution)

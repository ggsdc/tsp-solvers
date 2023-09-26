"""
This file contains the main logic for the two opt heuristic
"""

# Import from libraries
import copy
import datetime
import sys

# Import from internal modules
from tsp_solvers.initializers import NearestNeighbor, RandomInitializer
from tsp_solvers.methods.base import BaseSolver


class TwoOpt(BaseSolver):
    def __init__(self, graph, max_time, init="random", plot=False):
        super().__init__()
        self.graph = graph
        self.max_time = max_time
        self.init = init
        self.plot = plot
        if self.plot:
            if "matplotlib" not in sys.modules:
                raise ModuleNotFoundError(
                    "Matplotlib has to be installed to be able to plot!"
                )

        self.initializer = None
        self.cost = float("Inf")
        self.count = 0
        if self.init == "random":
            self.initializer = RandomInitializer(self.graph)
        elif self.init == "nearest":
            self.initializer = NearestNeighbor(self.graph)

        self.solution = self.initializer.get_init()[0]
        self.cost = self.graph.get_cost(self.solution)

    def get_best(self):
        print("\nTwo opt:")
        print(
            f"Best solution: {self.cost} \t|\t Swaps: {self.count} \t|\t Time: {self.time}"
        )

    def run(self):
        initial_time = datetime.datetime.utcnow()
        count = 0
        while (datetime.datetime.utcnow() - initial_time).seconds <= self.max_time:
            delta = 0
            for a, b in self.all_segments(len(self.solution)):
                delta += self.reverse_if_better(a, b)
            break
        self.time = datetime.datetime.utcnow() - initial_time
        self.cost = self.graph.get_cost(self.solution)

    def save(self, file):
        text = (
            "Two-Opt. Best solution: "
            + str(self.solution)
            + "\t|\tCost: "
            + str(self.cost)
            + "\t|\tSwaps: "
            + str(self.count)
            + "\n"
        )
        with open(file, "a") as myfile:
            myfile.write(text)

    def reverse_if_better(self, i, j):
        a, b, c, d = (
            self.solution[i - 1],
            self.solution[i],
            self.solution[j - 1],
            self.solution[j % len(self.solution)],
        )
        d0 = self.graph.calculate_cost(a, b) + self.graph.calculate_cost(c, d)

        d1 = self.graph.calculate_cost(a, c) + self.graph.calculate_cost(b, d)

        if d0 > d1:
            self.solution[i:j] = reversed(self.solution[i:j])
            self.count += 1
            if self.plot:
                filename = (
                    f"plots/two_opt_{self.graph.number_vertices}_{self.count}.png"
                )
                self.cost = self.graph.get_cost(self.solution)
                title = "Two opt " + "\n Solution cost: " + str(round(self.cost, 2))
                self.graph.plot_solution(
                    self.solution, pheromones=False, filename=filename, title=title
                )

            return -d0 + d1
        return 0

    @staticmethod
    def all_segments(n: int):
        return ((i, j) for i in range(n) for j in range(i + 2, n))

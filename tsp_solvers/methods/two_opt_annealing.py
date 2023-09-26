"""
This file contains the main logic for the two opt heuristic
"""

# Import from libraries
import copy
from datetime import datetime
import sys
from random import random

# Import from internal modules
from tsp_solvers.initializers import NearestNeighbor, RandomInitializer
from tsp_solvers.methods.base import BaseSolver


class SimulatedAnnealingTwoOpt(BaseSolver):
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
        self.good_count = 0
        self.bad_count = 0
        if self.init == "random":
            self.initializer = RandomInitializer(self.graph)
        elif self.init == "nearest":
            self.initializer = NearestNeighbor(self.graph)

        self.solution = self.initializer.get_init()[0]
        self.cost = self.graph.get_cost(self.solution)
        self.temperature = 1

    def get_best(self):
        print("\nSimulated annealing two opt:")
        print(
            f"Best solution: {self.cost} \t|\t Good swaps: {self.good_count} "
            f"\t|\t Bad swaps: {self.bad_count} \t|\t Time: {self.time}"
        )
        print(f"{self.solution}")

    def run(self):
        initial_time = datetime.utcnow()

        while (
            datetime.utcnow() - initial_time
        ).seconds <= self.max_time and self.temperature >= 0:
            delta = 0

            for a, b in self.all_segments(len(self.solution)):
                delta += self.reverse_if_better(a, b)

            self.temperature -= 0.33

        self.time = datetime.utcnow() - initial_time
        self.cost = self.graph.get_cost(self.solution)

    def save(self, file):
        text = (
            "Two-Opt. Best solution: "
            + str(self.solution)
            + "\t|\tCost: "
            + str(self.cost)
            + "\t|\tSwaps: "
            + str(self.good_count)
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

        rnd = random() <= self.temperature

        if d0 > d1 or (rnd and d0 * (1 + self.temperature) > d1):
            self.solution[i:j] = reversed(self.solution[i:j])
            if d0 > d1:
                self.good_count += 1
            else:
                self.bad_count += 1

            if self.plot:
                filename = f"plots/sa_two_opt_{self.graph.number_vertices}_{self.good_count + self.bad_count}.png"
                self.cost = self.graph.get_cost(self.solution)
                title = "SA Two opt " + "\n Solution cost: " + str(round(self.cost, 2))
                self.graph.plot_solution(
                    self.solution, pheromones=False, filename=filename, title=title
                )

            return -d0 + d1
        return 0

    @staticmethod
    def all_segments(n: int):
        return ((i, j) for i in range(n) for j in range(i + 2, n))

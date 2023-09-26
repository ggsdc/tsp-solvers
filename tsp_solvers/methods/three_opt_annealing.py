import sys
from datetime import datetime
from random import random

from tsp_solvers.initializers import NearestNeighbor, RandomInitializer
from tsp_solvers.methods.base import BaseSolver


class SimulatedAnnealingThreeOpt(BaseSolver):
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
        print("\nSimulated annealing three opt:")
        print(
            f"Best solution: {self.cost} \t|\t Good swaps: {self.good_count} "
            f"\t|\t Bad swaps: {self.bad_count} \t|\t Time: {self.time}"
        )

    def run(self):
        initial_time = datetime.utcnow()
        while (
            datetime.utcnow() - initial_time
        ).seconds <= self.max_time and self.temperature >= 0:
            delta = 0
            for a, b, c in self.all_segments(len(self.solution)):
                delta += self.reverse_if_better(a, b, c)

            self.temperature -= 0.1

        self.time = datetime.utcnow() - initial_time
        self.cost = self.graph.get_cost(self.solution)
        if self.plot:
            filename = f"plots/sa_three_opt_{self.graph.number_vertices}_{self.good_count + self.bad_count}.png"
            self.cost = self.graph.get_cost(self.solution)
            title = "SA Three opt " + "\n Solution cost: " + str(round(self.cost, 2))
            self.graph.plot_solution(
                self.solution, pheromones=False, filename=filename, title=title
            )

    def reverse_if_better(self, i, j, k):
        a, b, c, d, e, f = (
            self.solution[i - 1],
            self.solution[i],
            self.solution[j - 1],
            self.solution[j],
            self.solution[k - 1],
            self.solution[k % len(self.solution)],
        )

        d0 = (
            self.graph.calculate_cost(a, b)
            + self.graph.calculate_cost(c, d)
            + self.graph.calculate_cost(e, f)
        )

        d1 = (
            self.graph.calculate_cost(a, c)
            + self.graph.calculate_cost(b, d)
            + self.graph.calculate_cost(e, f)
        )

        d2 = (
            self.graph.calculate_cost(a, b)
            + self.graph.calculate_cost(c, e)
            + self.graph.calculate_cost(d, f)
        )

        d3 = (
            self.graph.calculate_cost(a, d)
            + self.graph.calculate_cost(e, b)
            + self.graph.calculate_cost(c, f)
        )

        d4 = (
            self.graph.calculate_cost(f, b)
            + self.graph.calculate_cost(c, d)
            + self.graph.calculate_cost(e, a)
        )

        rnd = random() <= self.temperature

        if d0 > d1 or (rnd and d0 * (1 + self.temperature) > d1):
            self.solution[i:j] = reversed(self.solution[i:j])

            if d0 > d1:
                self.good_count += 1
            else:
                self.bad_count += 1

            self.plot_solution()

            return -d0 + d1
        elif d0 > d2 or (rnd and d0 * (1 + self.temperature) > d2):
            self.solution[j:k] = reversed(self.solution[j:k])

            if d0 > d2:
                self.good_count += 1
            else:
                self.bad_count += 1

            self.plot_solution()

            return -d0 + d2
        elif d0 > d4 or (rnd and d0 * (1 + self.temperature) > d4):
            self.solution[i:k] = reversed(self.solution[i:k])

            if d0 > d4:
                self.good_count += 1
            else:
                self.bad_count += 1

            self.plot_solution()

            return -d0 + d4
        elif d0 > d3 or (rnd and d0 * (1 + self.temperature) > d3):
            tmp = self.solution[j:k] + self.solution[i:j]
            self.solution[i:k] = tmp

            if d0 > d3:
                self.good_count += 1
            else:
                self.bad_count += 1

            self.plot_solution()

            return -d0 + d3
        return 0

    @staticmethod
    def all_segments(n: int):
        return (
            (i, j, k)
            for i in range(n)
            for j in range(i + 2, n)
            for k in range(j + 2, n + (i > 0))
        )

    def plot_solution(self):
        if self.plot and (self.good_count + self.bad_count) % 50 == 0:
            filename = f"plots/sa_three_opt_{self.graph.number_vertices}_{self.good_count + self.bad_count}.png"
            self.cost = self.graph.get_cost(self.solution)
            title = "SA Three opt " + "\n Solution cost: " + str(round(self.cost, 2))
            self.graph.plot_solution(
                self.solution, pheromones=False, filename=filename, title=title
            )

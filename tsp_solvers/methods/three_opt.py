import sys
from datetime import datetime

from tsp_solvers.initializers import NearestNeighbor, RandomInitializer
from tsp_solvers.methods.base import BaseMethod


class ThreeOpt(BaseMethod):
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
        print("\nThree opt:")
        print(
            f"Best solution: {self.cost} \t|\t Swaps: {self.count} \t|\t Time: {self.time}"
        )

    def run(self):
        initial_time = datetime.utcnow()
        while (datetime.utcnow() - initial_time).seconds <= self.max_time:
            delta = 0
            for a, b, c in self.all_segments(len(self.solution)):
                delta += self.reverse_if_better(a, b, c)

            break

        self.time = datetime.utcnow() - initial_time
        self.cost = self.graph.get_cost(self.solution)

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

        if d0 > d1:
            self.solution[i:j] = reversed(self.solution[i:j])
            self.count += 1
            self.plot_solution()
            return -d0 + d1

        elif d0 > d2:
            self.solution[j:k] = reversed(self.solution[j:k])
            self.count += 1
            self.plot_solution()
            return -d0 + d2

        elif d0 > d4:
            self.solution[i:k] = reversed(self.solution[i:k])
            self.count += 1
            self.plot_solution()
            return -d0 + d4

        elif d0 > d3:
            tmp = self.solution[j:k] + self.solution[i:j]
            self.solution[i:k] = tmp
            self.count += 1
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
        if self.plot:
            filename = f"plots/three_opt_{self.graph.number_vertices}_{self.count}.png"
            self.cost = self.graph.get_cost(self.solution)
            title = "Three opt " + "\n Solution cost: " + str(round(self.cost, 2))
            self.graph.plot_solution(
                self.solution, pheromones=False, filename=filename, title=title
            )

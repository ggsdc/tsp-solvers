"""
This file contains the main logic for the two opt heuristic
"""

# Import from libraries
import datetime
import sys

# Import from internal modules
from ..initializers import NearestNeighbor, RandomInitializer
from .base import BaseSolver


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
            self.initializer = RandomInitializer(self.graph, 1)
        elif self.init == "nearest":
            self.initializer = NearestNeighbor(self.graph, 1)

        self.solution = self.initializer.get_init()[0]
        self.cost = self.graph.get_solution_cost(self.solution)

    def get_best(self):
        print("\nTwo opt:")
        print(
            "Best solution: ",
            str(self.solution),
            "\t|\tCost: ",
            str(round(self.cost, 2)),
            "\t|\t Swaps: ",
            str(self.count),
        )

    def run(self):
        initial_time = datetime.datetime.utcnow()
        while (datetime.datetime.utcnow() - initial_time).seconds <= self.max_time:
            swap = False
            start = 0
            end = len(self.solution) + 1

            for i in range(len(self.solution) - 1):
                for j in range(i + 2, len(self.solution) + 1):
                    if j - i > len(self.solution) - 2:
                        continue

                    if i == start:
                        part_1 = self.solution[start:j]
                        part_2 = self.solution[j:end]
                        part_2.reverse()
                        aux_solution = part_1 + part_2

                    elif j == end - 1:
                        part_1 = self.solution[start:i]
                        part_2 = self.solution[i:end]
                        part_2.reverse()
                        aux_solution = part_1 + part_2

                    else:
                        part_1 = self.solution[start:i]
                        part_2 = self.solution[i:j]
                        part_2.reverse()
                        part_3 = self.solution[j:end]
                        aux_solution = part_1 + part_2 + part_3

                    aux_cost = self.graph.get_solution_cost(aux_solution)

                    if self.cost > aux_cost:
                        self.solution = aux_solution
                        self.cost = aux_cost
                        swap = True
                        self.count += 1
                        break

                if swap:
                    break

            if not swap:
                break

        self.time = datetime.datetime.utcnow() - initial_time

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

"""
This file contains the main logic for the Ant Colony Optimization method
"""
# TODO: study to implement part of the logic on C or C++ to speed up

# Import from libraries
import datetime
import math
import random
import sys
from itertools import accumulate

# Import from internal modules
from .base import BaseSolver


class Ant:
    """
    The class for the individual ants
    """

    def __init__(self, alpha=0, beta=0, graph=None):
        """ """
        self.alpha = alpha
        self.beta = beta
        self.number_vertices = graph.number_vertices
        self.graph = graph
        self.solution = list()
        self.cost = 0
        self.unvisited_nodes = list(self.graph.vertices)

    def _select_node(self):
        """ """

        pheromone = [
            self.graph.edges_collection[
                (self.solution[-1].idx, unvisited.idx)
            ].pheromone
            for unvisited in self.unvisited_nodes
        ]

        # pheromone = []
        # for unvisited in self.unvisited_nodes:
        #     aux = self.graph.edges_collection[
        #         (self.solution[-1].idx, unvisited.idx)
        #     ].pheromone
        #     pheromone.append(aux)

        pheromone = list(map(lambda x: math.pow(x, self.alpha), pheromone))

        visibility = [
            self.graph.edges_collection[(self.solution[-1].idx, unvisited.idx)].cost
            for unvisited in self.unvisited_nodes
        ]

        visibility = list(map(lambda x: math.pow(1 / x, self.beta), visibility))

        denominator = sum([x * y for x, y in zip(pheromone, visibility)])
        cumulative_probability = list(
            accumulate([p * v / denominator for p, v in zip(pheromone, visibility)])
        )

        random_value = random.uniform(0, 1)

        added_idx = next(
            idx
            for idx, value in enumerate(cumulative_probability)
            if value >= random_value
        )

        added = self.unvisited_nodes[added_idx]
        self.unvisited_nodes.remove(added)
        return added

    def find_solution(self):
        """ """
        self.solution = random.sample(self.graph.vertices, 1)
        self.unvisited_nodes = list(self.graph.vertices)
        self.unvisited_nodes.remove(self.solution[0])
        while len(self.solution) < self.number_vertices:
            self.solution.append(self._select_node())
        return self.solution

    def get_cost(self):
        self.cost = self.graph.get_solution_cost(self.solution)
        return self.cost


class AntColonyOptimization(BaseSolver):
    def __init__(
        self,
        mode="AS",
        graph=None,
        iterations=100,
        population_size=10,
        alpha=1,
        beta=3,
        rho=0.1,
        pheromone_deposit=1,
        initial_pheromone=1,
        max_time=60,
        plot=False,
    ):
        super().__init__()
        self.mode = mode
        self.graph = graph
        self.iterations = iterations
        self.current_iteration = 0
        self.population_size = population_size
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.pheromone_deposit = pheromone_deposit
        self.initial_pheromone = initial_pheromone
        self.number_vertices = self.graph.number_vertices
        self.max_time = max_time
        self.plot = plot
        if self.plot:
            if "matplotlib" not in sys.modules:
                raise ModuleNotFoundError(
                    "Matplotlib has to be installed to be able to plot!"
                )

        self.time = None

        for edge in self.graph.edges_collection:
            self.graph.update_pheromone(edge, initial_pheromone)

        self.ants = [Ant(alpha, beta, self.graph) for _ in range(self.population_size)]

        self.best_solution = None
        self.best_cost = float("inf")

    def _add_pheromone(self, solution, cost, weight=1):
        pheromone_to_add = self.pheromone_deposit / cost
        for i in range(self.number_vertices):
            self.graph.edges_collection[
                (solution[i].idx, solution[(i + 1) % self.number_vertices].idx)
            ].pheromone = (
                self.graph.edges_collection[
                    (solution[i].idx, solution[(i + 1) % self.number_vertices].idx)
                ].pheromone
                + weight * pheromone_to_add
            )

    def get_best(self):
        best = self.ants[0]
        for ant in self.ants:
            if ant.cost < best.cost:
                best = ant
        print("\nACO:")
        print("Best solution: ", str(best.solution), "\t|\tcost: ", str(best.cost))

    def evaluate(self):
        costs = [i.cost for i in self.ants]
        mean_cost = sum(costs) / len(costs)
        min_cost = min(costs)

        if min_cost * 1.01 > mean_cost:
            print("BREAK")
            return True
        else:
            return False

    def _as(self):
        frac = 0.1
        initial_time = datetime.datetime.utcnow()
        for i in range(self.iterations):
            self.current_iteration = i
            if i / self.iterations >= frac:
                print("Iteration ", str(i), " of ", str(self.iterations))
                frac += 0.1

            if i != 0:
                for edge in self.graph.edges_collection:
                    self.graph.edges_collection[
                        edge
                    ].pheromone = self.graph.edges_collection[edge].pheromone * (
                        1 - self.rho
                    )

            for ant in self.ants:
                self._add_pheromone(ant.find_solution(), ant.get_cost(), 2)
                if ant.cost < self.best_cost:
                    self.best_solution = ant.solution
                    self.best_cost = ant.cost

            if i >= self.iterations // 5:
                if self.evaluate():
                    break

            if self.plot:
                self.plot_advancement()

            if (datetime.datetime.utcnow() - initial_time).seconds > self.max_time:
                break

    def run(self):
        start = datetime.datetime.utcnow()
        if self.mode == "AS":
            self._as()
        else:
            pass
        self.time = datetime.datetime.utcnow() - start

    def show(self):
        print("\nSOLUTION:")
        print(
            "Ants: "
            + str(self.population_size)
            + ". Iterations: "
            + str(self.iterations)
            + "\n"
        )
        for ant in self.ants:
            print("Best solution: %s\t|\t cost: %d" % (str(ant.solution), ant.cost))

    def save(self, file):
        best = self.ants[0]
        for ant in self.ants:
            if ant.cost < best.cost:
                best = ant
        text = (
            "ACO. Best solution: "
            + str(best.solution)
            + "\t|\tCost: "
            + str(best.cost)
            + "\n"
        )
        with open(file, "a") as f:
            f.write(text)

    def plot_advancement(self):
        plot = [10 * x for x in range(1, self.iterations // 10 + 1)]
        if (self.current_iteration + 1) in plot:
            filename = (
                "plots/aco_"
                + str(self.graph.number_vertices)
                + "_"
                + str(self.current_iteration + 1)
                + ".png"
            )
            title = (
                "Ant Colony Optimization. Iteration "
                + str(self.current_iteration + 1)
                + "\n Solution cost: "
                + str(round(self.best_cost, 2))
            )
            self.graph.plot_solution(
                self.best_solution,
                pheromones=True,
                filename=filename,
                title=title,
            )

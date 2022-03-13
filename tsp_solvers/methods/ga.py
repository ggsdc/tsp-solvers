"""
This file contains the main logic of the Genetic Algorithm method
"""
# TODO: study to implement part of the logic on C or C++ to speed up
# TODO: review convergence on algorithm as it always exists at 20% even with random initialization.

# Import from libraries
import datetime
import random
import sys

# Import from internal modules
from ..initializers import NearestNeighbor, RandomInitializer
from .base import BaseSolver


class Individual:
    """
    The genes are the solution (path)
    """

    def __init__(self, genes=None, cost=0, idx=0):
        if genes is None:
            genes = list()
        self.genes = genes
        self.cost = cost
        self.number_vertices = len(genes)
        self.idx = idx
        self._hash = self.__hash__()

    # TODO: change to property and setter methods
    def set_genes(self, genes):
        self.genes = list(genes)
        self.number_vertices = len(genes)

    def set_cost(self, cost):
        self.cost = cost

    def set_idx(self, idx):
        self.idx = idx

    def random_sub_solution(self):
        """"""
        start = random.randrange(0, self.number_vertices)
        end = start
        while (
            end == start
            or abs(end - start) == 1
            or abs(end - start) == len(self.genes) - 1
        ):
            end = random.randrange(0, self.number_vertices)
        if start > end:
            start, end = end, start
        return self.genes[start:end]

    def remove_vertices(self, sub_solution):
        """"""
        subset = set(sub_solution)
        self.genes = [gene for gene in self.genes if gene not in subset]

    def insert_sub_solution(self, sub_solution, x):
        """"""
        if x != -1:
            self.genes = self.genes[: x + 1] + sub_solution + self.genes[x + 1 :]
        else:
            self.genes = self.genes + sub_solution

    def mutate(self):
        """"""
        i = random.randrange(0, self.number_vertices)
        j = random.randrange(0, self.number_vertices)
        while i == j:
            j = random.randrange(0, self.number_vertices)

        aux = self.genes[i]
        self.genes[i] = self.genes[j]
        self.genes[j] = aux

    def __str__(self):
        return str(self.genes)


class GeneticAlgorithm(BaseSolver):
    def __init__(
        self,
        graph,
        max_generations,
        population_size,
        mutation_probability,
        max_time,
        init="random",
        plot=False,
        verbose=False,
    ):
        """ """
        super().__init__()
        self.individuals = list()
        self.graph = graph
        self.max_generations = max_generations
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.mating_pool = []
        self.children = []
        self.id = 1
        self.max_time = max_time
        self.time = None
        self.verbose = verbose

        self.best_genes = None
        self.best_cost = float("inf")
        self.plot = plot
        if self.plot:
            if "matplotlib" not in sys.modules:
                raise ModuleNotFoundError(
                    "Matplotlib has to be installed to be able to plot!"
                )
        self.init = init
        self.initializer = None
        if self.init == "random":
            self.initializer = RandomInitializer(self.graph, self.population_size)
        elif self.init == "nearest":
            self.initializer = NearestNeighbor(self.graph, self.population_size)

        solutions = self.initializer.get_init()

        self.individuals = [
            Individual(
                genes=solution,
                cost=self.graph.get_solution_cost(solution),
                idx=counter + self.id,
            )
            for counter, solution in enumerate(solutions)
        ]
        self.id += len(solutions)

    def get_best(self):
        """"""
        best = self.individuals[0]
        for individual in self.individuals:
            if individual.cost < best.cost:
                best = individual
        print("\nGA:")
        print("Best solution: ", str(best.genes), "\t|\tcost: ", str(best.cost))

    def _update_best(self):
        """"""
        for individual in self.individuals:
            if individual.cost < self.best_cost:
                self.best_genes = individual.genes
                self.best_cost = individual.cost

    def _best_insertion(self, child, sub_solution):
        """"""
        start = sub_solution[0]
        end = sub_solution[-1]
        best_payoff = float("-inf")
        j = 0
        for i in range(0, len(child.genes) - 1):
            payoff = (
                self.graph.edges_collection[
                    (child.genes[i].idx, child.genes[i + 1].idx)
                ].cost
                - self.graph.edges_collection[(child.genes[i].idx, start.idx)].cost
                - self.graph.edges_collection[(end.idx, child.genes[i + 1].idx)].cost
            )

            if payoff > best_payoff:
                best_payoff = payoff
                j = i

        payoff = (
            self.graph.edges_collection[(child.genes[-1].idx, child.genes[0].idx)].cost
            - self.graph.edges_collection[(child.genes[-1].idx, start.idx)].cost
            - self.graph.edges_collection[(end.idx, child.genes[0].idx)].cost
        )

        if payoff > best_payoff:
            best_payoff = payoff
            j = -1

        return j

    def _cross_over(self):
        """"""
        self.children = []
        for n in range(0, self.population_size // 2):
            ind1 = random.choice(self.mating_pool)
            ind2 = random.choice(self.mating_pool)

            child = Individual()
            child.set_genes(ind1.genes)
            child.set_cost(ind1.cost)
            child.set_idx(self.id)
            self.id += 1
            sub_solution = ind2.random_sub_solution()

            child.remove_vertices(sub_solution)

            n = self._best_insertion(child, sub_solution)
            child.insert_sub_solution(sub_solution, n)
            child.cost = self.graph.get_solution_cost(child.genes)
            self.children.append(child)

    def _selection(self):
        """"""
        self.mating_pool = []
        iterator_list = list(self.individuals)
        while len(self.mating_pool) < self.population_size // 2:
            selected = min(iterator_list, key=lambda i: i.cost)
            iterator_list.remove(selected)
            self.mating_pool.append(selected)

    def _mutation(self):
        """"""
        for i in range(len(self.children)):
            prob = random.uniform(0, 1)
            if prob < self.mutation_probability:
                self.children[i].mutate()
                self.children[i].cost = self.graph.get_solution_cost(
                    self.children[i].genes
                )

    def _substitution(self):
        """"""
        new_population = []
        iterator_list = self.individuals + self.children

        while len(new_population) < self.population_size:
            selected = min(iterator_list, key=lambda i: i.cost)
            iterator_list.remove(selected)
            new_population.append(selected)

        self.individuals = new_population

    def _evaluate(self):
        """"""
        # TODO: review logic behind as this diversity is not working as intended and it stops prematurely with
        #  worse solutions than when this evaluation is not performed
        costs = [i.cost for i in self.individuals]
        mean_cost = sum(costs) / len(costs)
        min_cost = min(costs)
        if min_cost * 1.01 > mean_cost:
            if self.verbose:
                print("BREAK")
            return True
        else:
            return False

    def run(self):
        """"""
        start = datetime.datetime.utcnow()
        frac = 0.1
        plot = [10 * x for x in range(1, self.max_generations // 10 + 1)]
        initial_time = datetime.datetime.utcnow()
        for i in range(self.max_generations):
            if i / self.max_generations >= frac and self.verbose:
                print("Iteration ", str(i), " of ", str(self.max_generations))
                frac += 0.1
            # print("Generation: ", i + 1)
            self._selection()
            self._cross_over()
            self._mutation()
            self._substitution()
            self._update_best()

            if i >= self.max_generations // 5:
                if self._evaluate():
                    break

            if self.plot:
                if (i + 1) in plot:
                    filename = (
                        "plots/ga_"
                        + str(self.graph.number_vertices)
                        + "_"
                        + str(i + 1)
                        + ".png"
                    )
                    title = (
                        "Genetic algorithm. Iteration "
                        + str(i + 1)
                        + "\n Solution cost: "
                        + str(round(self.best_cost, 2))
                    )
                    self.graph.plot_solution(
                        self.best_genes,
                        pheromones=False,
                        filename=filename,
                        title=title,
                    )

            # self.get_best()
            if (datetime.datetime.utcnow() - initial_time).seconds > self.max_time:
                break

        self.time = datetime.datetime.utcnow() - start

        # print('FINISHED')

    def show(self):
        """"""
        print("\nSOLUTION:")
        print(
            "Individuals: "
            + str(self.population_size)
            + ". Iterations: "
            + str(self.max_generations)
        )
        for ind in self.individuals:
            print("Best solution: %s\t|\tcost: %d" % (str(ind.genes), ind.cost))

    def save(self, file):
        """"""
        best = self.individuals[0]
        for individual in self.individuals:
            if individual.cost < best.cost:
                best = individual
        text = (
            "GA. Best solution: "
            + str(best.genes)
            + "\t|\tCost: "
            + str(best.cost)
            + "\n"
        )
        with open(file, "a") as myfile:
            myfile.write(text)

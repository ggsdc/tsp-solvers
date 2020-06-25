import random

import math


class Ant:
    def __init__(self, alpha, beta, number_vertices, graph):
        self.alpha = alpha
        self.beta = beta
        self.number_vertices = number_vertices
        self.graph = graph
        self.solution = None
        self.cost = 0

    def _select_node(self):
        unvisited_vertices = [vertice for vertice in range(self.number_vertices) if vertice not in self.solution]

        denominator = 0
        for unvisited in unvisited_vertices:
            pheromone = math.pow(self.graph.edges[(self.solution[-1], unvisited)].pheromone, self.alpha)
            visibility = math.pow(1 / self.graph.edges[(self.solution[-1], unvisited)].cost, self.beta)
            denominator += pheromone * visibility

        random_value = random.uniform(0, 1)
        cumulative_probability = 0
        for unvisited in unvisited_vertices:
            pheromone = math.pow(self.graph.edges[(self.solution[-1], unvisited)].pheromone, self.alpha)
            visibility = math.pow(1 / self.graph.edges[(self.solution[-1], unvisited)].cost, self.beta)
            cumulative_probability += (pheromone * visibility) / denominator
            if cumulative_probability >= random_value:
                return unvisited

    def find_solution(self):
        self.solution = [random.randint(0, self.number_vertices - 1)]
        while len(self.solution) < self.number_vertices:
            self.solution.append(self._select_node())
        return self.solution

    def get_cost(self):
        self.cost = self.graph.get_cost(self.solution)
        return self.cost


class ACO:
    def __init__(self, mode='ACS', graph=None, iterations=100, population_size=10, elitist_weight=1,
                 min_scaling_factor=0.001, alpha=1, beta=3, rho=0.1, pheromone_deposit=1, initial_pheromone=1):
        self.mode = mode
        self.graph = graph
        self.iterations = iterations
        self.population_size = population_size
        self.elitist_weight = elitist_weight
        self.min_scaling_factor = min_scaling_factor
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.pheromone_deposit = pheromone_deposit
        self.initial_pheromone = initial_pheromone
        self.number_vertices = self.graph.number_vertices

        for edge in self.graph.edges:
            self.graph.update_pheromone(edge, initial_pheromone)

        self.ants = [Ant(alpha, beta, self.number_vertices, self.graph) for _ in range(self.population_size)]

        self.best_solution = None
        self.best_cost = float("inf")

    def _add_pheromone(self, solution, cost, weight=1):
        pheromone_to_add = self.pheromone_deposit / cost
        for i in range(self.number_vertices):
            self.graph.edges[(solution[i], solution[(i+1) % self.number_vertices])].pheromone = \
                self.graph.edges[(solution[i], solution[(i+1) % self.number_vertices])].pheromone * self.rho +\
                weight * pheromone_to_add

    def get_best(self):
        best = self.ants[0]
        for ant in self.ants:
            if ant.cost < best.cost:
                best = ant

        print('BEST SOLUTION: ', str(best.solution), ". Cost: ", str(best.cost))


    def _acs(self):
        frac = 0.1
        for i in range(self.iterations):
            if i / self.iterations >= frac:
                print(str(frac * 100) + '% iterations complete')
                frac += 0.1
            for ant in self.ants:
                self._add_pheromone(ant.find_solution(), ant.get_cost())
                if ant.cost < self.best_cost:
                    self.best_solution = ant.solution
                    self.best_cost = ant.cost

    def run(self):
        if self.mode == 'ACS':
            self._acs()
        else:
            pass

    def show(self):
        print("\nSOLUTION:")
        print("Ants: " + str(self.population_size) + ". Iterations: " + str(self.iterations) + "\n")
        for ant in self.ants:
            print('Best solution: %s\t|\tcost: %d' % (str(ant.solution), ant.cost))

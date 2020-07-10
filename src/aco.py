import datetime
import math
import random


class Ant:
    def __init__(self, alpha, beta, number_vertices, graph):
        self.alpha = alpha
        self.beta = beta
        self.number_vertices = number_vertices
        self.graph = graph
        self.solution = None
        self.cost = 0
        self.unvisited_nodes = list(self.graph.vertices)

    def _select_node(self):

        denominator = 0
        for unvisited in self.unvisited_nodes:
            pheromone = math.pow(self.graph.edges[(self.solution[-1], unvisited)].pheromone, self.alpha)
            visibility = math.pow(1 / self.graph.edges[(self.solution[-1], unvisited)].cost, self.beta)
            denominator += pheromone * visibility

        random_value = random.uniform(0, 1)
        cumulative_probability = 0
        for unvisited in self.unvisited_nodes:
            pheromone = math.pow(self.graph.edges[(self.solution[-1], unvisited)].pheromone, self.alpha)
            visibility = math.pow(1 / self.graph.edges[(self.solution[-1], unvisited)].cost, self.beta)
            cumulative_probability += (pheromone * visibility) / denominator
            if cumulative_probability >= random_value:
                self.unvisited_nodes.remove(unvisited)
                return unvisited

    def find_solution(self):
        self.solution = [random.randint(0, self.number_vertices - 1)]
        self.unvisited_nodes = list(self.graph.vertices)
        self.unvisited_nodes.remove(self.solution[0])
        while len(self.solution) < self.number_vertices:
            self.solution.append(self._select_node())
        return self.solution

    def get_cost(self):
        self.cost = self.graph.get_cost(self.solution)
        return self.cost


class ACO:
    def __init__(self, mode='AS', graph=None, iterations=100, population_size=10, elitist_weight=1,
                 min_scaling_factor=0.001, alpha=1, beta=3, rho=0.1, pheromone_deposit=1, initial_pheromone=1,
                 max_time=60):
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
        self.max_time = max_time

        for edge in self.graph.edges:
            self.graph.update_pheromone(edge, initial_pheromone)

        self.ants = [Ant(alpha, beta, self.number_vertices, self.graph) for _ in range(self.population_size)]

        self.best_solution = None
        self.best_cost = float("inf")

    def _add_pheromone(self, solution, cost, weight=1):
        pheromone_to_add = self.pheromone_deposit / cost
        for i in range(self.number_vertices):
            self.graph.edges[(solution[i], solution[(i + 1) % self.number_vertices])].pheromone = \
                self.graph.edges[(solution[i], solution[(i + 1) % self.number_vertices])].pheromone + \
                weight * pheromone_to_add

    def get_best(self):
        best = self.ants[0]
        for ant in self.ants:
            if ant.cost < best.cost:
                best = ant
        print('\nACO:')
        print('Best solution: ', str(best.solution), "\t|\tcost: ", str(best.cost))

    def evaluate(self):
        costs = [i.cost for i in self.ants]
        mean_cost = sum(costs) / len(costs)
        min_cost = min(costs)

        if min_cost*1.01 > mean_cost:
            print('BREAK')
            return True
        else:
            return False

    def _as(self):
        frac = 0.01
        initial_time = datetime.datetime.utcnow()
        for i in range(self.iterations):
            if i / self.iterations >= frac:
                print("Iteration ", str(i), " of ", str(self.iterations))
                frac += 0.01

            if i != 0:
                for edge in self.graph.edges:
                    self.graph.edges[edge].pheromone = self.graph.edges[edge].pheromone * (1 - self.rho)

            for ant in self.ants:
                self._add_pheromone(ant.find_solution(), ant.get_cost())
                if ant.cost < self.best_cost:
                    self.best_solution = ant.solution
                    self.best_cost = ant.cost

            if i > self.iterations // 10:
                if self.evaluate():
                    break

            if (datetime.datetime.utcnow()- initial_time).seconds > self.max_time:
                break

    def run(self):
        if self.mode == 'AS':
            self._as()
        else:
            pass

    def show(self):
        print("\nSOLUTION:")
        print("Ants: " + str(self.population_size) + ". Iterations: " + str(self.iterations) + "\n")
        for ant in self.ants:
            print('Best solution: %s\t|\tcost: %d' % (str(ant.solution), ant.cost))

    def save(self, file):
        best = self.ants[0]
        for ant in self.ants:
            if ant.cost < best.cost:
                best = ant
        text = 'ACO. Best solution: ' + str(best.solution) + "\t|\tCost: " + str(best.cost) +'\n'
        with open(file, "a") as myfile:
            myfile.write(text)



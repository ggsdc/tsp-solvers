import copy
import datetime
import random
from statistics import mean


class Individual:
    """
    The genes are the solution (path)
    """

    def __init__(self, genes, cost, idx):
        self.genes = genes
        self.cost = cost
        self.number_vertices = len(genes)
        self.id = idx

    def swap(self, gene_1, gene_2):
        a = self.genes.index(gene_1)
        b = self.genes.index(gene_2)

        aux = self.genes[a]
        self.genes[a] = self.genes[b]
        self.genes[b] = aux

        self.__reset_params()

    def add(self, gene):
        self.genes.append(gene)
        self.__reset_params()

    def __reset_params(self):
        self.cost = 0

    def random_sub_solution(self):
        start = random.randrange(0, self.number_vertices)
        end = start
        while end == start or abs(end - start) == 1 or abs(end - start) == len(self.genes) - 1:
            end = random.randrange(0, self.number_vertices)
        if start > end:
            start, end = end, start
        return self.genes[start:end]

    def remove_vertice(self, x):
        if x in self.genes:
            del self.genes[self.genes.index(x)]

    def insert_sub_solution(self, sub_solution, x):
        if x != -1:
            self.genes = self.genes[:x + 1] + sub_solution + self.genes[x + 1:]
        else:
            self.genes = self.genes + sub_solution

    def mutate(self):
        i = random.randrange(0, self.number_vertices)
        j = random.randrange(0, self.number_vertices)
        while i == j:
            j = random.randrange(0, self.number_vertices)

        aux = self.genes[i]
        self.genes[i] = self.genes[j]
        self.genes[j] = aux

    def __str__(self):
        return str(self.genes)


class GA:

    def __init__(self, graph, max_generations, population_size, mutation_probability, max_time):
        """

        """
        self.individuals = list()
        self.graph = graph
        self.max_generations = max_generations
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.mating_pool = []
        self.children = []
        self.id = 1
        self.max_time = max_time

        solutions = self.graph.get_random_path(self.population_size)
        for solution in solutions:
            individual = Individual(genes=solution, cost=self.graph.get_cost(solution), idx=self.id)
            self.id += 1
            self.individuals.append(individual)

    def get_best(self):
        best = self.individuals[0]
        for individual in self.individuals:
            if individual.cost < best.cost:
                best = individual
        print("\nGA:")
        print('Best solution: ', str(best.genes), "\t|\tcost: ", str(best.cost))

    def best_insertion(self, child, sub_solution):
        start = sub_solution[0]
        end = sub_solution[1]
        best_payoff = float('-inf')
        j = 0
        for i in range(0, len(child.genes) - 1):
            payoff = self.graph.edges[(child.genes[i], child.genes[i + 1])].cost - \
                     self.graph.edges[(child.genes[i], start)].cost - \
                     self.graph.edges[(end, child.genes[i + 1])].cost

            if payoff > best_payoff:
                best_payoff = payoff
                j = i

        payoff = self.graph.edges[(child.genes[-1], child.genes[0])].cost - \
                 self.graph.edges[(child.genes[-1], start)].cost - \
                 self.graph.edges[(end, child.genes[0])].cost

        if payoff > best_payoff:
            best_payoff = payoff
            j = -1

        return j

    def cross_over(self):
        self.children = []
        for n in range(0, self.population_size // 2):
            ind1 = random.choice(self.mating_pool)
            ind2 = random.choice(self.mating_pool)

            child = copy.deepcopy(ind1)
            child.id = self.id
            self.id += 1
            sub_solution = ind2.random_sub_solution()

            for x in sub_solution:
                child.remove_vertice(x)

            n = self.best_insertion(child, sub_solution)
            child.insert_sub_solution(sub_solution, n)
            child.cost = self.graph.get_cost(child.genes)
            self.children.append(child)

    def selection(self):
        self.mating_pool = []
        iterator_list = copy.deepcopy(self.individuals)
        while len(self.mating_pool) < self.population_size // 2:
            selected = min(iterator_list, key=lambda i: i.cost)
            iterator_list.remove(selected)
            self.mating_pool.append(selected)

    def mutation(self):
        for i in range(len(self.children)):
            prob = random.uniform(0, 1)
            if prob < self.mutation_probability:
                self.children[i].mutate()
                self.children[i].cost = self.graph.get_cost(self.children[i].genes)

    def substitution(self):
        new_population = []
        iterator_list = copy.deepcopy(self.individuals + self.children)

        while len(new_population) < self.population_size:
            selected = min(iterator_list, key=lambda i: i.cost)
            iterator_list.remove(selected)
            new_population.append(selected)

        self.individuals = new_population

    def evaluate(self):
        costs = [i.cost for i in self.individuals]
        mean_cost = sum(costs) / len(costs)
        min_cost = min(costs)
        if min_cost * 1.01 > mean_cost:
            print('BREAK')
            return True
        else:
            return False

    def run(self):
        frac = 0.1
        initial_time = datetime.datetime.utcnow()
        for i in range(self.max_generations):
            if i / self.max_generations >= frac:
                print("Iteration ", str(i), " of ", str(self.max_generations))
                frac += 0.1
            # print("Generation: ", i + 1)
            self.selection()
            self.cross_over()
            self.mutation()
            self.substitution()

            if i > self.max_generations // 2:
                if self.evaluate():
                    break

            # self.get_best()
            if (datetime.datetime.utcnow() - initial_time).seconds > self.max_time:
                break

        # print('FINISHED')
    def show(self):
        print("\nSOLUTION:")
        print("Individuals: " + str(self.population_size) + ". Iterations: " + str(self.max_generations))
        for ind in self.individuals:
            print('Best solution: %s\t|\tcost: %d' % (str(ind.genes), ind.cost))

    def save(self, file):
        best = self.individuals[0]
        for individual in self.individuals:
            if individual.cost < best.cost:
                best = individual
        text = 'GA. Best solution: ' + str(best.genes) + "\t|\tCost: " + str(best.cost) + '\n'
        with open(file, "a") as myfile:
            myfile.write(text)

from ..initializers import NearestNeighbor, RandomInitializer
import datetime
import copy


class TwoOpt:

    def __init__(self, graph, max_time, init="random", plot=False):
        self.graph = graph
        self.max_time = max_time
        self.init = init
        self.plot = plot
        self.initializer = None
        self.cost = float("Inf")
        self.count = 0
        if self.init == "random":
            self.initializer = RandomInitializer(self.graph, 1)
        elif self.init == "nearest":
            self.initializer = NearestNeighbor(self.graph, 1)

        self.solution = self.initializer.get_init()[0]
        self.cost = self.graph.get_cost(self.solution)

    def get_best(self):
        # print("\nTwo opt:")
        print("Best solution: ", str(self.solution), "\t|\tcost: ", str(round(self.cost, 2)), "\t|\tswaps: ", str(self.count))

    def run(self):
        initial_time = datetime.datetime.utcnow()
        while (datetime.datetime.utcnow() - initial_time).seconds <= self.max_time:
            swap = False
            for i in range(len(self.solution)):
                for j in range(len(self.solution)):

                    if i == j:
                        continue

                    aux_solution = copy.copy(self.solution)
                    aux_solution[i], aux_solution[j] = aux_solution[j], aux_solution[i]
                    aux_cost = self.graph.get_cost(aux_solution)

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

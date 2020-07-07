from pulp import *


class LP:
    def __init__(self, graph, max_time):
        self.graph = graph
        self.model = LpProblem("TSP problem", LpMinimize)
        self.v01Travels = LpVariable.dicts("Travel", ((edge[0], edge[1]) for edge in self.graph.edges), cat="Binary")
        self.vOneTour = LpVariable.dicts("Aux", (v for v in self.graph.vertices), cat="Integer")
        self.vertice_list = list(self.graph.vertices)
        self.temp_solution = list()
        self.solution = list()
        self.cost = 0
        self.max_time = max_time

    def build_model(self):

        for v in self.graph.vertices:
            self.model += lpSum(self.v01Travels[v, x] for x in self.graph.vertices if x != v) == 1
            self.model += lpSum(self.v01Travels[x, v] for x in self.graph.vertices if x != v) == 1

        for i in self.vertice_list:
            for j in self.vertice_list:
                if i != j and i != self.vertice_list[0] and j != self.vertice_list[0]:
                    self.model += self.vOneTour[i] - self.vOneTour[j] + self.graph.number_vertices * self.v01Travels[
                        i, j] <= self.graph.number_vertices - 1

        for i in self.vertice_list:
            if i != self.vertice_list[0]:
                self.model += self.vOneTour[i] <= self.graph.number_vertices - 1

        self.model += lpSum(
            self.v01Travels[edge[0], edge[1]] * self.graph.edges[edge].cost for edge in self.graph.edges)

    def run(self):
        # self.model.solve(
        #     GUROBI_CMD(msg=1, options=[('TimeLimit', self.max_time), ('MIPGap', 0.05), ('MIPGapAbs', 0.05)]))
        self.model.solve(PULP_CBC_CMD(msg=1, fracGap=0.05, maxSeconds=self.max_time))

        print(self.model.status)
        if self.model.status == 1:
            self.solution = list()
            self.temp_solution = list()
            for v in self.model.variables():
                if v.varValue > 0 and "Travel" in v.name:
                    aux = v.name[7:]
                    aux = aux.replace("_", "", 1)
                    self.temp_solution.append(aux)

            array = self.temp_solution[0].split(",")
            self.solution.append(int(array[0][1:]))
            self.solution.append(int(array[1][:-1]))

            del self.temp_solution[0]
            while True:
                for i in range(len(self.temp_solution)):
                    array = self.temp_solution[i].split(",")
                    if array[0][1:] == str(self.solution[-1]):
                        self.solution.append(int(array[1][:-1]))
                        del self.temp_solution[i]
                        break

                if len(self.temp_solution) == 0:
                    break

            del self.solution[-1]

            self.cost = self.graph.get_cost(self.solution)

        else:
            self.cost = float("-inf")

    def show(self):
        print("\nLinear programming formulation:")
        print("Best solution: " + str(self.solution) + "\t|\tcost: " + str(self.cost))

    def save(self, file):
        text = 'LP. Best solution: ' + str(self.solution) + "\t|\tCost: " + str(self.cost) + '\n'
        with open(file, "a") as myfile:
            myfile.write(text)

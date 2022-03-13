import datetime

from pulp import *

from .base import BaseSolver


class LinearIntegerProgram(BaseSolver):
    def __init__(self, graph, max_time, plot=False):
        super().__init__()
        self.graph = graph
        self.model = LpProblem("TSP problem", LpMinimize)
        self.vertices_list = self.graph.vertices
        self.v01Travels = None
        self.vOneTour = None
        self.temp_solution = list()
        self.solution = list()
        self.cost = 0
        self.max_time = max_time
        self.time = None
        self.plot = plot
        if self.plot:
            if "matplotlib" not in sys.modules:
                raise ModuleNotFoundError(
                    "Matplotlib has to be installed to be able to plot!"
                )

    def build_model(self):

        self.v01Travels = LpVariable.dicts(
            "Travel",
            (
                (v1.idx, v2.idx)
                for v1 in self.vertices_list
                for v2 in self.vertices_list
                if v1 != v2
            ),
            cat="Binary",
        )
        self.vOneTour = LpVariable.dicts(
            "Aux", (v.idx for v in self.graph.vertices), cat="Integer"
        )

        for v in self.vertices_list:
            self.model += (
                lpSum(
                    self.v01Travels[v.idx, x.idx] for x in self.vertices_list if x != v
                )
                == 1
            )
            self.model += (
                lpSum(
                    self.v01Travels[x.idx, v.idx] for x in self.vertices_list if x != v
                )
                == 1
            )

        for i in self.vertices_list:
            for j in self.vertices_list:
                if i != j and i != self.vertices_list[0] and j != self.vertices_list[0]:
                    self.model += (
                        self.vOneTour[i.idx]
                        - self.vOneTour[j.idx]
                        + self.graph.number_vertices * self.v01Travels[i.idx, j.idx]
                        <= self.graph.number_vertices - 1
                    )

        for i in self.vertices_list:
            if i != self.vertices_list[0]:
                self.model += self.vOneTour[i.idx] <= self.graph.number_vertices - 1

        self.model += lpSum(
            self.v01Travels[edge[0], edge[1]] * self.graph.edges_collection[edge].cost
            for edge in self.graph.edges_collection
        )

    def run(self):
        start = datetime.datetime.utcnow()

        self.model.solve(PULP_CBC_CMD(msg=True, gapRel=0.05, timeLimit=self.max_time))

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

            self.solution = [
                self.graph.vertices_collection[idx] for idx in self.solution
            ]

            self.cost = self.graph.get_solution_cost(self.solution)

            if self.plot:
                filename = "plots/lp_" + str(self.graph.number_vertices) + ".png"
                title = (
                    "Mathematical optimization "
                    + "\n Solution cost: "
                    + str(round(self.cost, 2))
                )
                self.graph.plot_solution(
                    self.solution, pheromones=False, filename=filename, title=title
                )

        else:
            self.cost = float("-inf")

        self.time = datetime.datetime.utcnow() - start

    def show(self):
        print("\nLinear programming formulation:")
        print("Best solution: " + str(self.solution) + "\t|\tcost: " + str(self.cost))

    def save(self, file):
        text = (
            "LP. Best solution: "
            + str(self.solution)
            + "\t|\tCost: "
            + str(self.cost)
            + "\n"
        )
        with open(file, "a") as myfile:
            myfile.write(text)

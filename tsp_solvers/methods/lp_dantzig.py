from datetime import datetime

from pulp import (
    LpProblem,
    LpMinimize,
    LpVariable,
    lpSum,
    value,
    PULP_CBC_CMD,
)
from pytups import SuperDict

from tsp_solvers.methods.base import BaseSolver


class LinearIntegerDantzig(BaseSolver):
    def __init__(self, graph, max_time, plot=False):
        super().__init__()
        self.graph = graph
        self.model = LpProblem("TSP problem (DFJ)", LpMinimize)
        self.vertices_list = self.graph.vertices
        self.travel = SuperDict()
        self.max_time = max_time
        self.solution = []
        self.cost = float("-inf")
        self.plot = plot

    def build_model(self):
        self.travel = LpVariable.dicts(
            "Travel",
            (
                (v1.idx, v2.idx)
                for v1 in self.vertices_list
                for v2 in self.vertices_list
                if v1 != v2
            ),
            cat="Binary",
        )
        self.travel = SuperDict(self.travel)

        # objective function
        self.model += lpSum(
            self.travel[edge[0], edge[1]] * self.graph.edges_collection[edge].cost
            for edge in self.graph.edges_collection
        )

        # constraints
        for v in self.vertices_list:
            self.model += (
                lpSum(self.travel[v.idx, x.idx] for x in self.vertices_list if x != v)
                == 1
            )
            self.model += (
                lpSum(self.travel[x.idx, v.idx] for x in self.vertices_list if x != v)
                == 1
            )

    def run(self):
        count = 0
        start_time = datetime.utcnow()
        while (datetime.utcnow() - start_time).seconds <= self.max_time:
            received_status = self.model.solve(
                PULP_CBC_CMD(msg=False, timeLimit=self.max_time, mip=True)
            )
            if self.model.status == 1:
                travels = self.travel.vfilter(lambda v: value(v)).keys_tl()
                subtours = self.find_subtours(travels)
                if len(subtours) > 1:
                    self.add_subtour_constraint(subtours)

                else:
                    start = travels[0][0]
                    end = travels[0][1]
                    travels = travels[1:]
                    temp = [start]
                    while travels:
                        for travel in travels:
                            if travel[0] == end:
                                start = travel[0]
                                end = travel[1]
                                temp.append(start)
                                travels.remove(travel)
                                break
                    self.solution = self.solution = [
                        self.graph.vertices_collection[idx] for idx in temp
                    ]
                    self.cost = self.graph.get_cost(self.solution)
                    self.time = datetime.utcnow() - start_time
                    self.model.writeMPS("dfj.mps")
                    break
            else:
                self.cost = float("-inf")

        self.time = datetime.utcnow() - start_time
        if self.plot:
            filename = "plots/dantzig_" + str(self.graph.number_vertices) + ".png"
            title = (
                "Mathematical optimization "
                + "\n Solution cost: "
                + str(round(self.cost, 2))
            )
            self.graph.plot_solution(
                self.solution, pheromones=False, filename=filename, title=title
            )

    def find_subtours(self, travels):
        unvisited = [vertex.idx for vertex in self.vertices_list]
        temp = list(travels)
        start = temp[0][0]
        end = temp[0][1]
        temp = temp[1:]
        unvisited.remove(start)
        subtour = [start]
        subtours = []
        while unvisited:
            check = False
            for travel in temp:
                if travel[0] == end:
                    start = travel[0]
                    end = travel[1]
                    unvisited.remove(start)
                    subtour.append(start)
                    temp.remove(travel)
                    check = True
                    break
            if check is False:
                subtours.append(subtour)
                start = temp[0][0]
                end = temp[0][1]
                temp = temp[1:]
                unvisited.remove(start)
                subtour = [start]
        subtours.append(subtour)
        return subtours

    def add_subtour_constraint(self, subtours):
        for subtour in subtours:
            self.model += (
                lpSum(self.travel[i, j] for i in subtour for j in subtour if i != j)
                <= len(subtour) - 1
            )

    def get_best(self):
        print("\nLinear Dantzig programming formulation:")
        print(f"Best solution: {self.cost} \t|\t Time: {self.time}")

    def get_solution_value(self):
        return self.cost

    def get_solution_time(self):
        return self.time

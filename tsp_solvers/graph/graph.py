"""
This file contains the Graph class that is used to represent the TSp problem.
This graph is constructed from nodes and edges
"""
# TODO: add more supported file types

# Import from libraries
import json
import random
import sys
from math import pow, sqrt
import traceback

# Matplotlib is not an required requirement
try:
    import matplotlib.pyplot as plt

    plt.ioff()
except ModuleNotFoundError:
    pass
except NameError:
    pass


class Edge:
    def __init__(self, data):
        self.origin = data.get("origin")
        self.destination = data.get("destination")
        self.cost = data.get("cost", 0)
        self.pheromone = data.get("pheromone", 0)
        self._hash = self.__hash__()

    def set_cost(self, cost):
        self.cost = cost

    def set_pheromone(self, pheromone):
        self.pheromone = pheromone

    def __hash__(self):
        return hash((self.origin.idx, self.destination.idx))

    def __eq__(self, other):
        if not isinstance(other, Edge):
            raise NotImplemented("The objects do not share the same class")
        return self._hash == other._hash

    def __repr__(self):
        return "Origin: {}, Destination: {}, Cost: {}".format(
            self.origin, self.destination, self.cost
        )


class Vertex:
    def __init__(self, data):
        self.idx = data.get("idx")
        self.x = data.get("x")
        self.y = data.get("y")
        self._hash = self.__hash__()
        self.attributes_to_dict = ["idx", "x", "y"]

    def __hash__(self):
        return hash((self.idx, self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self._hash == other._hash
        elif isinstance(other, int):
            return self.idx == other
        else:
            raise NotImplemented("The objects do not share the same class")

    def __lt__(self, other):
        if isinstance(other, Vertex):
            return self._hash < other._hash
        elif isinstance(other, int):
            return self.idx < other
        else:
            raise NotImplemented("The objects do not share the same class")

    def __le__(self, other):
        if isinstance(other, Vertex):
            return self._hash <= other._hash
        elif isinstance(other, int):
            return self.idx <= other
        else:
            raise NotImplemented("The objects do not share the same class")

    def __repr__(self):
        return "Vertex: {}".format(self.idx)


class Graph:
    def __init__(self):
        self.data = None
        self.number_vertices = None
        self.edges = list()
        self.edges_collection = dict()
        self.vertices = list()
        self.vertices_collection = dict()

    def add_edge(self, vertex_1, vertex_2, cost=0.0, check=False):
        edge = Edge({"origin": vertex_1, "destination": vertex_2})
        if check:
            for created_edge in self.edges:
                if edge == created_edge:
                    return False

        edge.set_cost(cost)
        self.edges_collection[(vertex_1.idx, vertex_2.idx)] = edge
        self.edges.append(edge)

    def calculate_cost(self, vertex_1, vertex_2):

        distance = sqrt(
            pow(
                vertex_1.x - vertex_2.x,
                2,
            )
            + pow(
                vertex_1.y - vertex_2.y,
                2,
            )
        )
        return distance

    def plot(self):
        x_coord = [vertex.x for vertex in self.vertices]
        y_coord = [vertex.y for vertex in self.vertices]
        if "matplotlib" not in sys.modules:
            raise ModuleNotFoundError(
                "Matplotlib has to be installed to be able to plot!"
            )
        plt.close()
        plt.scatter(x_coord, y_coord, c="#000000")
        plt.show()

    def plot_solution(self, path, pheromones=False, filename="none.png", title=""):
        if "matplotlib" not in sys.modules:
            raise ModuleNotFoundError(
                "Matplotlib has to be installed to be able to plot!"
            )
        plt.close()

        # if pheromones:
        #     min_pheromone = 100
        #     max_pheromone = 0
        #     for i in self.edges:
        #         if min_pheromone > self.edges[i].pheromone:
        #             min_pheromone = self.edges[i].pheromone
        #
        #         if max_pheromone < self.edges[i].pheromone:
        #             max_pheromone = self.edges[i].pheromone
        #
        #     pheromone_dict = {
        #         key: 0.0
        #         + (self.edges[key].pheromone - min_pheromone)
        #         * 0.4
        #         / (max_pheromone - min_pheromone)
        #         for key in self.edges
        #     }
        #
        #     for i in pheromone_dict:
        #         x_values = [
        #             self.vertices_coordinates[i[0]][0],
        #             self.vertices_coordinates[i[1]][0],
        #         ]
        #         y_values = [
        #             self.vertices_coordinates[i[0]][1],
        #             self.vertices_coordinates[i[1]][1],
        #         ]
        #         plt.plot(
        #             x_values,
        #             y_values,
        #             c="#FF0000",
        #             alpha=pheromone_dict[i],
        #             linewidth=3,
        #         )

        x_coord = [vertex.x for vertex in self.vertices]
        y_coord = [vertex.y for vertex in self.vertices]
        plt.scatter(x_coord, y_coord, c="#000000")
        for i in range(self.number_vertices - 1):
            x_values = [self.vertices[i].x, self.vertices[i + 1].x]
            y_values = [self.vertices[i].y, self.vertices[i + 1].y]
            plt.plot(x_values, y_values, c="#000000")

        x_values = [
            self.vertices[self.number_vertices - 1].x,
            self.vertices[0].x,
        ]
        y_values = [
            self.vertices[self.number_vertices - 1].yº,
            self.vertices[0].y,
        ]
        plt.plot(x_values, y_values, c="#000000")

        plt.title(title)
        plt.savefig(filename)

    def random_complete_graph(self, size):
        self.number_vertices = size

        for i in range(self.number_vertices):
            new = True
            while new:
                temp = {
                    "idx": i,
                    "x": random.randint(0, self.number_vertices * 2),
                    "y": random.randint(0, self.number_vertices * 2),
                }
                temp_vertex = Vertex(temp)
                repeat = False
                for vertex in self.vertices:
                    if vertex == temp_vertex:
                        repeat = True

                if not repeat:
                    new = False
            self.vertices.append(temp_vertex)
            self.vertices_collection[temp_vertex.idx] = temp_vertex

        for i in self.vertices:
            for j in self.vertices:
                if i < j:
                    cost = self.calculate_cost(i, j)
                    self.add_edge(i, j, cost)
                    self.add_edge(j, i, cost)

    def create_graph_from_json(self, path: str):
        # TODO: add json schema validation here of kwargs so if data is passed no need to execute another method
        with open(path) as f:
            self.data = json.load(f)
        self.number_vertices = len(self.data.get("vertices"))
        self.vertices = [Vertex(vertex) for vertex in self.data.get("vertices")]

        edges = self.data.get("edges", None)
        if edges is None:
            for i in self.vertices:
                for j in self.vertices:
                    if i < j:
                        cost = self.calculate_cost(i, j)
                        self.add_edge(i, j, cost)
                        self.add_edge(j, i, cost)

        else:
            # TODO: implement if the json has edges
            pass

    def create_graph_from_db(self):
        pass

    def create_graph_from_tsp(self, path: str):
        with open(path) as f:
            text = f.read()
            _, nodes = text.split("NODE_COORD_SECTION")
            nodes = nodes.split("\n")
            nodes = nodes[1:-1]
            nodes = [node.split(" ") for node in nodes]

        self.number_vertices = len(nodes)
        print(nodes)

        self.vertices = [
            Vertex({"idx": int(node[0]), "x": float(node[1]), "y": float(node[2])})
            for node in nodes
        ]

        self.vertices_collection = {vertex.idx: vertex for vertex in self.vertices}

        for i in self.vertices:
            for j in self.vertices:
                if i < j:
                    cost = self.calculate_cost(i, j)
                    self.add_edge(i, j, cost)
                    self.add_edge(j, i, cost)

    def get_random_paths(self, size):
        random_paths = []

        for i in range(size):
            random_list = random.sample(self.vertices, len(self.vertices))
            random_paths.append(random_list)

        return random_paths

    def get_cost(self, path):
        total_cost = 0
        for i in range(self.number_vertices - 1):
            total_cost += self.edges_collection[(path[i].idx, path[i + 1].idx)].cost

        total_cost += self.edges_collection[
            (path[self.number_vertices - 1].idx, path[0].idx)
        ].cost
        return total_cost

    def update_pheromone(self, edge, pheromone):
        self.edges_collection[edge].pheromone = pheromone

    def save_graph_to_json(self, path):
        with open(path, "w") as f:
            json.dump(
                {
                    "vertices": [
                        {
                            key: value
                            for key, value in vertex.__dict__.items()
                            if key in vertex.attributes_to_dict
                        }
                        for vertex in self.vertices
                    ]
                },
                f,
            )

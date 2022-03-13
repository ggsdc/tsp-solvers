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
        self.degree = 0
        self._hash = self.__hash__()
        self.attributes_to_dict = ["idx", "x", "y"]

    def is_odd(self):
        return self.degree % 2 != 0

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
        # Used in Christofides approach
        self.components_groups = list()

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

        self._create_edges()

    def create_graph_from_json(self, path: str):
        # TODO: add json schema validation here of kwargs so if data is passed no need to execute another method
        # TODO: add vertices_collection
        with open(path) as f:
            self.data = json.load(f)
        self.number_vertices = len(self.data.get("vertices"))
        self.vertices = [Vertex(vertex) for vertex in self.data.get("vertices")]
        self.vertices_collection = {vertex.idx: vertex for vertex in self.vertices}

        edges = self.data.get("edges", None)
        if edges is None:
            self._create_edges()

        else:
            # TODO: implement if the json has edges
            pass

    def create_graph_from_tsp(self, path: str):
        with open(path) as f:
            text = f.read()
            _, nodes = text.split("NODE_COORD_SECTION")
            nodes = nodes.split("\n")
            nodes = nodes[1:-1]
            nodes = [node.split(" ") for node in nodes]

        self.number_vertices = len(nodes)

        self.vertices = [
            Vertex({"idx": int(node[0]), "x": float(node[1]), "y": float(node[2])})
            for node in nodes
        ]

        self.vertices_collection = {vertex.idx: vertex for vertex in self.vertices}

        self._create_edges()

    def create_graph_from_db(self):
        pass

    def create_graph_from_schema(self, data):
        aux_vertices = list(set([d["n1"] for d in data] + [d["n2"] for d in data]))
        self.number_vertices = len(aux_vertices)
        self.vertices = [
            Vertex({"idx": vertex, "x": 0, "y": 0}) for vertex in aux_vertices
        ]

        self.vertices_collection = {vertex.idx: vertex for vertex in self.vertices}

        self.edges = [
            Edge(
                {
                    "origin": self.vertices_collection[d["n1"]],
                    "destination": self.vertices_collection[d["n2"]],
                    "cost": d["w"],
                }
            )
            for d in data
            if d["n1"] != d["n2"]
        ] + [
            Edge(
                {
                    "origin": self.vertices_collection[d["n2"]],
                    "destination": self.vertices_collection[d["n1"]],
                    "cost": d["w"],
                }
            )
            for d in data
            if d["n1"] != d["n2"]
        ]

        self.edges_collection = {
            (edge.origin.idx, edge.destination.idx): edge for edge in self.edges
        }

    def create_minimum_spanning_tree(self):
        # With Boruvka algorithm - kind of
        self._clean_edges()
        completed = False
        # First iteration
        for vertex in self.vertices:
            rest = {
                other: self.calculate_cost(vertex, other)
                for other in self.vertices
                if other != vertex
            }

            nearest = min(rest, key=rest.get)

            self.edges.append(
                Edge(
                    {
                        "origin": vertex,
                        "destination": nearest,
                        "cost": rest[nearest],
                    }
                )
            )
            self.edges_collection[(vertex.idx, nearest.idx)] = self.edges[-1]

        self._calculate_first_components()

        if len(self.components_groups) == 1:
            completed = True

        while not completed:
            # Function to check if we have only one component to exit loop

            for group1 in self.components_groups:
                rest = {}
                for group2 in self.components_groups:
                    if group1 != group2:
                        for origin in group1:
                            for destination in group2:
                                rest[origin, destination] = self.calculate_cost(
                                    origin, destination
                                )

                nearest = min(rest, key=rest.get)

                self.edges.append(
                    Edge(
                        {
                            "origin": nearest[0],
                            "destination": nearest[1],
                            "cost": rest[nearest],
                        }
                    )
                )

                self.edges_collection[(nearest[0].idx, nearest[1].idx)] = self.edges[-1]

                break

            self._update_components()

            if len(self.components_groups) == 1:
                completed = True
                self.plot_edges()

    def create_full_odd_graph(self):
        self._calculate_vertices_degrees()
        self._clean_edges()
        self._subset_odd_vertices()
        self._create_edges()

    def create_minimum_weight_perfect_matching(self):
        pass

    def get_random_paths(self, number):
        random_paths = []

        for i in range(number):
            random_list = random.sample(self.vertices, len(self.vertices))
            random_paths.append(random_list)

        return random_paths

    def get_solution_cost(self, path):
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

    def plot_edges(self):
        x_coord = [vertex.x for vertex in self.vertices]
        y_coord = [vertex.y for vertex in self.vertices]
        if "matplotlib" not in sys.modules:
            raise ModuleNotFoundError(
                "Matplotlib has to be installed to be able to plot!"
            )
        plt.close()
        plt.scatter(x_coord, y_coord, c="#000000")

        for i in self.edges:
            x_values = [i.origin.x, i.destination.x]
            y_values = [i.origin.y, i.destination.y]
            plt.plot(x_values, y_values, c="#000000")
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
            self.vertices[self.number_vertices - 1].y,
            self.vertices[0].y,
        ]
        plt.plot(x_values, y_values, c="#000000")

        plt.title(title)
        plt.savefig(filename)

    def _add_edge(self, vertex_1, vertex_2, cost=0.0, check=False):
        edge = Edge({"origin": vertex_1, "destination": vertex_2})
        if check:
            for created_edge in self.edges:
                if edge == created_edge:
                    return False

        edge.set_cost(cost)
        self.edges_collection[(vertex_1.idx, vertex_2.idx)] = edge
        self.edges.append(edge)

    def _calculate_vertices_degrees(self):
        # TODO: implement function that either calculates the degrees of all vertices or a given one
        temp_count = {k: 0 for k in self.vertices}
        counted = list()
        for edge in self.edges:
            if (edge.origin, edge.destination) in counted:
                continue
            temp_count[edge.origin] += 1
            temp_count[edge.destination] += 1
            counted.append((edge.destination, edge.origin))

        for key, value in temp_count.items():
            key.degree = value

    def _calculate_first_components(self):
        # TODO: review as it is not working properly.
        self.components_groups = list()
        for edge in self.edges:
            in_group = False
            if not self.components_groups:
                self.components_groups.append([edge.origin, edge.destination])
                continue

            for component in self.components_groups:

                if edge.origin in component or edge.destination in component:

                    if edge.origin in component and edge.destination in component:
                        in_group = True
                        break

                    elif edge.origin in component:
                        component.append(edge.destination)
                        in_group = True
                        break

                    elif edge.destination in component:
                        component.append(edge.origin)
                        in_group = True
                        break

            if not in_group:
                self.components_groups.append([edge.origin, edge.destination])

    def _update_components(self):
        origin = self.edges[-1].origin
        destination = self.edges[-1].destination

        origin_component = [c for c in self.components_groups if origin in c][0]
        destination_component = [c for c in self.components_groups if destination in c][
            0
        ]

        self.components_groups.remove(origin_component)
        self.components_groups.remove(destination_component)

        final_component = list(origin_component) + list(
            set(destination_component) - set(origin_component)
        )

        self.components_groups.append(final_component)

    def _clean_edges(self):
        self.edges = list()
        self.edges_collection = dict()

    def _subset_odd_vertices(self):
        self.vertices = [vertex for vertex in self.vertices if vertex.is_odd()]
        self.vertices_collection = {vertex.idx: vertex for vertex in self.vertices}

    def _create_edges(self):
        for i in self.vertices:
            for j in self.vertices:
                if i < j:
                    cost = self.calculate_cost(i, j)
                    self._add_edge(i, j, cost)
                    self._add_edge(j, i, cost)

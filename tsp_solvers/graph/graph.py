"""

"""

# Import from libraries
import random
import sys
from math import pow, sqrt

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
        self.idx = data.get("idx", 0)
        self.origin = data.get("origin")
        self.destination = data.get("destination")
        self.cost = data.get("cost", 0)
        self.pheromone = data.get("pheromone", 0)

    def set_cost(self, cost):
        self.cost = cost

    def set_pheromone(self, pheromone):
        self.pheromone = pheromone

    def __hash__(self):
        return hash((self.idx, self.origin, self.destination, self.cost))

    def __eq__(self, other):
        if not isinstance(other, Edge):
            raise NotImplemented("The objects do not share the same class")
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return "ID: {}. Origin: {}. Destination: {}. Cost: {}".format(
            self.idx, self.origin, self.destination, self.cost
        )


class Vertex:
    def __init__(self, data):
        self.idx = data.get("id")
        self.x = data.get("x")
        self.y = data.get("y")

    def __hash__(self):
        return hash((self.idx, self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            raise NotImplemented("The objects do not share the same class")
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        if not isinstance(other, Vertex):
            raise NotImplemented("The objects do not share the same class")
        return self.__hash__() < other.__hash__()

    def __le__(self, other):
        if not isinstance(other, Vertex):
            raise NotImplemented("The objects do not share the same class")
        return self.__hash__() <= other.__hash__()

    def __repr__(self):
        return "ID: {}. x: {}. y: {}.".format(self.idx, self.x, self.y)


class Graph:
    def __init__(self, **kwargs):
        self.data = dict(kwargs)
        # TODO: add json schema validation here of kwargs so if data is passed no need to execute another method

        self.edges = dict()
        self.edges_collection = list()
        self.vertices = set()
        self.vertex_collection = list()
        self.vertices_coordinates = dict()
        self.number_vertices = None
        self.x_coordinates = list()
        self.y_coordinates = list()

        # TODO: if data is validated
        # self.create_graph_from_data()

    def edge_exists(self, origin, destination):
        if (origin, destination) in self.edges.keys():
            return True
        else:
            return False

    def add_edge(self, vertex_1, vertex_2, cost=0.0):
        edge = Edge({"origin": vertex_1, "destination": vertex_2})
        for created_edge in self.edges_collection:
            if edge == created_edge:
                return False

        self.edges_collection.append(edge)
        edge.set_cost(cost)

    def calculate_distance(self, vertex_1, vertex_2):

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

    def show(self):
        print("GRAPH:\n")
        for edge in self.edges:
            print(
                "%d linked with %d with cost %d"
                % (edge[0], edge[1], self.edges[edge].cost)
            )

    def plot(self):
        plt.close()
        plt.scatter(self.x_coordinates, self.y_coordinates, c="#000000")
        plt.show()

    def plot_solution(self, path, pheromones=False, filename="none.png", title=""):
        if "matplotlib" not in sys.modules:
            raise ModuleNotFoundError(
                "Matplotlib has to be installed to be able to plot!"
            )
        plt.close()

        if pheromones:
            min_pheromone = 100
            max_pheromone = 0
            for i in self.edges:
                if min_pheromone > self.edges[i].pheromone:
                    min_pheromone = self.edges[i].pheromone

                if max_pheromone < self.edges[i].pheromone:
                    max_pheromone = self.edges[i].pheromone

            pheromone_dict = {
                key: 0.0
                + (self.edges[key].pheromone - min_pheromone)
                * 0.4
                / (max_pheromone - min_pheromone)
                for key in self.edges
            }

            for i in pheromone_dict:
                x_values = [
                    self.vertices_coordinates[i[0]][0],
                    self.vertices_coordinates[i[1]][0],
                ]
                y_values = [
                    self.vertices_coordinates[i[0]][1],
                    self.vertices_coordinates[i[1]][1],
                ]
                plt.plot(
                    x_values,
                    y_values,
                    c="#FF0000",
                    alpha=pheromone_dict[i],
                    linewidth=3,
                )

        plt.scatter(self.x_coordinates, self.y_coordinates, c="#000000")
        for i in range(self.number_vertices - 1):
            x_values = [
                self.vertices_coordinates[path[i]][0],
                self.vertices_coordinates[path[i + 1]][0],
            ]
            y_values = [
                self.vertices_coordinates[path[i]][1],
                self.vertices_coordinates[path[i + 1]][1],
            ]
            plt.plot(x_values, y_values, c="#000000")

        x_values = [
            self.vertices_coordinates[path[self.number_vertices - 1]][0],
            self.vertices_coordinates[path[0]][0],
        ]
        y_values = [
            self.vertices_coordinates[path[self.number_vertices - 1]][1],
            self.vertices_coordinates[path[0]][1],
        ]
        plt.plot(x_values, y_values, c="#000000")

        plt.title(title)
        plt.savefig(filename)

    def random_complete_graph(self, size):
        self.number_vertices = size

        for i in range(self.number_vertices):
            self.vertices.add(i)
            new = True
            while new:
                x = random.randint(0, self.number_vertices * 2)
                y = random.randint(0, self.number_vertices * 2)
                repeat = False

                for j in self.vertices_coordinates:
                    if (
                        self.vertices_coordinates[j][0] == x
                        and self.vertices_coordinates[j][1] == y
                    ):
                        repeat = True
                        break

                if not repeat:
                    new = False

            self.vertices_coordinates[i] = [x, y]

        for i in self.vertices:
            for j in self.vertices:
                if i < j:
                    cost = self.calculate_distance(i, j)
                    self.add_edge(i, j, cost)
                    self.add_edge(j, i, cost)

        self.x_coordinates = [
            self.vertices_coordinates[i][0] for i in self.vertices_coordinates
        ]
        self.y_coordinates = [
            self.vertices_coordinates[i][1] for i in self.vertices_coordinates
        ]

    def create_graph_from_data(self):
        self.number_vertices = len(self.data.get("vertices"))
        self.vertex_collection = [
            Vertex(vertex) for vertex in self.data.get("vertices")
        ]

        edges = self.data.get("edges", None)
        if edges is None:

            for i in self.vertex_collection:
                for j in self.vertex_collection:
                    if i < j:
                        cost = self.calculate_distance(i, j)
                        self.add_edge(i, j, cost)
                        self.add_edge(j, i, cost)

    def get_random_path(self, size):
        random_paths = []
        list_vertices = list(self.vertices)

        for i in range(size):
            random_list = random.sample(list_vertices, len(list_vertices))
            random_paths.append(random_list)

        return random_paths

    def get_cost(self, path):
        total_cost = 0
        for i in range(self.number_vertices - 1):
            total_cost += self.edges[(path[i], path[i + 1])].cost

        total_cost += self.edges[(path[self.number_vertices - 1], path[0])].cost
        return total_cost

    def update_pheromone(self, edge, pheromone):
        self.edges[edge].pheromone = pheromone

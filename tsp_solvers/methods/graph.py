import random
from math import pow, sqrt

import matplotlib.pyplot as plt

plt.ioff()


class Edge:
    def __init__(self, origin, destination, cost, initial_pheromone=0):
        self.origin = origin
        self.destination = destination
        self.cost = cost
        self.pheromone = initial_pheromone


class Graph:
    def __init__(self, vertices):
        self.edges = dict()
        self.vertices = set()
        self.vertices_coordinates = dict()
        self.number_vertices = vertices
        self.x_coordinates = list()
        self.y_coordinates = list()

    def edge_exists(self, origin, destination):
        if (origin, destination) in self.edges.keys():
            return True
        else:
            return False

    def add_edge(self, origin, destination, cost=0.0):
        if not self.edge_exists(origin, destination):
            self.edges[(origin, destination)] = Edge(origin, destination, cost, 0)

    def calculate_distance(self, origin, destination):
        distance = sqrt(
            pow(
                self.vertices_coordinates[origin][0]
                - self.vertices_coordinates[destination][0],
                2,
            )
            + pow(
                self.vertices_coordinates[origin][1]
                - self.vertices_coordinates[destination][1],
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

    def random_complete_graph(self):

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

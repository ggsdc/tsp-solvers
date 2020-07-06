import random


class Edge:
    def __init__(self, origin, destination, cost, initial_pheromone=0):
        self.origin = origin
        self.destination = destination
        self.cost = cost
        self.pheromone = initial_pheromone


class Graph:
    def __init__(self, vertices):
        self.edges = {}
        self.vertices = set()
        self.number_vertices = vertices

    def edge_exists(self, origin, destination):
        if (origin, destination) in self.edges.keys():
            return True
        else:
            return False

    def add_edge(self, origin, destination, cost=0):
        if not self.edge_exists(origin, destination):
            self.edges[(origin, destination)] = Edge(origin, destination, cost, 0)
            self.vertices.add(origin)
            self.vertices.add(destination)

    def show(self):
        print('GRAPH:\n')
        for edge in self.edges:
            print('%d linked with %d with cost %d' % (edge[0], edge[1], self.edges[edge].cost))

    def random_complete_graph(self):
        for i in range(self.number_vertices):
            for j in range(self.number_vertices):
                if i < j:
                    cost = random.randint(1, 10)
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

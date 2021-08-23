import random


class RandomInitializer:
    def __init__(self, graph, population):
        self.graph = graph
        self.population = population

    def get_init(self):
        random_paths = []
        list_vertices = self.graph.vertices

        for _ in range(self.population):
            random_list = random.sample(list_vertices, len(list_vertices))
            random_paths.append(random_list)

        return random_paths

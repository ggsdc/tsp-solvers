import random


class NearestNeighbor:
    def __init__(self, graph, population):
        self.graph = graph
        self.population = population

    def get_init(self):
        random_paths = []
        list_vertices = self.graph.vertex_collection

        for _ in range(self.population):
            random_start = random.sample(list_vertices, 1)[0]
            aux_list = list(list_vertices)
            aux_list.remove(random_start)
            random_list = [random_start]
            while len(aux_list) > 0:
                min_dist = float("Inf")
                next_node = None
                for i in aux_list:
                    if self.graph.edges_cost[(random_list[-1].idx, i.idx)] < min_dist:
                        min_dist = self.graph.edges_cost[(random_list[-1].idx, i.idx)]
                        next_node = i

                random_list.append(next_node)
                aux_list.remove(next_node)

            random_paths.append(random_list)

        return random_paths

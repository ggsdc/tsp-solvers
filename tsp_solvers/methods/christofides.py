from tsp_solvers.methods.base import BaseMethod
from tsp_solvers.graph import Graph, Edge


class Christofides(BaseMethod):
    def __init__(self, graph, verbose=0):
        super().__init__()
        self.graph = graph
        self.verbose = verbose
        self.solution = None
        self.MST = None

    def run(self):
        # Calculate minimum spanning tree (MST)
        # Subset O vertices of odd degree
        # Subgraph with vertices O
        # Construct minim weight perfect matching M
        # Unite graphs
        # Calculate Euler tour
        # Fix euler tour
        self._get_minimum_spanning_tree()
        pass

    def _get_minimum_spanning_tree(self):
        # With Boruvka algorithm
        self.MST = Graph()
        self.MST.vertices = list(self.graph.vertices)
        self.MST.vertices_collection = dict(self.graph.vertices_collection)
        self.MST.number_vertices = len(self.MST.vertices)
        # self.MST.plot_edges()
        completed = False
        # First iteration
        for vertex in self.MST.vertices:
            rest = {
                other: self.MST.calculate_cost(vertex, other)
                for other in self.MST.vertices
                if other != vertex
            }

            nearest = min(rest, key=rest.get)

            self.MST.edges.append(
                Edge(
                    {
                        "origin": vertex,
                        "destination": nearest,
                        "cost": rest[nearest],
                    }
                )
            )
            self.MST.edges_collection[(vertex.idx, nearest.idx)] = self.MST.edges[-1]

        self.MST.calculate_components()
        print(self.MST.components_groups)
        print("OK")
        if len(self.MST.components_groups) == 1:
            completed = True

        self.MST.plot_edges()

        while not completed:

            # Function to check if we have only one component to exit loop

            for group1 in self.MST.components_groups:
                rest = {}
                for group2 in self.MST.components_groups:
                    if group1 != group2:
                        for origin in group1:
                            for destination in group2:
                                rest[origin, destination] = self.MST.calculate_cost(
                                    origin, destination
                                )

                nearest = min(rest, key=rest.get)

                self.MST.edges.append(
                    Edge(
                        {
                            "origin": nearest[0],
                            "destination": nearest[1],
                            "cost": rest[nearest],
                        }
                    )
                )

                print(nearest)

                self.MST.edges_collection[
                    (nearest[0].idx, nearest[1].idx)
                ] = self.MST.edges[-1]

            self.MST.plot_edges()
            self.MST.calculate_components()
            print(self.MST.components_groups)
            print("OK")
            if len(self.MST.components_groups) == 1:
                completed = True

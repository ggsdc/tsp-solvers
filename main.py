def main():
    from tsp_solvers import Graph, GeneticAlgorithm

    g = Graph()
    g.create_graph_from_json("./data/100_vertex_random_graph.json")
    ga = GeneticAlgorithm(g, 200, 100, 0.1, 120, "nearest")
    ga.run()
    ga.get_best()


if __name__ == "__main__":
    main()
    pass

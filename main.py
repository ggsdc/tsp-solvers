def main():
    from tsp_solvers import Graph, GeneticAlgorithm

    g = Graph()
    g.create_graph_from_json("./data/100_vertex_random_graph.json")
    # g.random_complete_graph(100)
    ga = GeneticAlgorithm(g, 200, 100, 0.1, 120, "nearest")
    ga.run()
    ga.get_best()


if __name__ == "__main__":
    import cProfile
    import pstats

    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename="times.prof")

import random


def main():
    from tsp_solvers import (
        Graph,
        GeneticAlgorithm,
        AntColonyOptimization,
        LinearIntegerProgram,
        Christofides,
    )

    random.seed(123)
    g = Graph()
    # g.create_graph_from_json("./data/100_vertex_random_graph.json")
    # g.create_graph_from_tsp("./data/dj38.tsp")
    g.random_complete_graph(13)
    c = Christofides(g)
    c.run()

    # g.save_graph_to_json("./tsp_solvers/tests/data/10v.json")
    # ga = GeneticAlgorithm(g, 200, 10, 0.1, 120, "nearest", verbose=True)
    # ga.run()
    # ga.get_best()
    #
    # aco = AntColonyOptimization("AS", g, 100, 10)
    # aco.run()
    # aco.get_best()
    #
    # lp = LinearIntegerProgram(g, 120)
    # lp.build_model()
    # lp.run()


if __name__ == "__main__":
    import cProfile
    import pstats

    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename="times.prof")

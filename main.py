import random


def main():
    from tsp_solvers import (
        Graph,
        GeneticAlgorithm,
        AntColonyOptimization,
        LinearIntegerProgram,
        TwoOpt,
    )


    g = Graph()
    # g.create_graph_from_json("./data/100_vertex_random_graph.json")
    # g.create_graph_from_tsp("./data/dj38.tsp")

    g.random_complete_graph(10)
    # g.save_graph_to_json("./tsp_solvers/tests/data/10v.json")
    ga = GeneticAlgorithm(g, 1000, 100, 0.2, 120, "random", verbose=True)
    ga.run()
    ga.get_best()

    aco = AntColonyOptimization("AS", g, 400, 10, max_time=120, plot=True)
    aco.run()
    aco.get_best()

    lp = LinearIntegerProgram(g, 120)
    lp.build_model()
    lp.run()

    tw = TwoOpt(g, 120, "nearest")
    tw.run()
    tw.get_best()


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

from tsp_solvers import (
    Graph,
    GeneticAlgorithm,
    AntColonyOptimization,
    TwoOpt,
    ThreeOpt,
    SimulatedAnnealingTwoOpt,
    SimulatedAnnealingThreeOpt,
    LinearIntegerProgram,
)
from tsp_solvers.methods.dynamic_programming import DynamicProgramming
from tsp_solvers.methods.lp_dantzig import LinearIntegerDantzig


def main():
    nodes = 25
    g = Graph()
    # g.create_graph_from_json("./tsp_solvers/data/250v_3.json")
    # g.create_graph_from_tsp("./data/dj38.tsp")
    g.random_complete_graph(nodes)
    # g.save_graph_to_json("./tsp_solvers/tests/data/10v.json")
    ga = GeneticAlgorithm(
        g, nodes * 100, 10, 0.2, 120, "random", verbose=True, plot=True
    )
    ga.run()
    ga.get_best()

    aco = AntColonyOptimization(
        "AS", g, nodes * 100, int(nodes * 1 / 2), max_time=120, plot=True, verbose=True
    )
    aco.run()
    aco.get_best()

    lp = LinearIntegerDantzig(g, 120, plot=False)
    lp.build_model()
    lp.run()
    lp.get_best()

    lp_1 = LinearIntegerProgram(g, 10, plot=True)
    lp_1.build_model()
    lp_1.run()
    lp_1.get_best()

    tw = TwoOpt(g, 120, "random", plot=True)
    tw.run()
    tw.get_best()

    sa_tw = SimulatedAnnealingTwoOpt(g, 300, "random", plot=True)
    sa_tw.run()
    sa_tw.get_best()

    th = ThreeOpt(g, 120, "random", plot=True)
    th.run()
    th.get_best()

    sa_th = SimulatedAnnealingThreeOpt(g, 600, "random", plot=True)
    sa_th.run()
    sa_th.get_best()


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

from tsp_solvers import (
    Graph,
    SimulatedAnnealingTwoOpt,
    SimulatedAnnealingThreeOpt,
    TwoOpt,
    ThreeOpt,
    GeneticAlgorithm,
    AntColonyOptimization,
)

file = "./results-aco.csv"


def get_optimal_values():
    combinations = {
        # 10: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        # 25: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        # 50: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        100: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        150: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        200: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        250: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    }

    for node, instances in combinations.items():
        for i in instances:
            g = Graph()
            g.create_graph_from_json(f"./tsp_solvers/data/{node}v_{i}.json")

            al = AntColonyOptimization(
                "AS", g, node * 50, int(node * 1 / 2), max_time=1800, plot=False
            )

            al.run()
            print(
                f"{node},{i},{al.get_solution_value()},"
                f"{al.get_solution_time().seconds + al.get_solution_time().microseconds/1000000}"
            )

            with open(file, "a") as f:
                f.write(
                    f"{node},{i},{al.get_solution_value()},"
                    f"{al.get_solution_time().seconds + al.get_solution_time().microseconds/1000000}\n"
                )


if __name__ == "__main__":
    get_optimal_values()

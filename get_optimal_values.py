from tsp_solvers import Graph, LinearIntegerProgram
from tsp_solvers.methods.lp_dantzig import LinearIntegerDantzig

file = "./results.csv"


def get_optimal_values():
    combinations = {250: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}

    for node, instances in combinations.items():
        for i in instances:
            g = Graph()
            g.create_graph_from_json(f"./tsp_solvers/data/{node}v_{i}.json")

            lp = LinearIntegerDantzig(g, 1800)
            lp.build_model()
            lp.run()
            print(
                f"{node},{i},{lp.get_solution_value()},"
                f"{lp.get_solution_time().seconds + lp.get_solution_time().microseconds / 1000000}"
            )

            with open(file, "a") as f:
                f.write(
                    f"{node},{i},{lp.get_solution_value()},"
                    f"{lp.get_solution_time().seconds + lp.get_solution_time().microseconds / 1000000}\n"
                )


if __name__ == "__main__":
    get_optimal_values()

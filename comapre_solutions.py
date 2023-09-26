from tsp_solvers import Graph, LinearIntegerProgram
from tsp_solvers.methods.lp_dantzig import LinearIntegerDantzig


def compare_solutions():
    g = Graph()
    g.create_graph_from_json("./tsp_solvers/data/25v_2.json")

    dantz = LinearIntegerDantzig(g, 120, plot=True)
    dantz.build_model()
    dantz.run()
    print(
        f"Dantzig ({dantz.get_solution_value()}): {[vertex.idx for vertex in dantz.solution]}"
    )

    miller = LinearIntegerProgram(g, 120, plot=True)
    miller.build_model()
    miller.run()
    print(
        f"Miller ({miller.get_solution_value()}): {[vertex.idx for vertex in miller.solution]}"
    )


if __name__ == "__main__":
    compare_solutions()

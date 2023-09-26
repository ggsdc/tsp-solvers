from tsp_solvers import Graph


def generate_instances(n: int = 10, nodes: list = [10, 25, 50, 100, 150, 200, 250]):
    for node in nodes:
        for i in range(n):
            g = Graph()
            g.random_complete_graph(node)
            g.save_graph_to_json(f"./tsp_solvers/data/{node}v_{i}.json")
            print(f"Generated {node}v_{i}.json")


if __name__ == "__main__":
    generate_instances()

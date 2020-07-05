from src.graph import Graph
from src.pso import PSO
from src.aco import ACO
from src.ga import GA
from src.lp import LP
import datetime
#
sizes = [5, 10, 25, 50, 75, 100, 150, 200, 250, 500, 750, 1000]
times = [3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600]


for i in range(len(sizes)):
    size = sizes[i]
    max_time = times[i]

    graph = Graph(size)
    graph.random_complete_graph()
    # graph.show()
    #
    pso = PSO(graph, iterations=500, size_population=50, alpha=0.9, beta=1, max_time=max_time)
    t1 = datetime.datetime.utcnow()
    pso.run()
    t2 = datetime.datetime.utcnow()

    acs = ACO(graph=graph, iterations=500, population_size=50, max_time=max_time)
    t3 = datetime.datetime.utcnow()
    acs.run()
    t4 = datetime.datetime.utcnow()

    ga = GA(graph=graph, max_generations=500, population_size=50, mutation_probability=0.1, max_time=max_time)
    t5 = datetime.datetime.utcnow()
    ga.run()
    t6 = datetime.datetime.utcnow()

    t7 = datetime.datetime.utcnow()
    lp = LP(graph=graph, max_time=max_time)
    lp.build_model()
    lp.run()
    t8 = datetime.datetime.utcnow()

    print('PSO time: ', t2 - t1)
    print('ACO time: ', t4 - t3)
    print('GA time: ', t6 - t5)
    print('LP time: ', t8 - t7)

    # pso.get_best()
    # acs.get_best()
    # ga.get_best()
    # lp.show()

    file = 'results-2.txt'
    text = 'Graph: ' + str(size) + ' nodes\n'
    with open('results.txt', "a") as myfile:
        myfile.write('-----------------------------\n')
        myfile.write(text)
        myfile.close()

    pso.save(file)
    acs.save(file)
    ga.save(file)
    lp.save(file)
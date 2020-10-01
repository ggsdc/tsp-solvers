from src.methods import ACO, GA, Graph, LP, PSO
import datetime

sizes = [5, 10, 25, 50, 75, 100, 150, 200, 250, 500, 750, 1000]
times = [3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600]
iterations = [1000, 1000, 1000, 1000, 1000, 1000, 2000, 2000, 2000, 3000, 3000, 3000]
population = [10, 10, 10, 10, 10, 10, 25, 25, 25, 50, 50, 50]

# sizes = [15]
# times = [3600]
# iterations = [1000]
# population = [10]

for i in range(len(sizes)):
    size = sizes[i]
    max_time = times[i]
    num_iterations = iterations[i]
    population_size = population[i]

    graph = Graph(size)
    graph.random_complete_graph()
    # graph.plot()
    # graph.show()

    # pso = PSO(graph, iterations=num_iterations, size_population=population_size, alpha=0.7, beta=0.7, max_time=max_time)
    # t1 = datetime.datetime.utcnow()
    # pso.run()
    # t2 = datetime.datetime.utcnow()
    #
    # acs = ACO(graph=graph, iterations=num_iterations, population_size=population_size, max_time=max_time)
    # t3 = datetime.datetime.utcnow()
    # acs.run()
    # t4 = datetime.datetime.utcnow()

    ga = GA(graph=graph, max_generations=num_iterations, population_size=population_size, mutation_probability=0.1,
            init="nearest", max_time=max_time)
    t5 = datetime.datetime.utcnow()
    ga.run()
    t6 = datetime.datetime.utcnow()

    t7 = datetime.datetime.utcnow()
    lp = LP(graph=graph, max_time=max_time)
    lp.build_model()
    lp.run()
    t8 = datetime.datetime.utcnow()

    # print('PSO time: ', t2 - t1)
    # print('ACO time: ', t4 - t3)
    # print('GA time: ', t6 - t5)
    # print('LP time: ', t8 - t7)
    #
    # pso.get_best()
    # acs.get_best()
    ga.get_best()
    lp.show()
    #
    # file = 'test.txt'
    # text = 'Graph: ' + str(size) + ' nodes\n'
    # with open(file, "a") as myfile:
    #     myfile.write('-----------------------------\n')
    #     myfile.write(text)
    #     myfile.close()
    #
    # pso.save(file)
    # acs.save(file)
    # ga.save(file)
    # lp.save(file)

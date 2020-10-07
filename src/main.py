from src.methods import ACO, GA, Graph, LP, PSO, TwoOpt
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

    pso = PSO(graph, iterations=num_iterations, population_size=population_size, alpha=0.7, beta=0.7, max_time=max_time,
              init="nearest")
    pso.run()

    acs = ACO(graph=graph, iterations=num_iterations, population_size=population_size, max_time=max_time)
    acs.run()

    ga = GA(graph=graph, max_generations=num_iterations, population_size=population_size, mutation_probability=0.1,
            init="nearest", max_time=max_time)
    ga.run()

    lp = LP(graph=graph, max_time=max_time)
    lp.build_model()
    lp.run()

    two_opt = TwoOpt(graph, max_time=max_time, init="random")
    two_opt.run()

    print('PSO time: ', pso.get_time())
    print('ACO time: ', acs.get_time())
    print('GA time: ', ga.get_time())
    print('LP time: ', lp.get_time())
    print('Two opt time: ', two_opt.get_time())
    pso.get_best()
    acs.get_best()
    ga.get_best()
    lp.show()
    two_opt.get_best()

    file = 'test.txt'
    text = 'Graph: ' + str(size) + ' nodes\n'
    with open(file, "a") as myfile:
        myfile.write('-----------------------------\n')
        myfile.write(text)
        myfile.close()

    pso.save(file)
    acs.save(file)
    ga.save(file)
    lp.save(file)
    two_opt.save(file)

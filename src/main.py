from src.graph import Graph
from src.pso import PSO
from src.aco import ACO
from src.ga import GA
import datetime

graph = Graph(100)
graph.random_complete_graph()
# graph.show()

pso = PSO(graph, iterations=1000, size_population=100, alpha=0.9, beta=1)
t1 = datetime.datetime.utcnow()
pso.run()
t2 = datetime.datetime.utcnow()

acs = ACO(graph=graph, iterations=1000, population_size=100)
t3 = datetime.datetime.utcnow()
acs.run()
t4 = datetime.datetime.utcnow()

ga = GA(graph=graph, max_generations=1000, population_size=100, mutation_probability=0.1)
t5 = datetime.datetime.utcnow()
ga.run()
t6 = datetime.datetime.utcnow()

print('PSO time: ', t2 - t1)
print('ACO time: ', t4 - t3)
print('GA tine: ', t6 - t5)

pso.get_best()
acs.get_best()
ga.get_best()

pso.show()
acs.show()
ga.show()

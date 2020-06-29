from src.graph import Graph
from src.pso import PSO
from src.aco import ACO
from src.ga import GA
from src.lp import LP
import datetime

graph = Graph(150)
graph.random_complete_graph()
# graph.show()
#
pso = PSO(graph, iterations=100, size_population=10, alpha=0.9, beta=1)
t1 = datetime.datetime.utcnow()
pso.run()
t2 = datetime.datetime.utcnow()

acs = ACO(graph=graph, iterations=100, population_size=10)
t3 = datetime.datetime.utcnow()
acs.run()
t4 = datetime.datetime.utcnow()

ga = GA(graph=graph, max_generations=100, population_size=10, mutation_probability=0.1)
t5 = datetime.datetime.utcnow()
ga.run()
t6 = datetime.datetime.utcnow()

t7 = datetime.datetime.utcnow()
lp = LP(graph=graph, max_time=60)
lp.build_model()
lp.run()
t8 = datetime.datetime.utcnow()

print('PSO time: ', t2 - t1)
print('ACO time: ', t4 - t3)
print('GA time: ', t6 - t5)
print('LP time: ', t8 - t7)
#
pso.get_best()
acs.get_best()
ga.get_best()
#
# pso.show()
# acs.show()
# ga.show()
lp.show()



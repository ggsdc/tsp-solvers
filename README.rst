TSP solvers
-------------

This library has a number of solvers for the TSP problem.
To be able to implement the solvers we have also implemented a Graph class that allows to store the data for the problem.

The graph can be initialized from a json file, randomly or from tsplib files.

The current full methods implemented to solve the TSP are:

- Ant Colony Optimization (ACO) in the AS mode.
- Genetic Algorithm (GA).
- Linear programming with the Miller-Tucker-Zemlin formulation (MTZ).
- Linear programming with the Dantzig-Fulkerson-Johnson formulation (DFJ).
- Particle Swarm Optimization (PSO).
- Three-opt local search.
- Three-opt local search with simulated annealing.
- Two-opt local search.
- Two-opt local search with simulated annealing.

Currently there are other methods that are not yet completed or published, but are in the works to get solutions from them as well:

- Christofides algorithm.
- Dynamic programming.
- Held-Karp algorithm.
- Self-organizing maps (SOM).
- Simulated annealing.

The library also comes with a set of examples (in json format) having ten instances for problems with 10, 25, 50, 100, 150, 200 and 250 nodes.

A future benchmark module will be available to compare properly all the different methods that are implemented in the library and get which methods are able to get the best solutions in the same time.

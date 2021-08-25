import copy
import datetime
import random
import sys
from ..initializers import NearestNeighbor, RandomInitializer


class Particle:
    def __init__(self, solution, cost):
        self.solution = solution
        self.cost = cost
        self.best_solution = solution
        self.best_cost = cost

        self.velocity = []

    def reset_velocity(self):
        del self.velocity[:]


class ParticleSwarmOptimization:
    def __init__(
        self,
        graph,
        iterations,
        population_size,
        alpha=1,
        beta=1,
        max_time=60,
        init="random",
        plot=False,
    ):
        self.graph = graph
        self.iterations = iterations
        self.population_size = population_size
        self.alpha = alpha
        self.beta = beta
        self.particles = list()
        self.best = None
        self.max_time = max_time
        self.time = None
        self.plot = plot
        if self.plot:
            if "matplotlib" not in sys.modules:
                raise ModuleNotFoundError(
                    "Matplotlib has to be installed to be able to plot!"
                )
        self.init = init
        self.initializer = None

        if self.init == "random":
            self.initializer = RandomInitializer(self.graph, self.population_size)
        elif self.init == "nearest":
            self.initializer = NearestNeighbor(self.graph, self.population_size)

        solutions = self.initializer.get_init()

        for solution in solutions:
            particle = Particle(
                solution=solution, cost=graph.get_solution_cost(solution)
            )
            self.particles.append(particle)

        self.size_population = len(self.particles)

    def get_best(self):
        best = self.particles[0]
        for particle in self.particles:
            if particle.cost < best.cost:
                best = particle
        print("\nPSO:")
        print("Best solution: ", str(best.solution), "\t|\tcost: ", str(best.cost))

    def show(self):
        print("\nSOLUTION:")
        print(
            "Particles: "
            + str(self.size_population)
            + ". Iterations: "
            + str(self.iterations)
        )
        for particle in self.particles:
            print(
                "Best solution: %s\t|\tcost: %d"
                % (str(particle.best_solution), particle.best_cost)
            )

    def evaluate(self):
        costs = [i.cost for i in self.particles]
        mean_cost = sum(costs) / len(costs)
        min_cost = min(costs)

        if min_cost * 1.01 > mean_cost:
            print("BREAK")
            return True
        else:
            return False

    def run(self):
        start = datetime.datetime.utcnow()
        frac = 0.1
        plot_interval = [10 * x for x in range(1, self.iterations // 10 + 1)]
        initial_time = datetime.datetime.utcnow()

        for i in range(self.iterations):
            if i / self.iterations >= frac:
                print("Iteration ", str(i), " of ", str(self.iterations))
                frac += 0.1

            if i >= self.iterations // 5:
                if self.evaluate():
                    break

            self.best = min(self.particles, key=lambda p: p.best_cost)

            for particle in self.particles:
                particle.reset_velocity()
                temp_velocity = []
                best_population = copy.copy(self.best.best_solution)
                best_particle = particle.best_solution
                solution_particle = particle.solution

                for v in range(self.graph.number_vertices):
                    if solution_particle[v] != best_particle[v]:
                        swap = (
                            v,
                            best_particle.index(solution_particle[v]),
                            self.alpha,
                        )

                        temp_velocity.append(swap)

                        aux = best_particle[swap[0]]
                        best_particle[swap[0]] = best_particle[swap[1]]
                        best_particle[swap[1]] = aux

                for v in range(self.graph.number_vertices):
                    if solution_particle[v] != best_population[v]:
                        swap = (
                            v,
                            best_population.index(solution_particle[v]),
                            self.beta,
                        )

                        temp_velocity.append(swap)

                        aux = best_population[swap[0]]
                        best_population[swap[0]] = best_population[swap[1]]
                        best_population[swap[1]] = aux

                particle.velocity = temp_velocity

                for w in temp_velocity:
                    if random.random() <= w[2]:
                        aux = solution_particle[w[0]]
                        solution_particle[w[0]] = solution_particle[w[1]]
                        solution_particle[w[1]] = aux

                particle.solution = solution_particle

                current_cost = self.graph.get_solution_cost(solution_particle)
                particle.cost = current_cost

                if current_cost < particle.best_cost:
                    particle.best_cost = current_cost
                    particle.best_solution = solution_particle

            if self.plot:
                if (i + 1) in plot_interval:
                    filename = (
                        "plots/pso_"
                        + str(self.graph.number_vertices)
                        + "_"
                        + str(i + 1)
                        + ".png"
                    )
                    title = (
                        "Particle Swarm Optimization. Iteration "
                        + str(i + 1)
                        + "\n Solution cost: "
                        + str(round(particle.best_cost, 2))
                    )
                    self.graph.plot_solution(
                        particle.best_solution, filename=filename, title=title
                    )

            if (datetime.datetime.utcnow() - initial_time).seconds > self.max_time:
                break

        self.time = datetime.datetime.utcnow() - start

    def save(self, file):
        best = self.particles[0]
        for particle in self.particles:
            if particle.cost < best.cost:
                best = particle
        text = (
            "PSO. Best solution: "
            + str(best.solution)
            + "\t|\tCost: "
            + str(best.cost)
            + "\n"
        )
        with open(file, "a") as myfile:
            myfile.write(text)

    def get_time(self):
        return self.time

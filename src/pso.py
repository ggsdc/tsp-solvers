import random
import copy


class Particle:

    def __init__(self, solution, cost):
        self.solution = solution
        self.cost = cost
        self.best_solution = solution
        self.best_cost = cost

        self.velocity = []

    def reset_velocity(self):
        del self.velocity[:]


class PSO:
    def __init__(self, graph, iterations, size_population, alpha=1, beta=1):
        self.graph = graph
        self.iterations = iterations
        self.size_population = size_population
        self.alpha = alpha
        self.beta = beta
        self.particles = list()
        self.best = None

        solutions = self.graph.get_random_path(self.size_population)

        for solution in solutions:
            particle = Particle(solution=solution, cost=graph.get_cost(solution))
            self.particles.append(particle)

        self.size_population = len(self.particles)

    def get_best(self):
        best = self.particles[0]
        for particle in self.particles:
            if particle.cost < best.cost:
                best = particle

        print('BEST SOLUTION: ', str(best.solution), ". Cost: ", str(best.cost))

    def show(self):
        print("\nSOLUTION:")
        print("Particles: " + str(self.size_population) + ". Iterations: " + str(self.iterations))
        for particle in self.particles:
            print('Best solution: %s\t|\tcost: %d' % (str(particle.best_solution), particle.best_cost))

    def run(self):

        frac = 0.1

        for i in range(self.iterations):
            if i / self.iterations >= frac:
                print(str(frac*100) + '% iterations complete')
                frac += 0.1

            self.best = min(self.particles, key=lambda p: p.best_cost)

            for particle in self.particles:
                particle.reset_velocity()
                temp_velocity = []
                best_population = copy.copy(self.best.best_solution)
                best_particle = particle.best_solution
                solution_particle = particle.solution

                for v in range(self.graph.number_vertices):
                    if solution_particle[v] != best_particle[v]:
                        swap = (v, best_particle.index(solution_particle[v]), self.alpha)

                        temp_velocity.append(swap)

                        aux = best_particle[swap[0]]
                        best_particle[swap[0]] = best_particle[swap[1]]
                        best_particle[swap[1]] = aux

                for v in range(self.graph.number_vertices):
                    if solution_particle[v] != best_population[v]:
                        swap = (v, best_population.index(solution_particle[v]), self.beta)

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

                current_cost = self.graph.get_cost(solution_particle)
                particle.cost = current_cost

                if current_cost < particle.best_cost:
                    particle.best_cost = current_cost
                    particle.best_solution = solution_particle

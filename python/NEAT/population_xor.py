from .genome_history import *
from .genome import *

import random


class Population:
    def __init__(self, gh, pop_size, agent) -> None:
        self.pop_size = pop_size

        self.population = []
        for _ in range(pop_size):
            self.population.append(agent(gh))

        self.gh = gh
        self.best_fitness = 0.0


    def reset(self):
        parents = self.population

        parents.sort(key=lambda x: x.fitness, reverse=True)

        self.population = []

        for i in range(self.pop_size):
            parent1 = parents[random.randint(0, len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]
            agent = parent1.mate(parent2)
            agent.brian.mutate()
            self.population.append(agent)

        self.best_fitness = 0.0

    def reset_2(self):
        parents = sorted(self.population, key=lambda x: x.fitness, reverse=True)

        self.population = []

        elite_count = 5
        self.population.extend(parents[:elite_count])

        fitnesses = [p.fitness for p in parents]
        fitness_sum = sum(fitnesses)

        def select_weighted():
            r = random.uniform(0, fitness_sum)
            running = 0
            for p in parents:
                running += p.fitness
                if running >= r:
                    return p
            return parents[0]

    def update(self, inputs):
        best_agent = self.population[0]
        for agent in self.population:
            
            fitness = agent.calculate_fitness(inputs)
                
            if (fitness > self.best_fitness):
                self.best_fitness = fitness
                best_agent = agent

        return best_agent
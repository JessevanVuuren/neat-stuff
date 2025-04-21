from .genome_history import *
from .genome import *

import random


class Population:
    def __init__(self, gh, pop_size, agent) -> None:
        self.pop_size = pop_size
        self.population = []
        self.gh = gh

        for _ in range(pop_size):
            self.population.append(agent(gh))

        self.best_local = self.population[0]
        self.best_global = self.population[0]

    def reset(self):
        parents = self.population

        parents.sort(key=lambda x: x.fitness, reverse=True)

        self.population = []

        for i in range(self.pop_size):
            parent1 = parents[random.randint(0, len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]
            agent = parent1.mate(parent2)
            agent.brain.mutate()
            self.population.append(agent)

        self.best_local = self.population[0]

    def all_dead(self):

        for agent in self.population:
            if not agent.dead:
                return False

        return True

    def draw(self):
        for agent in self.population:
            agent.draw()

    def update(self, inputs, dt):
        for agent in self.population:

            agent.update(inputs, dt)
            fitness = agent.fitness

            if (fitness > self.best_local.fitness):
                
                self.best_fitness = agent

            if (fitness > self.best_global.fitness):
                self.best_global = agent

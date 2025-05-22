from __future__ import annotations

from .genome_history import GenomeHistory
from collections.abc import Callable
from .genome import Genome

import random


class Population:
    def __init__(self, gh: GenomeHistory, pop_size: int) -> None:

        self.pop_size = pop_size
        self.generation = 0
        self.population: list[Genome] = []
        self.gh = gh

        for _ in range(self.pop_size):
            genome = Genome(self.gh)
            genome.mutate()
            self.population.append(genome)

        self.best_local = self.population[0]
        self.best_global = self.population[0]

    def reset(self):
        self.generation += 1

        parents = self.population.copy()
        self.population.clear()

        parents.sort(key=lambda x: x.fitness, reverse=True)

        for _ in range(self.pop_size):
            parent1 = parents[random.randint(0, len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]

            child = parent1.crossover(parent2)
            child.mutate()

            self.population.append(child)

        self.population[0] = parents[0].clone()

    def run(self, fitness_function: Callable[[list[Genome]], None], n: int = 0):


        while self.generation < n or n == 0:

            fitness_function(self.population)

            self.best_local = self.population[0]
            for genome in self.population:
                if (genome.fitness > self.best_local.fitness):
                    self.best_local = genome.clone()

            if (self.best_local.fitness > self.best_global.fitness):
                self.best_global = self.best_local.clone()

            print("Local Fitness: ", self.best_local.fitness)
            print("Global Fitness: ", self.best_global.fitness)
            print()
            self.reset()
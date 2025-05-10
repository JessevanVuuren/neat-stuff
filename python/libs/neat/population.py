from __future__ import annotations
from collections.abc import Callable

from .genome import Genome
from .genome_history import GenomeHistory


import random


class Population:
    def __init__(self, gh: GenomeHistory, pop_size: int) -> None:

        self.pop_size = pop_size
        self.generation = 0
        self.population: list[Genome] = []
        self.gh = gh

        for _ in range(self.pop_size):
            genome = Genome(self.gh)
            [genome.mutate() for _ in range(10)]
            self.population.append(genome)

        self.best_local = self.population[0]
        self.best_global = self.population[0]

    def reset(self):
        self.generation += 1

        parents = self.population
        self.population = []

        parents.sort(key=lambda x: x.fitness, reverse=True)

        for _ in range(self.pop_size):
            parent1 = parents[random.randint(0, len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]

            child = parent1.crossover(parent2)
            child.mutate()

            self.population.append(child)

    def run(self, fitness_function: Callable[[list[Genome]], None], n: int = 0):

        if (n == 0):
            raise RuntimeError("n cannot, (yet!) be zero")

        for _ in range(n):
            fitness_function(self.population)

            self.best_local = self.population[0]
            for genome in self.population:
                if (genome.fitness > self.best_local.fitness):
                    self.best_local = genome

            if (self.best_local.fitness > self.best_global.fitness):
                self.best_global = self.best_local

            print("Local Fitness: ", self.best_local.fitness)
            print("Global Fitness: ", self.best_global.fitness)
            print()
            self.reset()

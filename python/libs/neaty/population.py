from __future__ import annotations

from .genome_history import GenomeHistory
from collections.abc import Callable
from .genome import Genome

import random
import time


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

        self.population[0] = self.best_global.clone()
        self.population[1] = parents[0].clone()
        self.population[2] = parents[1].clone()

    def run(self, fitness_function: Callable[[list[Genome]], None], n: int = 0, report: bool = False):

        while self.generation < n or n == 0:

            fitness_function(self.population)

            self.best_local = self.population[0]
            for genome in self.population:
                if (genome.fitness > self.best_local.fitness):
                    self.best_local = genome.clone()

            if (self.best_local.fitness > self.best_global.fitness):
                self.best_global = self.best_local.clone()

            start = time.perf_counter()
            self.reset()
            stop = time.perf_counter()

            if (report):
                self.report(stop - start)

    def report(self, execution_time: float):
        print(f"=== [Generation: {self.generation}] ===")
        print(f"Reset time: {execution_time:.4f}ms")
        print(f"Local Fitness: {self.best_local.fitness:.6f}")
        print(f"Global Fitness: {self.best_global.fitness:.6f}")
        print(f"Genes history: {len(self.gh.all_genes)}")
        self.best_global.info()
        print()

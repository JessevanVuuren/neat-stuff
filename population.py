from concurrent.futures import ThreadPoolExecutor, as_completed
from NEAT.genome_history import *
from agent import XORsolver
from NEAT.genome import *

import random
import time

class Population:
    def __init__(self, gh, pop_size) -> None:
        self.pop_size = pop_size

        self.population = []
        for _ in range(pop_size):
            self.population.append(XORsolver(gh))

        self.gh = gh
        self.best_fitness = 0.0

    def _create_offspring(self, parents):
        parent1 = parents[random.randint(0, len(parents) // 10)]
        parent2 = parents[random.randint(0, len(parents) // 10)]
        xor = parent1.mate(parent2)
        xor.brian.mutate()
        return xor

    def reset_thread(self):
        parents = self.population

        parents.sort(key=lambda x: x.fitness, reverse=True)

        with ThreadPoolExecutor() as executor:
            
            futures = []
            for off in self.population:
                futures.append(executor.submit(self._create_offspring, parents))
            
            self.population = []
            for future in as_completed(futures):
                self.population.append(future.result())
        self.best_fitness = 0.0


    def reset(self):
        parents = self.population

        parents.sort(key=lambda x: x.fitness, reverse=True)

        self.population = []

        for i in range(self.pop_size):
            parent1 = parents[random.randint(0, len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]
            xor = parent1.mate(parent2)
            xor.brian.mutate()
            self.population.append(xor)

        self.best_fitness = 0.0


    def update(self, xor_inputs):
        best_xor = self.population[0]
        for xor in self.population:
            start = time.time()
            total_error = 0
            for inputs, expected in xor_inputs:
                out = xor.predict(inputs)
                total_error += (out[0] - expected) ** 2

            xor.fitness = 1 / (total_error + 1e-6)

            if (xor.fitness > self.best_fitness):
                self.best_fitness = xor.fitness
                best_xor = xor

        return best_xor

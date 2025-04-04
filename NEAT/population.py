from genome_history import *
from genome import *

import concurrent.futures
import random
import time


class XORsolver:
    def __init__(self, gh) -> None:
        self.gh = gh
        self.fitness = 0.0

        self.brian = Genome(gh)
        for _ in range(10):
            self.brian.mutate()

    def mate(self, partner):
        xor = XORsolver(self.gh)
        xor.brian = self.brian.crossover(partner.brian)
        return xor

    def predict(self, inputs):
        out = self.brian.get_outputs(inputs)
        return out


class Population:
    def __init__(self, gh, pop_size) -> None:
        self.pop_size = pop_size

        self.population: list[XORsolver] = []
        for _ in range(pop_size):
            self.population.append(XORsolver(gh))

        self.gh = gh
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

            print("TIME:", time.time() - start)

        return best_xor

    def calculate_fitness(self, xor, xor_inputs):

        total_error = 0
        for inputs, expected in xor_inputs:
            out = xor.predict(inputs)
            total_error += (out[0] - expected) ** 2

        xor.fitness = 1 / (total_error + 1e-6)
        return xor

    def update_thread(self, xor_inputs):
        best_xor = self.population[0]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for xor in self.population:
                futures.append(executor.submit(self.calculate_fitness, xor, xor_inputs))
            for future in concurrent.futures.as_completed(futures):
                xor = future.result()
                if (xor.fitness > self.best_fitness):
                    self.best_fitness = xor.fitness
                    best_xor = xor

        return best_xor

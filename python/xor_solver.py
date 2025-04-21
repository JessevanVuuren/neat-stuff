from NEAT.population_xor import *
from NEAT.genome_history import *
from NEAT.genome import *

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

    def calculate_fitness(self, inputs):
        total_error = 4
        for xor, expected in inputs:
            out = self.predict(xor)
            total_error -= (out[0] - expected) ** 2

        self.fitness = total_error
        return self.fitness

    def predict(self, inputs):
        out = self.brian.get_outputs(inputs)
        return out


genome_history = GenomeHistory(3, 1)

xor = [
    ([0, 0, 1], 0),
    ([0, 1, 1], 1),
    ([1, 0, 1], 1),
    ([1, 1, 1], 0)
]

pop = Population(genome_history, 100, XORsolver)
best = -1

start = time.time()
for i in range(1000):

    best_xor = pop.update(xor)

    if (pop.best_fitness > best):
        best = pop.best_fitness
        print()
        print("Gen:", i, "Fitness:", pop.best_fitness)
        for inputs, expected in xor:
            out = best_xor.predict(inputs)
            print(f"{inputs[0]} - {inputs[1]} => {out}, expected: {expected}, fit: {(out[0] - expected) ** 2}")
        print()
    else:
        print("Gen:", i, "Fitness:", pop.best_fitness)

    pop.reset()


print("Time: ", time.time() - start)

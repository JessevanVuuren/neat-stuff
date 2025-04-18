from NEAT.genome_history import *
from NEAT.population import *
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
        total_error = 0
        for inputs, expected in inputs:
            out = self.predict(inputs)
            total_error += (out[0] - expected) ** 2

        self.fitness = 1 / (total_error + 1e-6)
        return self.fitness

    def predict(self, inputs):
        out = self.brian.get_outputs(inputs)
        return out
    



genome_history = GenomeHistory(2, 1)

xor = [
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 0)
]


pop = Population(genome_history, 100, XORsolver)
best = -1

start = time.time()
for i in range(100):

    best_xor = pop.update(xor)

    if (pop.best_fitness > best):
        best = pop.best_fitness
        print()
        print("Gen:",i, "Fitness:", pop.best_fitness)
        for inputs, expected in xor:
            out = best_xor.predict(inputs)
            print(f"{inputs[0]} - {inputs[1]} => {out}, expected: {expected}, fit: {(out[0] - expected) ** 2}")
        print()
    else:
        print("Gen:",i, "Fitness:", pop.best_fitness)

    pop.reset()


print("Time: ", time.time() - start)





# 4.960271407454573
# 0 - 0 => [0.5643580563571999], expected: 0, fit: 0.3185000157752765
# 0 - 1 => [0.7859887360215381], expected: 1, fit: 0.04580082110965892
# 1 - 0 => [0.8870810501881524], expected: 1, fit: 0.012750689226610552
# 1 - 1 => [0.2448815134805575], expected: 0, fit: 0.05996695564452847

# 323.88793266129557
# 0 - 0 => [0.484802823441564], expected: 0, fit: 0.23503377761691227
# 0 - 1 => [0.9840224443077834], expected: 1, fit: 0.0002552822858978829
# 1 - 0 => [0.9889082552840414], expected: 1, fit: 0.0001230268008439964
# 1 - 1 => [0.034655967938337265], expected: 0, fit: 0.0012010361137430605

# Gen: 50 Fitness: 1076.9845338426924
# 0 - 0 => [0.043395795820732413], expected: 0, fit: 0.0018831950949146968
# 0 - 1 => [0.9218523441754538], expected: 1, fit: 0.006107056110871728
# 1 - 0 => [0.9887334085246545], expected: 1, fit: 0.00012693608347232738
# 1 - 1 => [0.01814115058274791], expected: 0, fit: 0.0003291013444659349

# Gen: 82 Fitness: 44800.83419159887
# 0 - 0 => [0.0021045069821121224], expected: 0, fit: 4.4289496377586735e-06
# 0 - 1 => [0.9922250571791854], expected: 1, fit: 6.044973586693633e-05
# 1 - 0 => [0.997547492364821], expected: 1, fit: 6.014793700611355e-06
# 1 - 1 => [0.0026714230076915115], expected: 0, fit: 7.136500886023561e-06
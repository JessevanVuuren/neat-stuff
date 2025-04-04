from NEAT.genome_history import *
from population import *
import time

genome_history = GenomeHistory(2, 1)

xor = [
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 0)
]


pop = Population(genome_history, 10)
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
from dataclasses import dataclass
from neat_ref import *
import time

start = time.perf_counter()


@dataclass()
class XorInput:
    inputs: list[float]
    output: int


xor_values: list[XorInput] = [
    XorInput([0, 0], 0),
    XorInput([0, 1], 1),
    XorInput([1, 0], 1),
    XorInput([1, 1], 0),
]

gh = GenomeHistory(2, 1)
pop = Population(gh, 100)


def eval_fitness(genomes: list[Genome]):

    for genome in genomes:
        genome.fitness = 4

        for xor in xor_values:
            out = genome.get_outputs(xor.inputs)
            genome.fitness -= (out[0] - xor.output) ** 2


pop.run(eval_fitness, 100, report=True)


print("Gen:", pop.generation, "Fitness:", pop.best_global.fitness)
for eval in xor_values:
    out = pop.best_global.get_outputs(eval.inputs)
    print(f"{eval.inputs[0]} - {eval.inputs[1]} => {out}, expected: {eval.output}, fit: {(out[0] - eval.output) ** 2}")
print()


pop.best_global.info()

print()
print(f"total time: {time.perf_counter() - start}")


# 39657254 function calls (39651299 primitive calls) in 62.935 seconds
# 41525770 function calls (41519815 primitive calls) in 59.742 seconds -> genome_history map
# 25444520 function calls (25438565 primitive calls) in 15.954 seconds -> gene and node map


# Gen: 100 Fitness: 4.0
# 0 - 0 => [5.2781822826751376e-09], expected: 0, fit: 2.785920820914573e-17
# 0 - 1 => [0.9999999986885615], expected: 1, fit: 1.7198709742729778e-18
# 1 - 1 => [1.0], expected: 1, fit: 0.0
# 1 - 0 => [8.618799089730035e-09], expected: 0, fit: 7.428369774913127e-17

# Nodes: len nodes: 37
# Genes: len genes: 185
# inputs nodes: 3
# outputs nodes: 1
from neat_ref import *


@dataclass()
class XorInput:
    inputs: list[float]
    output: int


xor_values: list[XorInput] = [
    XorInput([0, 0, 1], 0),
    XorInput([0, 1, 1], 1),
    XorInput([1, 0, 1], 1),
    XorInput([1, 1, 1], 0),
]

gh = GenomeHistory(3, 1)
pop = Population(gh, 100)


def eval_fitness(genomes: list[Genome]):

    for genome in genomes:
        genome.fitness = 4

        for xor in xor_values:
            out = genome.get_outputs(xor.inputs)
            genome.fitness -= (out[0] - xor.output) ** 2


pop.run(eval_fitness, 100)


print("Gen:", pop.generation, "Fitness:", pop.best_global.fitness)
for eval in xor_values:
    out = pop.best_global.get_outputs(eval.inputs)
    print(f"{eval.inputs[0]} - {eval.output} => {out}, expected: {eval.output}, fit: {(out[0] - eval.output) ** 2}")
print()

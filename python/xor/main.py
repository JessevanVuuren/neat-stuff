from neat_ref import *
from xor_solver import *

genome_history = GenomeHistory(3, 1)

xor: list[XorInput] = [
    XorInput([0, 0, 1], 0),
    XorInput([0, 1, 1], 1),
    XorInput([1, 0, 1], 1),
    XorInput([1, 1, 1], 0),
]

pop = Population_xor(genome_history, 100)

for i in range(100):

    best_xor = pop.update(xor)

    if (pop.local_best.fitness == pop.global_best.fitness):

        print()
        print("Gen:", i, "Fitness:", best_xor.fitness)
        for eval in xor:
            out = best_xor.predict(eval.inputs)
            print(f"{eval.inputs[0]} - {eval.output} => {out}, expected: {eval.output}, fit: {(out[0] - eval.output) ** 2}")
        print()
    else:
        print("Gen:", i, "Fitness:", best_xor.fitness)

    pop.reset()


print(pop.global_best.fitness)
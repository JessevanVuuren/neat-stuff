import time
from neat_ref import *


brain = load_genome("../astroFighter/best_genome_gen_147")
gh = brain.genome_history

amount = 200
# pop = Population(gh, amount)


# for i in range(pop.pop_size):
#     pop.population[i] = brain

# brain.info()
# print(len(gh.all_genes))


# print("start ")
# start = time.perf_counter()

# pop.reset()


# stop = time.perf_counter()
# print(f"Total time:\t {stop - start}ms")


new_gh = GenomeHistory2(8, 3)

for i, gene in enumerate(gh.all_genes):
    new_gh.all_geness[gene.in_node.number, gene.out_node.number] = gene

pop = Population(new_gh, amount)


for i in range(pop.pop_size):
    pop.population[i] = brain

brain.info()
print(len(gh.all_genes))


print("start ")
start = time.perf_counter()

pop.reset()


stop = time.perf_counter()
print(f"Total time:\t {stop - start}ms")
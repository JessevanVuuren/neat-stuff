from debug_genome import DebugGenome
from neat_ref import *

gh = GenomeHistory(8, 3)

pop = Population(gh, 10)

dg = DebugGenome()


for i, p in enumerate(pop.population):
    p.fitness = i



for i in range(100):
    pop.reset()

print()


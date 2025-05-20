from debug_genome import DebugGenome
from neat_ref import *

dg = DebugGenome()


gh = GenomeHistory(8, 3)
brain = Genome(gh)

dg.print_genome(brain)
dg.history_info(brain.genome_history)

for i in range(1000):
    brain.mutate()

print()

dg.print_genome(brain)
dg.history_info(brain.genome_history)


layers: set[float] = set()

for i in brain.nodes:
    layers.add(i.layer)

print()
print()

out = brain.get_outputs([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
print(out)
print()
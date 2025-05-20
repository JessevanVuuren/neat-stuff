from debug_genome import DebugGenome
from neat_ref import *

dg = DebugGenome()


gh = GenomeHistory(8, 3)
brain = Genome(gh)

dg.print_genome(brain)
dg.history_info(brain.genome_history)

brain.mutate()

print()
print()
print()

dg.print_genome(brain)
dg.history_info(brain.genome_history)

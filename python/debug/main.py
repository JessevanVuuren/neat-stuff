from debug_genome import DebugGenome
from neat_ref import *

brain = load_genome("best_genome_slow")
# brain = load_genome("best_genome_260_gen")


dg = DebugGenome()

dg.print_genome(brain)
dg.history_info(brain.genome_history)

brain.mutate()


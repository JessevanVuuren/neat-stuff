from debug_genome import DebugGenome
from neat_ref import *

gh = GenomeHistory(8, 3)


pop = Population(gh, 10)

dg = DebugGenome()

# dg.print_genome(pop.best_global)


@dataclass
class MutateInfo:
    add_node: int
    add_gene: int
    remove_node: int
    remove_gene: int

    def print(self):
        print(f"add_node: {self.add_node}")
        print(f"add_gene: {self.add_gene}")
        print(f"remove_node: {self.remove_node}")
        print(f"remove_gene: {self.remove_gene}")


x = MutateInfo(0, 0, 0, 0)

for i in pop.population:
    i.fitness = 1

pop.reset()

amount = 1000
# print(f"mutate {amount} times")
# for _ in range(amount):
#     gen.mutate()


# gen.crossover(gen)


print()
x.print()

# dg.print_genome(gen)


#     def mutate(self, x):
#         if len(self.genes) == 0:
#             self.add_gene()

#         if random.random() < .5:  # add gene
#             x.add_gene += 1
#             self.add_gene()
#         if random.random() < .2:  # add node
#             x.add_node += 1
#             self.add_node()
#         if random.random() < .5:  # remove gene
#             x.remove_gene += 1
#             self.remove_gene()
#         if random.random() < .2:  # remove node
#             x.remove_node += 1
#             self.remove_node()

#         for i in range(len(self.genes)):
#             self.genes[i].mutate()
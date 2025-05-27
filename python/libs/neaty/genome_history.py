from .gene import *
from .node import *


class GenomeHistory:
    def __init__(self, inputs:int, outputs:int) -> None:
        self.outputs = outputs
        self.inputs = inputs

        self.all_genes: dict[tuple[int, int], Gene] = {}
        self.global_innovation = 0

    def add_gene(self, gene:Gene):
        self.all_genes[gene.in_node.number, gene.out_node.number] = gene

    def exists(self, n1: Node, n2: Node):
        return self.all_genes.get((n1.number, n2.number))

# dict   5131137   22.517    0.000   22.517    0.000 genome.py:213(exists)
# list   6349005   30.676    0.000   30.676    0.000 genome.py:213(exists)


# 122560514 function calls (115054483 primitive calls) in 130.817 seconds
# 113889271 function calls (106383240 primitive calls) in 85.543 seconds
# 80990205 function calls (73484174 primitive calls) in 59.685 seconds

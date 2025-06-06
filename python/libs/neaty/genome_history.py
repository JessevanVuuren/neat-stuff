from .config import NeatConfig
from .gene import *
from .node import *


class GenomeHistory:
    def __init__(self, config: NeatConfig) -> None:
        self.outputs = config.outputs
        self.inputs = config.inputs

        self.all_genes: dict[tuple[int, int], Gene] = {}
        self.global_innovation = 0

    def add_gene(self, gene: Gene):
        self.all_genes[gene.in_node.number, gene.out_node.number] = gene

    def exists(self, n1: Node, n2: Node):
        return self.all_genes.get((n1.number, n2.number))

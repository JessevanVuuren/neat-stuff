from .gene import *
from .node import *


class GenomeHistory(object):
    def __init__(self, inputs:int, outputs:int) -> None:
        self.outputs = outputs
        self.inputs = inputs

        self.all_genes: list[Gene] = []
        self.global_innovation = 0

    def exists(self, n1: Node, n2: Node):
        for c in self.all_genes:
            if c.in_node.number == n1.number and c.out_node.number == n2.number:
                return c.clone()

        return None




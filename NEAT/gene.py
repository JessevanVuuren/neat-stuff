from .node import *
import random


class Gene(object):
    def __init__(self, in_node, out_node) -> None:
        self.in_node: Node = in_node  # type: ignore
        self.out_node: Node = out_node  # type: ignore

        self.weight = random.random() * 4 - 2

        self.innovation = -1
        self.enabled = True

    def mutate(self):
        if random.random() < .1:
            self.weight = random.random() * 4 - 2
        else:
            self.weight += random.uniform(-0.02, 0.02)
            self.weight = self.weight if self.weight < 2 else 2
            self.weight = self.weight if self.weight > -2 else -2

    def clone(self):
        gene = Gene(self.in_node, self.out_node)
        gene.weight = self.weight
        gene.innovation = self.innovation
        gene.enabled = self.enabled
        return gene

    def get_info(self):
        s = str(self.innovation) + "] "
        s += str(self.in_node.number) + "(" + str(self.in_node.layer) + ") -> "
        s += str(self.out_node.number) + "(" + str(self.out_node.layer) + ") "
        s += str(self.weight) + " "
        s += str(self.enabled) + "\n"
        return s

    def __str__(self) -> str:
        return self.get_info()

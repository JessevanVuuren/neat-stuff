from .node import Node
import random

max_diff = 10
grow = .5

class Gene(object):
    def __init__(self, in_node:Node, out_node:Node) -> None:
        self.in_node: Node = in_node
        self.out_node: Node = out_node

        self.weight = random.random() * (max_diff * 2) - max_diff

        self.innovation = -1
        self.enabled = True

    def mutate(self):
        if random.random() < .1:
            self.weight = random.random() * (max_diff * 2) - max_diff
        else:
            self.weight += random.random() * (grow * 2) - grow
            self.weight = self.weight if self.weight < max_diff else max_diff
            self.weight = self.weight if self.weight > -max_diff else -max_diff

    def clone(self):
        gene = Gene(self.in_node, self.out_node)
        gene.weight = self.weight
        gene.innovation = self.innovation
        gene.enabled = self.enabled
        return gene
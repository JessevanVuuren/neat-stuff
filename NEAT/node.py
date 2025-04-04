from .gene import *
import math

class Node(object):
    def __init__(self, n, l, is_bias=False) -> None:
        self.number = n
        self.layer = l # type -> input, hidden bias

        self.output = 0
        self.is_bias = is_bias

        self.genes:list[Gene] = [] # type: ignore

        self.sigmoid = lambda x: 1 / (1 + math.exp(-x))

    def clone(self):
        n = Node(self.number, self.layer, self.is_bias)
        n.output = self.output
        return n

    def calculate(self):
        if self.layer == 0:
            return
        
        s = 0
        for g in self.genes:
            if g.enabled:
                s += g.in_node.output * g.weight

        self.output = self.sigmoid(s)
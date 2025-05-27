from .node import Node
import random
import math

weight_init_mean = 0.0
weight_init_stDev = 1.0
weight_max_value = 30
weight_min_value = -30
weight_mutate_power = 0.5
weight_mutate_rate = 0.8
weight_replace_rate = 0.1


class Gene(object):
    def __init__(self, in_node: Node, out_node: Node) -> None:
        self.in_node: Node = in_node
        self.out_node: Node = out_node

        self.weight = self.gaussian_number() * weight_init_stDev + weight_init_mean

        self.innovation = -1
        self.enabled = True

    def mutate(self):
        if (random.random() < weight_mutate_rate):
            if (random.random() < weight_replace_rate):
                self.weight = self.gaussian_number() * weight_init_stDev + weight_init_mean
            else:
                delta = self.gaussian_number() * weight_mutate_power
                self.weight += delta

        self.weight = self.clamp(self.weight)

    def clamp(self, number: float):
        return max(weight_min_value, min(number, weight_max_value))

    def gaussian_number(self) -> float:
        rand1 = random.random()
        rand2 = random.random()

        return math.sqrt(-2 * math.log(rand1)) * math.cos(2 * math.pi * rand2)

    def clone(self):
        gene = Gene(self.in_node, self.out_node)
        gene.weight = self.weight
        gene.innovation = self.innovation
        gene.enabled = self.enabled
        return gene

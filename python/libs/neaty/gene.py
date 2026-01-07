from __future__ import annotations
from typing import TYPE_CHECKING
from .config import NeatConfig

import random
import math

if TYPE_CHECKING:
    from .node import Node


class Gene(object):
    def __init__(self, config: NeatConfig, in_node: Node, out_node: Node) -> None:
        self.in_node: Node = in_node
        self.out_node: Node = out_node
        self.config = config

        self.weight = self.gaussian_number() * self.config.weight_init_stdev + self.config.weight_init_mean

        self.innovation = -1
        self.enabled = True

    def mutate(self):
        if random.random() < self.config.weight_mutate_rate:
            if random.random() < self.config.weight_replace_rate:
                self.weight = self.gaussian_number() * self.config.weight_init_stdev + self.config.weight_init_mean
            else:
                delta = self.gaussian_number() * self.config.weight_mutate_power
                self.weight += delta

        self.weight = self.clamp(self.weight)

    def clamp(self, number: float) -> float:
        return max(self.config.weight_min_value, min(number, self.config.weight_max_value))

    def gaussian_number(self) -> float:
        rand1 = random.random()
        rand2 = random.random()

        return math.sqrt(-2 * math.log(rand1)) * math.cos(2 * math.pi * rand2)

    def clone(self) -> Gene:
        gene = Gene(self.config, self.in_node, self.out_node)
        gene.weight = self.weight
        gene.innovation = self.innovation
        gene.enabled = self.enabled
        return gene

from __future__ import annotations
from typing import TYPE_CHECKING

from .config import NeatConfig

import random
import math

if TYPE_CHECKING:
    from .gene import Gene
    from .gene import Node


class Node:
    def __init__(self, config: NeatConfig, n: int, l: float) -> None:
        self.config = config
        self.number = n
        self.layer = l

        self.output: float = 0
        self.calculated = False

        self.bias = self.gaussian_number() * self.config.bias_init_stdev + self.config.bias_init_mean

        self.genes: list[Gene] = []

    def mutate(self) -> None:
        if random.random() < self.config.bias_mutate_rate:
            if random.random() < self.config.bias_replace_rate:
                self.bias = self.gaussian_number() * self.config.bias_init_stdev + self.config.bias_init_mean
            else:
                delta = self.gaussian_number() * self.config.bias_mutate_power
                self.bias += delta

        self.bias = self.clamp(self.bias, self.config.bias_min_value, self.config.bias_max_value)

    def clamp(self, number: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(number, max_value))

    def gaussian_number(self) -> float:
        rand1 = random.random()
        rand2 = random.random()

        return math.sqrt(-2 * math.log(rand1)) * math.cos(2 * math.pi * rand2)

    def sigmoid(self, x: float) -> float:
        val = self.clamp(x, -100, 100) * 5.0
        return 1 / (1 + math.exp(-val))

    def clone(self) -> Node:
        n = Node(self.config, self.number, self.layer)
        n.output = self.output
        n.bias = self.bias
        return n

    def calculate(self) -> None:
        if self.calculated:
            return

        self.calculated = True

        s = 0
        for g in self.genes:
            if g.enabled:
                s += g.in_node.output * g.weight

        self.output = self.sigmoid(s + self.bias)

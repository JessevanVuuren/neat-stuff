from .gene import *
import random
import math

bias_init_mean = 0.0
bias_init_stDev = 1.0
bias_max_value = 30
bias_min_value = -30
bias_mutate_power = 0.5
bias_mutate_rate = 0.7
bias_replace_rate = 0.1


class Node:
    def __init__(self, n: int, l: float) -> None:
        self.number = n
        self.layer = l  # type -> input, hidden bias

        self.output: float = 0
        self.calculated = False

        self.bias = self.gaussian_number() * bias_init_stDev + bias_init_mean

        self.genes: list[Gene] = []

    def mutate(self):
        if (random.random() < bias_mutate_rate):
            if (random.random() < bias_replace_rate):
                self.bias = self.gaussian_number() * bias_init_stDev + bias_init_mean
            else:
                delta = self.gaussian_number() * bias_mutate_power
                self.bias += delta

        self.bias = self.clamp(self.bias, bias_min_value, bias_max_value)

    def clamp(self, number: float, min_value: float, max_value: float):
        return max(min_value, min(number, max_value))

    def gaussian_number(self) -> float:
        rand1 = random.random()
        rand2 = random.random()

        return math.sqrt(-2 * math.log(rand1)) * math.cos(2 * math.pi * rand2)

    def sigmoid(self, x: float) -> float:
        # val = self.clamp(x, -100, 100) * 5.0
        # return 1 / (1 + math.exp(-val))
        return 1 / (1 + math.exp(-x))

    def clone(self):
        n = Node(self.number, self.layer)
        n.output = self.output
        n.bias = self.bias
        return n

    def calculate(self):
        if self.calculated:
            return

        self.calculated = True

        s = 0
        for g in self.genes:
            if g.enabled:
                s += g.in_node.output * g.weight

        self.output = self.sigmoid(s + self.bias)

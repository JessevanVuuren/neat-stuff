from __future__ import annotations
from dataclasses import dataclass
from neat_ref import *
import random


@dataclass()
class XorInput:
    inputs: list[float]
    output: int


class XORsolver:
    def __init__(self, gh: GenomeHistory) -> None:
        self.gh = gh
        self.fitness = 0.0

        self.brian = Genome(gh)
        for _ in range(10):
            self.brian.mutate()

    def mate(self, partner: XORsolver):
        xor = XORsolver(self.gh)
        xor.brian = self.brian.crossover(partner.brian)
        return xor

    def calculate_fitness(self, inputs: list[XorInput]):
        total_error = 4
        for input in inputs:
            out = self.predict(input.inputs)
            total_error -= (out[0] - input.output) ** 2

        self.fitness = total_error
        return self.fitness

    def predict(self, inputs: list[float]):
        out = self.brian.get_outputs(inputs)
        return out


class Population_xor:
    def __init__(self, gh: GenomeHistory, pop_size: int) -> None:
        self.pop_size = pop_size

        self.population: list[XORsolver] = []
        for _ in range(pop_size):
            self.population.append(XORsolver(gh))

        self.gh = gh

        self.local_best = self.population[0]
        self.global_best = self.population[0]

    def reset(self):
        parents = self.population

        parents.sort(key=lambda x: x.fitness, reverse=True)

        self.population = []

        for _ in range(self.pop_size):
            parent1 = parents[random.randint(0, len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]
            agent = parent1.mate(parent2)
            agent.brian.mutate()
            self.population.append(agent)

    def update(self, inputs: list[XorInput]):
        self.local_best = self.population[0]
        for agent in self.population:

            fitness = agent.calculate_fitness(inputs)

            if (fitness > self.local_best.fitness):
                self.local_best = agent
            if (fitness > self.global_best.fitness):
                self.global_best = agent

        return self.local_best

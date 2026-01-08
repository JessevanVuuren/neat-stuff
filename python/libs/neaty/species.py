import random

from .genome import Genome
from .genome_history import GenomeHistory


class Species:
    def __init__(self, member: Genome) -> None:
        self.members: list[Genome] = [member]
        self.representative: Genome = member
        self.average_fitness = 0.0
        self.allow_offspring = 0
        self.staleness = 0
        self.best_fitness = member.fitness

    def update_staleness(self) -> None:
        max_member = max([m.fitness for m in self.members])
        if max_member > self.best_fitness:
            self.best_fitness = max_member
            self.staleness = 0
        else:
            self.staleness += 1

    def add(self, genome: Genome) -> None:
        self.members.append(genome)
        if genome.fitness > self.representative.fitness:
            self.representative = genome

    def check(self, genome: Genome, threshold: float) -> bool:
        compatibility = self.representative.calculate_compatibility(genome)
        return compatibility < threshold

    def adjusted_fitness(self) -> None:
        for genome in self.members:
            genome.adjusted_fitness = genome.fitness / len(self.members)

    def get_total_adjusted_fitness(self) -> float:
        return sum([g.adjusted_fitness for g in self.members])

    def get_average_fitness(self) -> float:
        self.average_fitness = self.get_total_adjusted_fitness() / len(self.members)
        return self.average_fitness

    def get_random_parent(self) -> Genome:
        total_priority = sum(g.adjusted_fitness for g in self.members)
        selection = random.uniform(0, total_priority)

        current = 0
        for g in self.members:
            current += g.adjusted_fitness
            if current >= selection:
                return g

        return self.representative

    def give_random_offspring(self, gh: GenomeHistory) -> Genome:
        parent1 = self.get_random_parent()
        parent2 = self.get_random_parent()
        child = parent1.crossover(parent2)
        child.mutate()
        return child

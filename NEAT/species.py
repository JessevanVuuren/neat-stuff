from .genome import Genome
import random


class Species:
    def __init__(self, mem) -> None:
        self.members: list[Genome] = []
        self.members.append(mem)
        self.rep = self.members[0]

        self.max_members = 8
        
        self.average_fitness = 0
        self.allow_offspring = 0
        
        self.threshold = 3.5

        # No. of generations species hasn't improved
        self.staleness = 0

    def add(self, brain):
        self.members.append(brain)

        if self.rep.fitness < brain.fitness:
            self.rep = self.members[-1]

    def get_random_parent(self):
        # random member, give bias to high performing members
        total_priority = sum([m.adjusted_fitness for m in self.members])
        selection = random.uniform(0, total_priority)

        current = 0
        for i, member in enumerate(self.members):
            current += member.adjusted_fitness
            if (current >= selection):
                return self.members[i]

        return self.rep

    def give_random_offspring(self):
        parent1 = self.get_random_parent()
        parent2 = self.get_random_parent()
        child = parent1.crossover(parent2)
        child.mutate()
        return child

    def check(self, brain):
        done = False
        cd = self.rep.calculate_compatibility(brain)
        if cd < self.threshold and len(self.members) < self.max_members:
            done = True

        return done

    def adjusted_fitness(self):
        for i in range(len(self.members)):
            self.members[i].adjusted_fitness = self.members[i].fitness / len(self.members)

    def get_average_fitness(self):
        return sum([m.adjusted_fitness for m in self.members]) / len(self.members)
from collections.abc import Callable
from .genome_history import *
from .species import *
from .genome import *

import random


class PopulationSpecies:
    def __init__(self, gh: GenomeHistory, pop_size: int, target_species_count: int = 10) -> None:
        self.population: list[Genome] = []
        self.species: list[Species] = []

        self.target_species_count = target_species_count
        self.compatibility_threshold = 3.5

        self.pop_size = pop_size
        self.gh = gh

        self.generation = 0
        self.global_avg = 0

        for _ in range(self.pop_size):
            genome = Genome(self.gh)
            genome.mutate()
            self.population.append(genome)

        self.best_local = self.population[0]
        self.best_global = self.population[0]

    def speciate(self):
        for sp in self.species:
            sp.members.clear()
            sp.representative = random.choice(sp.members) if sp.members else sp.representative

        for genome in self.population:
            assigned = False
            for sp in self.species:
                if sp.check(genome, self.compatibility_threshold):
                    sp.add(genome)
                    assigned = True
                    break
            if not assigned:
                self.species.append(Species(genome))

        self.species = [sp for sp in self.species if len(sp.members) > 0]

    def set_allowed_offspring(self):
        total_adjusted_fitness = 0.0
        for sp in self.species:
            sp.adjusted_fitness()
            total_adjusted_fitness += sp.get_total_adjusted_fitness()

        self.global_avg = total_adjusted_fitness / self.pop_size

        total_offspring = 0
        for sp in self.species:
            if sp.get_total_adjusted_fitness() == 0:
                sp.allow_offspring = 0
            else:
                proportion = sp.get_total_adjusted_fitness() / total_adjusted_fitness
                sp.allow_offspring = max(1, int(proportion * self.pop_size))
            total_offspring += sp.allow_offspring

        while total_offspring < self.pop_size:
            random.choice(self.species).allow_offspring += 1
            total_offspring += 1
        while total_offspring > self.pop_size:
            sp = random.choice(self.species)
            if sp.allow_offspring > 1:
                sp.allow_offspring -= 1
                total_offspring -= 1

    def adjust_compatibility_threshold(self):
        species_diff = len(self.species) - self.target_species_count

        if abs(species_diff) > 1:
            self.compatibility_threshold += 0.05 * species_diff

        self.compatibility_threshold = max(0.5, min(self.compatibility_threshold, 15.0))

    def reset(self):
        self.generation += 1
        self.speciate()

        for sp in self.species:
            sp.update_staleness()

        self.species = [sp for sp in self.species if sp.staleness < 15 or sp.best_fitness >= self.best_global.fitness]

        self.adjust_compatibility_threshold()
        self.set_allowed_offspring()

        new_pop: list[Genome] = [self.best_global.clone()]

        for sp in self.species:
            elite = max(sp.members, key=lambda g: g.fitness)
            new_pop.append(elite.clone())
            for _ in range(sp.allow_offspring - 1):
                new_pop.append(sp.give_random_offspring(self.gh))

        while len(new_pop) < self.pop_size:
            new_pop.append(Genome(self.gh))

        self.population = new_pop[:self.pop_size]

    def run(self, fitness_function: Callable[[list[Genome]], None], n: int = 0):

        while self.generation < n or n == 0:
            fitness_function(self.population)

            self.best_local = max(self.population, key=lambda g: g.fitness).clone()
            if self.best_local.fitness > self.best_global.fitness:
                self.best_global = self.best_local.clone()

            print(f"\n=== Generation {self.generation} ===")
            print(f"Best Local Fitness: {self.best_local.fitness:.3f}")
            print(f"Best Global Fitness: {self.best_global.fitness:.3f}")
            print(f"Compatibility Threshold: {self.compatibility_threshold:.2f}")
            print(f"Number of Species: {len(self.species)}")

            stale = [sp.staleness for sp in self.species]
            stale.sort(reverse=True)
            print(f"Staleness: {stale}")

            species_sizes = [len(sp.members) for sp in self.species]
            species_sizes.sort(reverse=True)
            print(f"Species Sizes: {species_sizes}")
            print()

            self.reset()

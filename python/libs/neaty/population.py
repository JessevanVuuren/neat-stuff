from __future__ import annotations

import random
from collections.abc import Callable

from .config import NeatConfig
from .genome import Genome
from .genome_history import GenomeHistory
from .manager import save_genome
from .parallel import MultiEvaluator
from .profiler import Profiler
from .species import Species


class Population:
    def __init__(self, config: NeatConfig, gh: GenomeHistory) -> None:
        self.population: list[Genome] = []
        self.species: list[Species] = []

        self.config = config
        self.gh = gh

        self.target_species_count = config.target_species
        self.compatibility_threshold = 3.5
        self.pop_size = config.pop_size

        self.generation = 0
        self.global_avg = 0

        for _ in range(self.pop_size):
            genome = Genome(self.config, self.gh)
            genome.mutate()
            self.population.append(genome)

        self.best_local = self.population[0]
        self.best_global = self.population[0]

    def speciate(self) -> None:
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

    def set_allowed_offspring(self) -> None:
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

    def adjust_compatibility_threshold(self) -> None:
        species_diff = len(self.species) - self.target_species_count

        if abs(species_diff) > 1:
            self.compatibility_threshold += 0.05 * species_diff

        self.compatibility_threshold = max(0.5, min(self.compatibility_threshold, 15.0))

    def reset_species(self) -> None:
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
            new_pop.append(Genome(self.config, self.gh))

        self.population = new_pop[: self.pop_size]

    def reset_population(self) -> None:
        self.generation += 1

        parents = self.population.copy()
        self.population.clear()

        parents.sort(key=lambda x: x.fitness, reverse=True)

        for _ in range(self.pop_size):
            parent1 = parents[random.randint(0, len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]

            child = parent1.crossover(parent2)
            child.mutate()

            self.population.append(child)

        self.population[0] = self.best_global.clone()
        for i in range(self.config.elitism):
            if i + 1 < len(self.population) and i < len(parents):
                self.population[i + 1] = parents[i].clone()

    def run(self, fitness_function: Callable[[list[Genome]], list[float]]) -> None:
        if self.config.parallel:
            evaluator = MultiEvaluator(fitness_function, self.config.workers)
            fitness_function = evaluator.eval

        with Profiler()["eval"]:
            while self.generation < self.config.generations or self.config.generations == 0:
                with Profiler()["fitness"]:
                    fitness_function(self.population)

                self.best_local = max(self.population, key=lambda g: g.fitness).clone()
                if self.best_local.fitness > self.best_global.fitness:
                    self.best_global = self.best_local.clone()

                with Profiler()["reset"]:
                    if self.config.speciation:
                        self.reset_species()
                    else:
                        self.reset_population()

                if self.config.log_progress:
                    self.report()

                if self.config.target_fitness and self.best_global.fitness >= self.config.target_fitness:
                    break

        if self.config.save_genome:
            fit_name = f"{self.best_global.fitness:.4f}".replace(".", "-")
            save_genome(self.best_global, f"genomes/genome_gen_fit_{fit_name}")

        print(f"Eval: {Profiler().get('eval')}")

    def report(
        self,
    ) -> None:
        print(f"=== [Generation: {self.generation}] ===")
        print(f"Reset time: {Profiler().get('reset'):.4f}ms")
        print(f"Sim time: {Profiler().get('fitness'):.4f}ms")
        print(f"Local Fitness: {self.best_local.fitness:.6f}")
        print(f"Global Fitness: {self.best_global.fitness:.6f}")
        print(f"Genes history: {len(self.gh.all_genes)}")

        if self.config.speciation:
            stale = [sp.staleness for sp in self.species]
            stale.sort(reverse=True)
            print(f"Staleness: {stale}")

            species_sizes = [len(sp.members) for sp in self.species]
            species_sizes.sort(reverse=True)
            print(f"Species Sizes: {species_sizes}")

        self.best_global.info()

        print()


# 136.60020986699965
# 79.3463093420014

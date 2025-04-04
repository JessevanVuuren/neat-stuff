from genome_history import *
from species import *
from genome import *
import random

class XORsolver:
    def __init__(self, gh) -> None:
        self.gh = gh
        self.fitness = 0.0

        self.brian = Genome(gh)
        for _ in range(10):
            self.brian.mutate()

    def mate(self, partner):
        xor = XORsolver(self.gh)
        xor.brian = self.brian.crossover(partner.brian)
        return xor

    def predict(self, inputs):
        out = self.brian.get_outputs(inputs)
        return out

class Population:
    def __init__(self, gh, pop_size) -> None:
        self.pop_size = pop_size
        self.gh = gh

        self.population: list[XORsolver] = [XORsolver(gh) for _ in range(pop_size)]
        self.species: list[Species] = []
        self.best_fitness = 0.0
        self.champion = None
        self.generation = 0

        self.speciate()  # initial grouping

    def speciate(self):
        self.species.clear()
        assigned = [False] * len(self.population)

        while not all(assigned):
            i = assigned.index(False)
            rep = self.population[i].brian
            sp = Species(rep)
            assigned[i] = True

            for j in range(len(self.population)):
                if assigned[j]:
                    continue
                if sp.check(self.population[j].brian):
                    sp.add(self.population[j].brian)
                    assigned[j] = True

            self.species.append(sp)

    def update(self, xor_inputs):
        best_xor = None
        self.best_fitness = 0.0

        for xor in self.population:
            total_error = 0
            for inputs, expected in xor_inputs:
                out = xor.predict(inputs)
                total_error += (out[0] - expected) ** 2

            xor.fitness = 1 / (total_error + 1e-6)

            if xor.fitness > self.best_fitness:
                self.best_fitness = xor.fitness
                best_xor = xor
                self.champion = xor

        # Adjust fitness within species
        for species in self.species:
            species.adjusted_fitness()

        return best_xor

    def set_offspring_allocation(self):
        total_adjusted = sum(
            sum(m.adjusted_fitness for m in sp.members) for sp in self.species
        )

        for sp in self.species:
            sp_fitness = sum(m.adjusted_fitness for m in sp.members)
            sp.allow_offspring = round((sp_fitness / total_adjusted) * self.pop_size)

    def reset(self):
        self.generation += 1
        self.speciate()
        self.set_offspring_allocation()

        new_population: list[XORsolver] = []

        for sp in self.species:
            for _ in range(sp.allow_offspring):
                child = XORsolver(self.gh)
                child.brian = sp.give_random_offspring()
                new_population.append(child)

        # Fill the rest of the population if needed
        while len(new_population) < self.pop_size:
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            child = parent1.mate(parent2)
            child.brian.mutate()
            new_population.append(child)

        self.population = new_population

from __future__ import annotations
from game_types import *
from neat_ref import *
import random

class Population:
    def __init__(self, gh: GenomeHistory, pop_size: int, agent: Type[Agent]) -> None:
        self.pop_size = pop_size
        self.population: list[Agent] = []
        self.gh = gh

        for _ in range(pop_size):
            self.population.append(agent(gh))

        self.best_local = self.population[0]
        self.best_global = self.population[0]

    def reset(self):
        parents = self.population

        parents.sort(key=lambda x: x.fitness, reverse=True)

        self.population = []

        for _ in range(self.pop_size):
            parent1 = parents[random.randint(0, len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]
            agent = parent1.mate(parent2)
            agent.brain.mutate()
            self.population.append(agent)

        self.best_local = self.population[0]

    def all_dead(self):

        for agent in self.population:
            if not agent.dead:
                return False

        return True

    def update(self, inputs: Sequence[Pipe], dt: float):
        for agent in self.population:

            agent.update(inputs, dt)
            fitness = agent.fitness

            if (fitness > self.best_local.fitness):

                self.best_fitness = agent

            if (fitness > self.best_global.fitness):
                self.best_global = agent


# class Population:
#     population = 100
    
#     def update_population
#         for agent in population
#             update_agent(pipe)



# class agent:
#     pipe_calculate_next_move()

#     render_agent


# class pipe
#     pos_pipe
#     size_pipe

#     render_pipe

# class screen
#     render_stuff


# these are my classes, the agent is part of the population, and requires class pipe and screen, but that makes my code tightly coupled, how can i 
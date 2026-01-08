from __future__ import annotations

import random
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from bird import Bird

if TYPE_CHECKING:
    from controller import GameController, PhysicsController



from game_types import Pipe


class PopulationBird:
    def __init__(self, pop_size: int, agent: Callable[[], Bird]) -> None:
        self.physicsController: PhysicsController
        self.gameController: GameController

        self.agent = agent
        self.generation = 0
        self.pop_size = pop_size
        self.population: list[Bird] = []

    def set_controllers(self, game: GameController, physics: PhysicsController):
        self.physicsController = physics
        self.gameController = game

    def create_population(self):
        for _ in range(self.pop_size):
            entity = self.agent()
            entity.set_controllers(self.gameController, self.physicsController)
            self.population.append(entity)

        self.best_local = self.population[0]
        self.best_global = self.population[0]

    def reset(self):
        self.generation += 1
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

            if fitness > self.best_local.fitness:
                self.best_fitness = agent

            if fitness > self.best_global.fitness:
                self.best_global = agent

    def display_stats(self):
        print()
        print("Generation:", self.generation)
        print("Best Local:", self.best_local.fitness)
        print("Best Global:", self.best_global.fitness)

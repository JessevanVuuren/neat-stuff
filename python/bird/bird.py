from __future__ import annotations

from population_bird import *
from game_types import *
from neat_ref import *
from globals import *

import pygame


class Bird(Agent):
    def __init__(self, gh: GenomeHistory) -> None:
        self.size = 25
        self.speed = 600
        self.dead = False
        self.hit = False
        self.fitness = 0.0
        self.gh = gh

        body = pygame.Rect(SCREEN_WIDTH * .3 - self.size / 2, SCREEN_HEIGHT / 2 - self.size / 2, self.size, self.size)
        self.graphics = Graphics(body)

        self.brain = Genome(gh)
        for _ in range(10):
            self.brain.mutate()

    def update(self, inputs: Sequence[Pipe], dt: float):
        pipe = self.closest_pipe(inputs)

        if (pipe.top_rect.colliderect(self.graphics.body) or pipe.bottom_rect.colliderect(self.graphics.body) or self.graphics.body.bottomleft[1] >= SCREEN_HEIGHT or self.graphics.body.topleft[1] < 0):
            self.dead = True

        if self.dead:
            return

        self.fitness += 1

        norm_inputs = self.get_inputs(pipe)
        action = self.think(norm_inputs)
        self.move(action, dt)

    def think(self, inputs: list[float]):
        out = self.brain.get_outputs(inputs)
        index = out.index(max(out))
        return ActionState(index)

    def closest_pipe(self, pipes: Sequence[Pipe]) -> Pipe:
        for pipe in pipes:
            if pipe.pos_x + pipe.width > self.graphics.body.topleft[0]:
                return pipe

        return pipes[0]

    def mate(self, parent: Bird):
        child = Bird(self.gh)
        child.brain = self.brain.crossover(parent.brain)
        return child

    def get_inputs(self, pipe: Pipe):
        inputs: list[float] = []
        inputs.append((SCREEN_HEIGHT - self.graphics.body.centery) / SCREEN_HEIGHT)                        # distance ground
        inputs.append((pipe.pos_x + pipe.width - self.graphics.body.topleft[0]) / SCREEN_WIDTH)            # distance first pipe
        inputs.append((self.graphics.body.bottomleft[1] - pipe.top_rect.bottomleft[1]) / SCREEN_HEIGHT)    # distance to top pipe
        inputs.append((pipe.bottom_rect.topleft[1] - self.graphics.body.topleft[1]) / SCREEN_HEIGHT)       # distance to bottom pipe
        return inputs

    def move(self, state: ActionState, dt: float):
        if self.dead:
            return

        if state == ActionState.UP:
            self.graphics.body.centery -= int(self.speed * dt)
        if state == ActionState.DOWN:
            self.graphics.body.centery += int(self.speed * dt)
        if state == ActionState.STAY:
            pass

    def __call__(self, gh: GenomeHistory) -> Self:
        raise NotImplementedError

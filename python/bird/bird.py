from __future__ import annotations

from population_bird import *
from game_types import *
from neat_ref import *
from globals import *

import pygame


class Bird(Agent):
    def __init__(self, gh: GenomeHistory) -> None:
        self.velocity = 0.0
        self.fitness = 0.0
        self.pre_pos = 0.0

        self.dead = False
        self.hit = False
        self.gh = gh

        self.body = pygame.Rect(SCREEN_WIDTH * .3 - BIRD_SIZE / 2, SCREEN_HEIGHT / 2 - BIRD_SIZE / 2, BIRD_SIZE, BIRD_SIZE)
        self.graphics = Graphics(self.body)
        self.graphics.animation_speed = BIRD_ANIMATION_SPEED

        self.brain = Genome(gh)
        for _ in range(10):
            self.brain.mutate()

    def set_sprites(self, sprites: list[str]):
        for sprite in sprites:
            img = pygame.image.load(sprite)
            scale_factor = BIRD_SIZE / img.get_width()
            scaled_img = pygame.transform.scale_by(img, scale_factor)
            self.body.height = scaled_img.get_height()
            self.graphics.assets.append(scaled_img)

    def update(self, inputs: Sequence[Pipe], dt: float, human_player: bool = False):
        pipe = self.closest_pipe(inputs)

        if (pipe.top_rect.colliderect(self.body) or pipe.bottom_rect.colliderect(self.body) or self.body.bottomleft[1] >= SCREEN_HEIGHT or self.body.topleft[1] < 0):
            self.dead = True

        if self.dead:
            return

        self.fitness += 1

        self.update_movement(pipe, dt, human_player)
        self.update_animation(dt)

    def update_movement(self, pipe: Pipe, dt: float, human_player: bool):
        if (not human_player):
            norm_inputs = self.get_inputs(pipe)
            action = self.think(norm_inputs)
            self.move(action, dt)
        else:
            self.velocity += GRAVITY * dt
            self.body.centery += int(self.velocity)

    def update_animation(self, dt: float):
        if (self.pre_pos > self.body.centery):
            self.graphics.current_image = 0
        elif (self.pre_pos == self.body.centery):
            self.graphics.current_image = 1
        else:
            self.graphics.current_image = 2

        self.pre_pos = self.body.centery
        self.graphics.anchor_point = tuple_2_vec2(self.body.topleft)

    def think(self, inputs: list[float]):
        out = self.brain.get_outputs(inputs)
        index = out.index(max(out))
        return ActionState(index)

    def closest_pipe(self, pipes: Sequence[Pipe]) -> Pipe:
        for pipe in pipes:
            if pipe.pos_x + PIPE_WIDTH > self.body.topleft[0]:
                return pipe

        return pipes[0]

    def fly(self):
        self.velocity = -BIRD_FLY_FORCE

    def mate(self, parent: Bird):
        child = Bird(self.gh)
        child.brain = self.brain.crossover(parent.brain)
        return child

    def get_inputs(self, pipe: Pipe):
        inputs: list[float] = []
        inputs.append((SCREEN_HEIGHT - self.body.centery) / SCREEN_HEIGHT)                        # distance ground
        inputs.append((pipe.pos_x + PIPE_WIDTH - self.body.topleft[0]) / SCREEN_WIDTH)            # distance first pipe
        inputs.append((self.body.bottomleft[1] - pipe.top_rect.bottomleft[1]) / SCREEN_HEIGHT)    # distance to top pipe
        inputs.append((pipe.bottom_rect.topleft[1] - self.body.topleft[1]) / SCREEN_HEIGHT)       # distance to bottom pipe
        return inputs

    def move(self, state: ActionState, dt: float):
        if self.dead:
            return

        if state == ActionState.UP:
            self.body.centery -= int(BIRD_SPEED * dt)
        if state == ActionState.DOWN:
            self.body.centery += int(BIRD_SPEED * dt)
        if state == ActionState.STAY:
            pass

    def __call__(self, gh: GenomeHistory) -> Self:
        raise NotImplementedError

from __future__ import annotations

from controller import PhysicsController, GameController
from game_types import *
from neat_ref import *
from globals import *

import random
import pygame


class Bird:
    def __init__(self, gh: GenomeHistory, assets: list[list[str]]) -> None:
        self.physicsController: PhysicsController
        self.gameController: GameController

        self.assets: list[list[str]] = assets
        self.fly_cooldown = .15
        self.gh = gh
        self.setup_bird()

    def set_controllers(self, game: GameController, physics: PhysicsController):
        self.physicsController = physics
        self.gameController = game

    def setup_bird(self):
        self.current_fly = 0.0
        self.rotation = 0.0
        self.velocity = 0.0
        self.fitness = 0.0
        self.pre_pos = 0.0

        self.dead = False
        self.hit = False

        self.body = pygame.Rect(SCREEN_WIDTH * .3 - BIRD_SIZE / 2, SCREEN_HEIGHT / 2 - BIRD_SIZE / 2, BIRD_SIZE, BIRD_SIZE)
        self.graphics = Graphics(self.body)
        self.graphics.animation_speed = BIRD_ANIMATION_SPEED

        self.brain = Genome(self.gh)
        for _ in range(10):
            self.brain.mutate()

        self.set_sprites(self.assets)

    def reset(self):
        self.setup_bird()

    def set_sprites(self, sprites: list[list[str]]):
        self.assets = sprites

        color_sprites = random.choice(self.assets)
        for sprite in color_sprites:
            img = pygame.image.load(sprite)
            scale_factor = BIRD_SIZE / img.get_width()
            scaled_img = pygame.transform.scale_by(img, scale_factor)
            self.body.height = scaled_img.get_height()
            self.graphics.assets.append(scaled_img)

    def update(self, inputs: Sequence[Pipe], dt: float):
        pipe = self.closest_pipe(inputs)

        if (pipe.top_rect.colliderect(self.body) or pipe.bottom_rect.colliderect(self.body) or self.body.bottomleft[1] >= SCREEN_HEIGHT or self.body.topleft[1] < 0):
            self.dead = True

        if self.dead:
            return

        self.fitness += 1

        if self.current_fly > 0:
            self.current_fly -= dt

        self.update_movement(pipe, dt)
        self.update_animation(dt)

    def update_movement(self, pipe: Pipe, dt: float):
        if (GAME_PLAYER == GamePlayer.NEAT.value):
            norm_inputs = self.get_inputs(pipe)
            action = self.think(norm_inputs)
            self.move(action, dt)

        if (GAME_TYPE == GameType.DYNAMIC.value):
            self.velocity += GRAVITY * dt
            self.body.centery += int(self.velocity)

    def update_animation(self, dt: float):
        image = self.physicsController.animation(self)
        surface = self.graphics.assets[image]

        rotated_image = pygame.transform.rotate(surface, self.rotation)
        self.graphics.current_surface = rotated_image

        self.pre_pos = self.body.centery
        self.graphics.anchor_point = tuple_2_vec2(self.body.topleft)

    def think(self, inputs: list[float]):
        out = self.brain.get_outputs(inputs)
        return self.physicsController.think(out)

    def closest_pipe(self, pipes: Sequence[Pipe]) -> Pipe:
        for pipe in pipes:
            if pipe.pos_x + PIPE_WIDTH > self.body.topleft[0]:
                return pipe

        return pipes[0]

    def mate(self, parent: Bird):
        child = Bird(self.gh, self.assets)
        child.set_controllers(self.gameController, self.physicsController)
        child.brain = self.brain.crossover(parent.brain)
        return child

    def get_inputs(self, pipe: Pipe):
        inputs: list[float] = []
        inputs.append((SCREEN_HEIGHT - self.body.centery) / SCREEN_HEIGHT)                      # distance ground
        inputs.append((pipe.pos_x + PIPE_WIDTH - self.body.topleft[0]) / SCREEN_WIDTH)          # distance first pipe
        inputs.append((self.body.bottomleft[1] - pipe.top_rect.bottomleft[1]) / SCREEN_HEIGHT)  # distance to top pipe
        inputs.append((pipe.bottom_rect.topleft[1] - self.body.topleft[1]) / SCREEN_HEIGHT)     # distance to bottom pipe
        return inputs

    def move(self, input: ActionState, dt: float):
        if self.dead:
            return

        if input == ActionState.UP:
            self.body.centery -= int(BIRD_SPEED * dt)
        if input == ActionState.DOWN:
            self.body.centery += int(BIRD_SPEED * dt)
        if input == ActionState.STAY:
            pass

        if input == ActionState.FLY and self.current_fly <= 0:
            self.velocity = -BIRD_FLY_FORCE
            self.current_fly = self.fly_cooldown

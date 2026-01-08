from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller import GameController, PhysicsController

import random

import globals as gl
import pygame
from game_types import ActionState, GamePlayer, GameType, Graphics, Pipe
from neaty import Genome, GenomeHistory, NeatConfig
from utils import Sequence, tuple_2_vec2


class Bird:
    def __init__(self, config: NeatConfig, gh: GenomeHistory, assets: list[list[str]]) -> None:
        self.physicsController: PhysicsController
        self.gameController: GameController

        self.pre_action_state = ActionState.STAY

        self.assets: list[list[str]] = assets

        self.gh = gh
        self.config = config

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

        self.body = pygame.Rect(
            gl.SCREEN_WIDTH * 0.3 - gl.BIRD_SIZE / 2,
            gl.SCREEN_HEIGHT / 2 - gl.BIRD_SIZE / 2,
            gl.BIRD_SIZE,
            gl.BIRD_SIZE,
        )
        self.graphics = Graphics(self.body)
        self.graphics.animation_speed = gl.BIRD_ANIMATION_SPEED

        self.brain = Genome(self.config, self.gh)
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
            scale_factor = gl.BIRD_SIZE / img.get_width()
            scaled_img = pygame.transform.scale_by(img, scale_factor)
            self.body.height = scaled_img.get_height()
            self.graphics.assets.append(scaled_img)

    def update(self, inputs: Sequence[Pipe], dt: float):
        pipe = self.closest_pipe(inputs)

        if pipe.top_rect.colliderect(self.body) or pipe.bottom_rect.colliderect(self.body) or self.body.bottomleft[1] >= gl.SCREEN_HEIGHT or self.body.topleft[1] < 0:
            self.dead = True

        if self.dead:
            return

        self.fitness += 1

        if self.current_fly > 0:
            self.current_fly -= dt

        self.update_movement(pipe, dt)
        self.update_animation(dt)

    def update_movement(self, pipe: Pipe, dt: float):
        if gl.GAME_PLAYER == GamePlayer.NEAT.value:
            norm_inputs = self.get_inputs(pipe)
            action = self.think(norm_inputs)
            self.move(action, dt)

        if gl.GAME_TYPE == GameType.DYNAMIC.value:
            self.velocity += gl.GRAVITY * dt
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
            if pipe.pos_x + gl.PIPE_WIDTH > self.body.topleft[0]:
                return pipe

        return pipes[0]

    def mate(self, parent: Bird):
        child = Bird(self.config, self.gh, self.assets)
        child.set_controllers(self.gameController, self.physicsController)
        child.brain = self.brain.crossover(parent.brain)
        return child

    def get_inputs(self, pipe: Pipe):
        inputs: list[float] = []
        inputs.append((gl.SCREEN_HEIGHT - self.body.centery) / gl.SCREEN_HEIGHT)  # distance ground
        inputs.append((pipe.pos_x + gl.PIPE_WIDTH - self.body.centerx) / gl.SCREEN_WIDTH)  # distance first pipe
        inputs.append((self.body.topleft[1] - pipe.top_rect.bottomleft[1]) / gl.SCREEN_HEIGHT)  # distance to top pipe
        inputs.append((pipe.bottom_rect.topleft[1] - self.body.bottomleft[1]) / gl.SCREEN_HEIGHT)  # distance to bottom pipe
        return inputs

    def move(self, input: ActionState, dt: float):
        if self.pre_action_state != input:
            self.pre_action_state = input
            self.fitness -= 1

        if input == ActionState.UP:
            self.body.centery -= int(gl.BIRD_SPEED * dt)
        if input == ActionState.DOWN:
            self.body.centery += int(gl.BIRD_SPEED * dt)
        if input == ActionState.FLY and self.current_fly <= 0:
            self.velocity = -gl.BIRD_FLY_FORCE
            self.current_fly = gl.BIRD_FLY_COOLDOWN

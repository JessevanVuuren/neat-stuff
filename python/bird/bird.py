from __future__ import annotations

from game_types import *
from neat_ref import *
from globals import *

import random
import pygame


class Bird:
    def __init__(self, assets: list[list[str]]) -> None:
        self.assets: list[list[str]] = assets
        self.fly_cooldown = .15

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

        self.set_sprites(self.assets)

    def set_sprites(self, sprites: list[list[str]]):
        self.assets = sprites

        color_sprites = random.choice(self.assets)
        for sprite in color_sprites:
            img = pygame.image.load(sprite)
            scale_factor = BIRD_SIZE / img.get_width()
            scaled_img = pygame.transform.scale_by(img, scale_factor)
            self.body.height = scaled_img.get_height()
            self.graphics.assets.append(scaled_img)

    def update(self, inputs: Sequence[Pipe], dt: float, gravity:bool):
        pipe = self.closest_pipe(inputs)

        if (pipe.top_rect.colliderect(self.body) or pipe.bottom_rect.colliderect(self.body) or self.body.bottomleft[1] >= SCREEN_HEIGHT or self.body.topleft[1] < 0):
            self.dead = True

        if self.dead:
            return

        if self.current_fly > 0:
            self.current_fly -= dt

        self.update_movement(pipe, dt)
        self.update_animation(dt, gravity)

    def update_movement(self, pipe: Pipe, dt: float):
        if (GAME_TYPE == GameType.DYNAMIC.value):
            self.velocity += GRAVITY * dt
            self.body.centery += int(self.velocity)

    def update_animation(self, dt: float, gravity: bool):
        dy = self.pre_pos - self.body.centery

        if (dy > 0):
            self.rotation = 45
            image = 0
        elif (dy == 0):
            image = 1
        else:
            self.rotation -= self.velocity * ROTATION_SCALE
            image = 2

        surface = self.graphics.assets[image]

        rotated_image = pygame.transform.rotate(surface, self.rotation)
        self.graphics.current_surface = rotated_image

        self.pre_pos = self.body.centery
        self.graphics.anchor_point = tuple_2_vec2(self.body.topleft)

    def closest_pipe(self, pipes: Sequence[Pipe]) -> Pipe:
        for pipe in pipes:
            if pipe.pos_x + PIPE_WIDTH > self.body.topleft[0]:
                return pipe

        return pipes[0]

    def get_inputs(self, pipe: Pipe):
        inputs: list[float] = []
        inputs.append((SCREEN_HEIGHT - self.body.centery) / SCREEN_HEIGHT)                      # distance ground
        inputs.append((pipe.pos_x + PIPE_WIDTH - self.body.centerx) / SCREEN_WIDTH)             # distance first pipe
        inputs.append((self.body.topleft[1] - pipe.top_rect.bottomleft[1]) / SCREEN_HEIGHT)     # distance to top pipe
        inputs.append((pipe.bottom_rect.topleft[1] - self.body.bottomleft[1]) / SCREEN_HEIGHT)  # distance to bottom pipe
        return inputs

    def move(self, input: ActionState, dt: float):

        if input == ActionState.UP:
            self.body.centery -= int(BIRD_SPEED * dt)
        if input == ActionState.DOWN:
            self.body.centery += int(BIRD_SPEED * dt)
        if input == ActionState.FLY and self.current_fly <= 0:
            self.velocity = -BIRD_FLY_FORCE
            self.current_fly = self.fly_cooldown

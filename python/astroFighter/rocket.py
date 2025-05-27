from __future__ import annotations

from game_types import *
from particles import *
from globals import *
from utils import *
from coin import *

import pygame
import math


class Rocket(Entity):

    def __init__(self, x: float, y: float, image: pygame.Surface, ps: ParticleSystem, training_mode:bool=False):
        Entity.__init__(self, pygame.Vector2(x, y), image.get_rect().w, image.get_rect().h, 0)
        self.training_mode = training_mode
        self.idle_time = 0.0

        self.velocity = 0
        self.coins = 0
        self.ps = ps

        self.smoke_trail = 10

        self.graphic = Graphic(image, self.pos)
        self.image = image

        self.smokeRange = gradient_color("white", "#181818", 60)
        self.exhaustRange = gradient_color("red", "yellow", 60)

        self.left_thrust_pos = Vector2(-25, -31.4)
        self.right_thrust_pos = Vector2(-25, 31.4)
        self.middle_thrust_pos = Vector2(-25, 0)

    def update(self, delta_time: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.thrust_effect(self.middle_thrust_pos)
            self.velocity = min(self.velocity + ACCELERATION, MAX_VELOCITY)
        elif (self.velocity > 0):
            self.velocity = self.velocity * math.pow((1 - BRAKE_FORCE), delta_time)
        else:
            self.velocity = 0

        if keys[pygame.K_a]:
            self.thrust_effect(self.right_thrust_pos)
            self.angle -= ROTATION_VELOCITY
        if keys[pygame.K_d]:
            self.thrust_effect(self.left_thrust_pos)
            self.angle += ROTATION_VELOCITY

        self.update_graphic()
        self.move()
        self.wrap()

    def update_neat(self, delta_time: float, inputs: list[float]):
        self.idle_time += delta_time
        if inputs[0] > .5:
            self.idle_time = 0.0

        if inputs[0] > .5:
            self.thrust_effect(self.middle_thrust_pos)
            self.velocity = min(self.velocity + ACCELERATION, MAX_VELOCITY)
        elif (self.velocity > 0):
            self.velocity = self.velocity * math.pow((1 - BRAKE_FORCE), delta_time)
        else:
            self.velocity = 0

        if inputs[1] > .5:
            self.thrust_effect(self.right_thrust_pos)
            self.angle -= ROTATION_VELOCITY
        if inputs[2] > .5:
            self.thrust_effect(self.left_thrust_pos)
            self.angle += ROTATION_VELOCITY

        self.update_graphic()
        self.move()
        self.wrap()

    def thrust_effect(self, pos: Vector2):
        if self.training_mode:
            return
        x, y = pos
        self.ps.add_particle(ParticleExhaust(self, x, y, 3, .1, self.exhaustRange, 4, 30))
        self.ps.add_particle(ParticleSmoke(self, x - 39, y * 1.2, 4, 1, self.smokeRange, 15))

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity

        self.pos.x += vertical
        self.pos.y += horizontal

    def update_graphic(self):
        self.graphic.surface = pygame.transform.rotate(self.image, -self.angle - 90)
        rect = self.graphic.surface.get_rect(center=self.image.get_rect(topleft=(self.pos.x, self.pos.y)).center)
        self.graphic.anchor_point = tuple_2_vec2(rect.topleft)

from __future__ import annotations

from particles import ParticleSystem, ParticleExhaust, ParticleSmoke
from game_types import *
from globals import *
from utils import *

import pygame
import math


class Spaceship(Entity):
    def __init__(self, x: float, y: float, image: pygame.Surface, ps: ParticleSystem):
        Entity.__init__(self, pygame.Vector2(x, y), image.get_rect().w, image.get_rect().h, 0)

        self.velocity = Vector2(0, 0)
        self.mass = 1.0

        self.thrust_force = 1000.0
        self.rotate_speed = 200.0
        self.max_force = 1000
        self.magic_drag = .995

        self.coins = 0
        self.ps = ps

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
            force_x = math.cos(self.angle * 0.0174532925) * self.thrust_force
            force_y = math.sin(self.angle * 0.0174532925) * self.thrust_force

            acceleration_force_x = force_x / self.mass
            acceleration_force_y = force_y / self.mass

            self.velocity.x += acceleration_force_x * delta_time
            self.velocity.y += acceleration_force_y * delta_time

            self.velocity.x = clamp(self.velocity.x, -self.max_force, self.max_force)
            self.velocity.y = clamp(self.velocity.y, -self.max_force, self.max_force)

            self.thrust_effect(self.middle_thrust_pos)

        if keys[pygame.K_a]:
            self.thrust_effect(self.right_thrust_pos)
            self.angle -= self.rotate_speed * delta_time
        if keys[pygame.K_d]:
            self.thrust_effect(self.left_thrust_pos)
            self.angle += self.rotate_speed * delta_time

        self.pos += self.velocity * delta_time
        self.velocity *= self.magic_drag
        print(self.velocity.x)

        self.update_graphic()
        self.wrap()

    def thrust_effect(self, pos: Vector2):
        x, y = pos
        self.ps.add_particle(ParticleExhaust(self, x, y, 3, .1, self.exhaustRange, 4, 30))
        self.ps.add_particle(ParticleSmoke(self, x - 39, y * 1.2, 4, 1, self.smokeRange, 15))

    def update_graphic(self):
        self.graphic.surface = pygame.transform.rotate(self.image, -(self.angle) - 90)

        rect = self.graphic.surface.get_rect(center=self.image.get_rect(topleft=(self.pos.x, self.pos.y)).center)
        self.graphic.anchor_point = tuple_2_vec2(rect.topleft)

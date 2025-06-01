from __future__ import annotations

from game_types import *
from neat_ref import *
from globals import *
from utils import *
import pygame
import random
import math


class ParticleSystem:
    def __init__(self) -> None:
        self.particles: list[Particle] = []

    def add_particle(self, particle: Particle):
        self.particles.append(particle)

    def update(self, dt: float):
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update(dt)

class Star(Particle):
    def __init__(self, pos: Vec2, size: float, ttl: float, color: str, pulse: FMinMax, speed: float) -> None:
        super().__init__(pos, size, ttl, color)
        self.color = pygame.Color(color)
        self.pulse = pulse
        self.speed = speed

    def update(self, dt: float):
        self.ttl += .01
        color_value = int((math.cos(self.ttl * self.speed) + 1) * self.pulse.max + self.pulse.min)
        color_value = clamp(color_value, 0, 255)
        self.color.a = int(color_value)

class StarSystem:
    def __init__(self, amount: int, pulse: FMinMax, size: FMinMax, speed: FMinMax, colors: list[str]):
        self.stars: list[Particle] = []

        for _ in range(amount):
            pos_x = random.randint(0, SCREEN_WIDTH)
            pos_y = random.randint(0, SCREEN_HEIGHT)

            star_size = random.random() * size.max + size.min
            star_speed = random.random() * speed.max + speed.min

            star_color = random.choice(colors)

            self.stars.append(Star(Vec2(pos_x, pos_y), star_size, 0, star_color, pulse * 128, star_speed))

    def update(self, delta_time: float):
        for star in self.stars:
            star.update(delta_time)


class ParticleExhaust(Particle):
    def __init__(self, rocked: Entity, x: float, y: float, size: float, ttl: float, color_range: list[str], force: float, arc: int) -> None:
        self.color = color_range[random.randint(0, len(color_range) - 1)]
        super().__init__(Vec2(x, y), size, ttl, self.color)

        self.cone = random.randrange(0, arc) - arc//2
        self.rocked = rocked
        self.force = force
        self.moving = 0

        self.x = x
        self.y = y

    def update(self, dt: float):
        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False

        rotation = math.radians(self.rocked.angle + self.cone)
        offset_pos = self.rocked.rotate_from_origin(self.x, self.y)

        self.moving += self.force

        self.pos.y = offset_pos.y - self.moving * math.sin(rotation)
        self.pos.x = offset_pos.x - self.moving * math.cos(rotation)

class ParticleSmoke(Particle):
    def __init__(self, rocked: Entity, x: float, y: float, size: float, ttl: float, color_range: list[str], width: int) -> None:
        super().__init__(Vec2(x, y), size, ttl, color_range[0])
        self.alive_time = ttl
        self.color_range = color_range
        self.color = color_range[0]

        self.gradient_count = 0
        new_off = random.randint(0, width) - width // 2

        self.pos = rocked.rotate_from_origin(x, y + new_off)

    def update(self, dt: float):
        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False

        val = map(self.alive_time - self.ttl, 0, self.alive_time, 0, len(self.color_range))
        val = clamp(val, 0, len(self.color_range) - 1)
        self.color = self.color_range[int(val)]

from __future__ import annotations

from game_types import Entity
from neat_ref import *
from utils import *
import pygame
import random
import math


class Particle(ABC):
    def __init__(self, x: float, y: float, size: float, ttl: float, color: str) -> None:
        self.pos = pygame.Vector2(x, y)

        self.alive = True
        self.color = color
        self.size = size
        self.ttl = ttl

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass

    def is_alive(self):
        return self.alive


class ParticleExhaust(Particle):
    def __init__(self, rocked:Entity, x: float, y: float, size: float, ttl: float, color_range: list[str], force: float, arc: int) -> None:
        self.color = color_range[random.randint(0, len(color_range) - 1)]
        super().__init__(x, y, size, ttl, self.color)

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
        x, y = self.rocked.rotate_from_origin(self.x, self.y)

        self.moving += self.force

        self.pos.y = y - self.moving * math.sin(rotation)
        self.pos.x = x - self.moving * math.cos(rotation)

    def draw(self, surface: pygame.Surface):
        if not self.alive:
            return

        pygame.draw.circle(surface, self.color, self.pos, self.size)


class ParticleSystem:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.particles: list[Particle] = []

    def add_particle(self, particle: Particle):
        self.particles.append(particle)

    def update(self, dt: float):
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update(dt)

    def draw(self, surface: pygame.Surface):
        for particle in self.particles:
            particle.draw(surface)

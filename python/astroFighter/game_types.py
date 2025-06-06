from __future__ import annotations
from abc import ABC, abstractmethod

from dataclasses import dataclass
from pygame import Surface
from neat_ref import *
from globals import *

import math
import uuid


@dataclass
class Vec2:
    x: float
    y: float

    def distance(self, v: Vec2):
        d = math.pow(v.x - self.x, 2) + math.pow(v.y - self.y, 2)
        return math.sqrt(d)

    def __sub__(self, v: Vec2):
        return Vec2(self.x - v.x, self.y - v.y)

    def _magnitude_squared(self):
        return self.x * self.x + self.y * self.y

    def copy(self):
        return Vec2(self.x, self.y)

    def norm(self):
        length = math.sqrt(self._magnitude_squared())
        if length == 0:
            return Vec2(0, 0)
        return Vec2(self.x / length, self.y / length)


@dataclass
class SpaceMan:
    gameobject: GameObject
    brain: Genome
    idle_time = 0.0

    def extract(self) -> tuple[Entity, Graphic, Genome]:
        return (
            self.gameobject.player,
            self.gameobject.graphics,
            self.brain
        )


@dataclass
class Square:
    x: float
    y: float
    w: float
    h: float

    def overlap(self, b: Square) -> bool:

        if self.x + self.w <= b.x or b.x + b.w <= self.x:
            return False

        if self.y + self.h <= b.y or b.y + b.h <= self.y:
            return False

        return True


@dataclass
class GameObject:
    player: Entity
    graphics: Graphic


@dataclass
class Graphic:
    surface: Surface
    entity: Entity
    angle_offset: float = 0.0


@dataclass
class FMinMax:
    min: float
    max: float

    def __mul__(self, amount: float):
        return FMinMax(self.min * amount, self.max * amount)


@dataclass
class IMinMax:
    min: int
    max: int


class Entity(ABC):
    @property
    def angle(self) -> float:
        return self._angle

    @property
    def pos(self) -> Vec2:
        return self._pos

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @pos.setter
    def pos(self, vec: Vec2):
        self._pos = vec

    @angle.setter
    def angle(self, value: float):
        self._angle = value

    @property
    def coins(self) -> int:
        return self._coins

    @coins.setter
    def coins(self, amount: int):
        self._coins = amount

    @property
    def id(self) -> str:
        return str(self._id)

    def __init__(self, pos: Vec2, width: float, height: float, angle: float):
        self._pos = pos
        self._width = width
        self._height = height
        self._angle = angle
        self._coins = 0
        self._id = uuid.uuid4()

    def set_xy(self, x: float, y: float):
        self.pos = Vec2(x, y)

    @abstractmethod
    def update(self, inputs: list[bool], delta_time: float): ...

    def center(self):
        center_x = self.pos.x + self._width / 2
        center_y = self.pos.y + self._height / 2
        return Vec2(center_x, center_y)

    def rotate_from_origin(self, x_offset: float, y_offset: float):
        angle_radians = math.radians(self._angle)

        origin_x = self.pos.x + self._width / 2
        origin_y = self.pos.y + self._height / 2

        new_point_x = origin_x + x_offset
        new_point_y = origin_y + y_offset

        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)

        new_x1 = (new_point_x - origin_x) * cos - (new_point_y - origin_y) * sin + origin_x
        new_y1 = (new_point_x - origin_x) * sin + (new_point_y - origin_y) * cos + origin_y

        return Vec2(new_x1, new_y1)

    def rotate(self, delta_angle: float):
        self._angle += delta_angle

    def set_rotation(self, angle: float):
        self._angle = angle

    def get_square(self) -> Square:
        return Square(self._pos.x, self._pos.y, self._width, self._height)

    def wrap(self):
        if (self.pos.x > SCREEN_WIDTH):
            self.pos = Vec2(-self.width, self.pos.y)
        if (self.pos.y > SCREEN_HEIGHT):
            self.pos = Vec2(self.pos.x, -self.height)
        if (self.pos.x < -self.width):
            self.pos = Vec2(SCREEN_WIDTH, self.pos.y)
        if (self.pos.y < -self.height):
            self.pos = Vec2(self.pos.x, SCREEN_HEIGHT)


class Particle(ABC):
    def __init__(self, pos: Vec2, size: float, ttl: float, color: str) -> None:
        self.pos = pos

        self.alive = True
        self.color = color
        self.size = size
        self.ttl = ttl

    @abstractmethod
    def update(self, dt: float):
        pass

    def is_alive(self):
        return self.alive

    def get_square(self):
        return Square(self.pos.x, self.pos.y, self.size, self.size)

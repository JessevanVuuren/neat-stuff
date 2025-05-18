from __future__ import annotations

from pygame import Surface, Vector2, Rect
from dataclasses import dataclass
from neat_ref import *
from globals import *
from utils import *

import math


@dataclass
class Graphic:
    surface: Surface
    anchor_point: Vector2


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
    def pos(self) -> Vector2:
        return self._pos

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @pos.setter
    def pos(self, vec: Vector2):
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
    def initial_distance(self) -> float:
        return self._initial_distance

    @initial_distance.setter
    def initial_distance(self, amount: float):
        self._initial_distance = amount

    def __init__(self, pos: Vector2, width: float, height: float, angle: float):
        self._pos = pos
        self._width = width
        self._height = height
        self._angle = angle
        self._coins = 0
        self._initial_distance = 0.0

    def set_xy(self, x: float, y: float):
        self.pos = Vector2(x, y)

    @abstractmethod
    def update(self, delta_time: float): ...

    def center(self):
        center_x = self.pos.x + self._width / 2
        center_y = self.pos.y + self._height / 2
        return Vector2(center_x, center_y)

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

        return Vector2(new_x1, new_y1)

    def rotate(self, delta_angle: float):
        self._angle += delta_angle

    def set_rotation(self, angle: float):
        self._angle = angle

    def get_rect(self) -> Rect:
        return Rect(self._pos.x, self._pos.y, self._width, self._height)

    def wrap(self):
        if (self.pos.x > SCREEN_WIDTH):
            self.pos = Vector2(-self.width, self.pos.y)
        if (self.pos.y > SCREEN_HEIGHT):
            self.pos = Vector2(self.pos.x, -self.height)
        if (self.pos.x < -self.width):
            self.pos = Vector2(SCREEN_WIDTH, self.pos.y)
        if (self.pos.y < -self.height):
            self.pos = Vector2(self.pos.x, SCREEN_HEIGHT)

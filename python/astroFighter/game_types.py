from __future__ import annotations

from pygame import Surface, Vector2, Rect
from dataclasses import dataclass
from neat_ref import *
from utils import *

import math


@dataclass
class Graphic:
    surface: Surface
    anchor_point: Vector2


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

    def __init__(self, pos: Vector2, width: float, height: float, angle: float):
        self._pos = pos
        self._width = width
        self._height = height
        self._angle = angle

    def set_xy(self, x: float, y: float):
        self.pos = Vector2(x, y)

    @abstractmethod
    def update(self, delta_time:float): ...

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

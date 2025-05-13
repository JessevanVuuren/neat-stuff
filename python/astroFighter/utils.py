from pygame import Vector2, Surface, transform
from abc import ABC, abstractmethod  # type: ignore
from colour import Color  # type: ignore
from typing import Tuple
from game_types import *
import random

def random_color(startC: str, endC: str, amount: int) -> str:
    index = random.randint(0, amount - 1)
    range = list(Color(startC).range_to(Color(endC), amount))  # type: ignore
    return range[index].get_hex_l()


def gradient_color(startC: str, endC: str, amount: int) -> list[str]:
    range = list(Color(startC).range_to(Color(endC), amount))  # type: ignore
    return [color.get_hex_l() for color in range]


def tuple_2_vec2(t: Tuple[int, int]) -> Vector2:
    return Vector2(t[0], t[1])


def vec2_2i_tuple(v: Vector2) -> Tuple[int, int]:
    return (int(v.x), int(v.y))


def vec2_2f_tuple(v: Vector2) -> Tuple[float, float]:
    return (v.x, v.y)


def img_scaler(img: Surface, factor: float) -> Surface:
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return transform.scale(img, size)

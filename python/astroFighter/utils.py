import os
import random
from typing import Tuple

from colour import Color
from game_types import Vec2
from pygame import Surface, Vector2, transform


def random_color(startC: str, endC: str, amount: int) -> str:
    index = random.randint(0, amount - 1)
    range = list(Color(startC).range_to(Color(endC), amount))  # type: ignore
    return range[index].get_hex_l()


def gradient_color(startC: str, endC: str, amount: int) -> list[str]:
    range = list(Color(startC).range_to(Color(endC), amount))  # type: ignore
    return [color.get_hex_l() for color in range]


def tuple_2_vec2(t: Tuple[int, int]) -> Vec2:
    return Vec2(t[0], t[1])


def vec2_2i_tuple(v: Vector2) -> Tuple[int, int]:
    return (int(v.x), int(v.y))


def vec2_2f_tuple(v: Vector2) -> Tuple[float, float]:
    return (v.x, v.y)


def vec2_2_vector2(v: Vec2) -> Vector2:
    return Vector2(v.x, v.y)


def scale_to_pixels(img: Surface, size: Vector2):
    return transform.scale(img, size)


def img_scaler(img: Surface, factor: float) -> Surface:
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return transform.scale(img, size)


def map(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clamp(x: float, min_value: float, max_value: float) -> float:
    return min(max_value, max(x, min_value))


def absolute_path(file: str):
    script_dir = os.path.dirname(__file__)
    img_path = os.path.abspath(os.path.join(script_dir, file))
    return img_path

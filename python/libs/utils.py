from typing import Protocol, Self, List, Type, Sequence, TypeVar, Optional, Tuple  # type: ignore
from dataclasses import dataclass, field  # type: ignore
from enum import Enum  # type: ignore
import pygame


def tuple_2_vec2(t: Tuple[int, int]) -> pygame.Vector2:
    return pygame.Vector2(t[0], t[1])


def vec2_2i_tuple(v: pygame.Vector2) -> Tuple[int, int]:
    return (int(v.x), int(v.y))


def vec2_2f_tuple(v: pygame.Vector2) -> Tuple[float, float]:
    return (v.x, v.y)

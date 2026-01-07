from typing import Protocol, Self, List, Type, Sequence, TypeVar, Optional, Tuple, Callable  # type: ignore
from dataclasses import dataclass, field  # type: ignore
from abc import ABC, abstractmethod  # type: ignore
from enum import Enum, EnumMeta  # type: ignore
from pygame import Vector2


class MetaEnum(EnumMeta):
    def __contains__(cls, item):  # type: ignore
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


def tuple_2_vec2(t: Tuple[int, int]) -> Vector2:
    return Vector2(t[0], t[1])


def vec2_2i_tuple(v: Vector2) -> Tuple[int, int]:
    return (int(v.x), int(v.y))


def vec2_2f_tuple(v: Vector2) -> Tuple[float, float]:
    return (v.x, v.y)

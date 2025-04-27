from __future__ import annotations
from neat_ref import *
import pygame


class Agent(Protocol):
    dead: bool
    fitness: float
    brain: Genome
    graphics:Graphics


    def __init__(self, gh: GenomeHistory): ...
    def mate(self, parent: Self) -> Self: ...
    def update(self, inputs: Sequence[Pipe], dt: float): ...

@dataclass
class Graphics:
    body: pygame.Rect
    color: str = "#ffffff"


class Pipe(Protocol):
    top_rect: pygame.Rect
    bottom_rect: pygame.Rect
    width: float
    height: float
    pos_x: float

    def update(self, dt: float): ...


class ActionState(Enum):
    UP = 0
    DOWN = 1
    STAY = 2

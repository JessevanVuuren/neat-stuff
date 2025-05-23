from __future__ import annotations

from neat_ref import *

import pygame

@dataclass
class FlyBird:
    body: Bird
    brain: Genome

@dataclass
class Graphics:
    body: pygame.Rect
    current_image = 0.0
    animation_speed = 0.0
    color: str = "#ffffff"
    current_surface: pygame.Surface | None = None
    assets: list[pygame.Surface] = field(default_factory=lambda: [])
    anchor_point: pygame.Vector2 = field(default_factory=lambda: pygame.math.Vector2(0, 0))



class Pipe(Protocol):
    top_rect: pygame.Rect
    bottom_rect: pygame.Rect
    pos_x: float

    def update(self, dt: float): ...


class GameType(BaseEnum):
    STATIC = "static"
    DYNAMIC = "dynamic"


class GamePlayer(BaseEnum):
    MANUAL = "manual"
    NEAT = "neat"


class ActionState(Enum):
    UP = 0
    DOWN = 1
    STAY = 2
    FLY = 3


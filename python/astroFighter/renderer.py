from __future__ import annotations

from game_types import *
from globals import *

import pygame


class Render:
    def __init__(self, width: int, height: int, typeface: str = "", font_size: int = 30) -> None:
        self.height = height
        self.width = width

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_layer = None
        pygame.font.init()

        if (not typeface):
            typeface = pygame.font.get_default_font()

        self.fontSystem = pygame.font.SysFont(typeface, font_size)

    def set_background(self, img: str, repeat: bool = False, stretch: bool = False):
        self.background_layer = pygame.Surface((self.width, self.height))
        self.background_img = pygame.image.load(img)

        if (stretch):
            scale_factor = self.height / self.background_img.get_height()
            self.background_img = pygame.transform.scale_by(self.background_img, scale_factor)

        if (repeat):
            full_width = 0
            while (full_width < self.width):
                self.background_layer.blit(self.background_img, (full_width, 0))
                full_width += self.background_img.get_width()

    def text(self, text: str, x: float, y: float, color: str = "#ffffff"):
        font = self.fontSystem.render(text, True, color)
        self.screen.blit(font, (x, y))

    def fill(self, color: str = "#ffffff"):
        if (self.background_layer):
            self.screen.blit(self.background_layer, (0, 0))
        else:
            self.screen.fill(color)

    def surface(self, graph: Graphic):
        self.screen.blit(graph.surface, graph.anchor_point)

    def display(self):
        pygame.display.flip()

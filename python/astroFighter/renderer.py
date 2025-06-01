from __future__ import annotations

from game_types import *
from globals import *

import pygame
from utils import vec2_2_vector2

class Render:
    def __init__(self, width: int, height: int, typeface: str = "", font_size: int = 30) -> None:
        self.height = height
        self.width = width

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.alpha = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)

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

    @staticmethod
    def circle(color:str, pos:Vec2, size:float, screen:Surface):
        pygame.draw.circle(screen, color, vec2_2_vector2(pos), size)
        
    def particles(self, particles:list[Particle], alpha:bool=False):
        for particle in particles:
            if (not particle.alive):
                continue
            
            screen = self.screen if not alpha else self.alpha
            self.circle(particle.color, particle.pos, particle.size, screen)
            
            
    def surface(self, graph: Graphic):
        surface = pygame.transform.rotate(graph.surface, -graph.entity.angle + graph.angle_offset)
        rect = surface.get_rect(center=vec2_2_vector2(graph.entity.center()))
        self.screen.blit(surface, rect.topleft)

    def display(self):
        self.screen.blit(self.alpha, (0, 0))
        pygame.display.flip()


import math

import globals as gl
import pygame
from game_types import Graphics


class Render:
    def __init__(self) -> None:
        self.background_layer = None
        self.screen = pygame.display.set_mode((gl.SCREEN_WIDTH, gl.SCREEN_HEIGHT))

    def set_background(self, img: str, repeat: bool = False, stretch: bool = False):
        self.background_layer = pygame.Surface((gl.SCREEN_WIDTH, gl.SCREEN_HEIGHT))
        self.background_img = pygame.image.load(img)

        if stretch:
            scale_factor = gl.SCREEN_HEIGHT / self.background_img.get_height()
            self.background_img = pygame.transform.scale_by(self.background_img, scale_factor)

        if repeat:
            full_width = 0
            while full_width < gl.SCREEN_WIDTH:
                self.background_layer.blit(self.background_img, (full_width, 0))
                full_width += self.background_img.get_width()

    def fill(self, color: str = "#ffffff"):
        if self.background_layer:
            self.screen.blit(self.background_layer, (0, 0))
        else:
            self.screen.fill(color)

    def render(self, graph: Graphics):
        if len(graph.assets) > 0:
            self.screen.blit(graph.assets[0], graph.anchor_point)
        else:
            pygame.draw.rect(self.screen, graph.color, graph.body)

    def graphics_surface(self, graph: Graphics):
        if graph.current_surface:
            self.screen.blit(graph.current_surface, graph.anchor_point)

    def render_animation(self, graph: Graphics):
        image = graph.assets[math.floor(graph.current_image)]
        self.screen.blit(image, graph.anchor_point)

    def display(self):
        pygame.display.flip()

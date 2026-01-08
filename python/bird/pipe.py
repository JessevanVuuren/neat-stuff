import random

import globals as gl
import pygame
from game_types import Graphics, Pipe
from utils import tuple_2_vec2


class PipeObject(Pipe):
    def __init__(self, img: str) -> None:
        self.pipe_image = pygame.image.load(img)

        self.scale_factor = gl.PIPE_WIDTH / self.pipe_image.get_width()

        self.pos_x = gl.SCREEN_WIDTH
        self.height = random.randint(0, gl.SCREEN_HEIGHT - int(gl.PIPE_GAP))

        self.top_rect = pygame.Rect(0, 0, 0, 0)
        self.bottom_rect = pygame.Rect(0, 0, 0, 0)

        self.graphics_top = Graphics(self.top_rect)
        self.graphics_bottom = Graphics(self.bottom_rect)

        self.graphics_top.assets.append(pygame.transform.scale_by(self.pipe_image, self.scale_factor))
        self.graphics_bottom.assets.append(pygame.transform.scale_by(self.pipe_image, self.scale_factor))

        self.graphics_top.assets[0] = pygame.transform.flip(self.graphics_top.assets[0], False, True)
        self.graphics_bottom.assets[0] = pygame.transform.flip(self.graphics_bottom.assets[0], False, False)

    def update(self, dt: float):
        self.pos_x -= gl.PIPE_SPEED * dt

        self.top_rect = pygame.Rect(self.pos_x, 0, gl.PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.pos_x, self.height + gl.PIPE_GAP, gl.PIPE_WIDTH, gl.SCREEN_HEIGHT)

        self.graphics_top.body = self.top_rect
        self.graphics_bottom.body = self.bottom_rect

        self.graphics_top.anchor_point = tuple_2_vec2(self.top_rect.bottomleft)
        self.graphics_top.anchor_point.y -= self.pipe_image.get_height() * self.scale_factor

        self.graphics_bottom.anchor_point = tuple_2_vec2(self.bottom_rect.topleft)

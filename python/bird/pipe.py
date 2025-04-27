from game_types import Pipe
import pygame
import random

class PipeObject(Pipe):
    def __init__(self, screen: pygame.Surface, speed: float, width: float, gap: float, color: str) -> None:
        self.screen = screen
        self.default_color = color
        self.color = color
        self.speed = speed
        self.width = width
        self.gap = gap

        self.pos_x = screen.get_width()
        self.height = random.randint(0, screen.get_height() - int(gap))

        self.top_rect = pygame.Rect(0, 0, 0, 0)
        self.bottom_rect = pygame.Rect(0, 0, 0, 0)

    def update(self, dt: float):
        self.pos_x -= self.speed * dt

        self.top_rect = pygame.Rect(self.pos_x, 0, self.width, self.height)
        self.bottom_rect = pygame.Rect(self.pos_x, self.height + self.gap, self.width, self.screen.get_height())

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.top_rect)
        pygame.draw.rect(self.screen, self.color, self.bottom_rect)
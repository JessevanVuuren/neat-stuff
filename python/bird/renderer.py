from game_types import *
import pygame

class Render:
    def __init__(self, screen:pygame.Surface) -> None:
        self.screen = screen
        
    def render(self, color:str, graph:Graphics):
        
        pygame.draw.rect(self.screen, graph.color, graph.body)

    def renders(self, color:str, rect_s:list[pygame.Rect]):
        for rect in rect_s:
            pygame.draw.rect(self.screen, color, rect)
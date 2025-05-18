from game_types import *
import pygame


class Coin(Entity):
    def __init__(self, pos: Vector2, width: float, height: float, color: str):
        Entity.__init__(self, pos, width, height, 0)
        self.color = color
        self.timer = 0

    def update(self, delta_time: float):
        pass

    def draw(self, surface: Surface):
        pygame.draw.circle(surface, self.color, self.pos, self.height/2)


class CoinSystem:
    def __init__(self, screen: Surface) -> None:
        self.coin = self.spawn_coin(Vector2(SCREEN_WIDTH * .8, SCREEN_HEIGHT // 2))
        self.screen = screen

    def spawn_coin(self, position: Vector2 | None = None) -> Coin:
        if (not position):
            rand_x = random.randint(10, SCREEN_WIDTH - 10)
            rand_y = random.randint(10, SCREEN_HEIGHT - 10)
            position = Vector2(rand_x, rand_y)

        return Coin(position, 10, 10, "#FFDD33")

    def update(self, rocked: Entity):
        if (self.coin.get_rect().colliderect(rocked.get_rect())):
            rocked.coins += 1
            self.coin = self.spawn_coin()
            rocked.initial_distance = rocked.pos.distance_to(self.coin.pos)

        self.coin.draw(self.screen)

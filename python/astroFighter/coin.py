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
    def __init__(self, screen:Surface) -> None:
        self.screen = screen
        self.coins: list[Coin] = []
        self.spawn_coin()

    def spawn_coin(self):
        rand_x = random.randint(10, SCREEN_WIDTH - 10)
        rand_y = random.randint(10, SCREEN_HEIGHT - 10)

        self.coins.append(Coin(Vector2(rand_x, rand_y), 10, 10, "#FFDD33"))

    def update(self, rocked: Entity):
        for coin in self.coins:
            if (coin.get_rect().colliderect(rocked.get_rect())):
                rocked.coins += 1
                self.coins.remove(coin)
                self.spawn_coin()
            
            coin.draw(self.screen)


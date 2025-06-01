from random import randint
from game_types import *


class Coin(Particle):
    def __init__(self, pos: Vec2, size: float, color: str):
        super().__init__(pos, size, 0, color) 

    def update(self, dt: float):
        pass

    def draw(self, surface: Surface):
        pass


class CoinSystem:
    def __init__(self, screen: Surface) -> None:
        self.coins: dict[str, Coin] = {}
        self.entitys: list[Entity] = []
        self.screen = screen

    def set_entitys(self, entitys: list[Entity]):
        self.entitys = entitys
        self.reset_coins()
        self.init_coins()

    def reset_coins(self):
        self.coins = {}

    def init_coins(self):
        for agent in self.entitys:
            self.spawn_coin(agent)

    def spawn_coin(self, agent: Entity):
        x = randint(10, SCREEN_WIDTH - 10)
        y = randint(10, SCREEN_HEIGHT - 10)

        self.coins[agent.id] = Coin(Vec2(x, y), 5, "#FFDD33")

    def update(self, agent: Entity):
        if (self.coins[agent.id].get_square().overlap(agent.get_square())):
            agent.coins += 1

            self.spawn_coin(agent)

    def draw(self):
        for coin in self.coins.values():
            coin.draw(self.screen)

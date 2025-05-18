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
        self.coins: dict[str, Coin] = {}
        self.agents: list[Entity] = []
        self.screen = screen

        self.start_pos = Vector2(SCREEN_WIDTH * .8, SCREEN_HEIGHT // 2)

    def set_agents(self, agents: list[Entity]):
        self.agents = agents
        self.reset_coins()
        self.init_coins()

    def reset_coins(self):
        self.coin_positions = [self.start_pos]
        self.coins = {}

    def init_coins(self):
        for agent in self.agents:
            self.spawn_coin(agent)

    def spawn_coin(self, agent: Entity):
        x = random.randint(10, SCREEN_WIDTH - 10)
        y = random.randint(10, SCREEN_HEIGHT - 10)
        pos = Vector2(x, y)
        self.coins[agent.id] = Coin(pos, 10, 10, "#FFDD33")

    def update(self, agent: Entity):
        if (self.coins[agent.id].get_rect().colliderect(agent.get_rect())):
            agent.coins += 1

            self.spawn_coin(agent)

    def draw(self):
        for coin in self.coins.values():
            coin.draw(self.screen)

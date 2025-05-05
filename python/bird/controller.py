from population_bird import Population
from renderer import Render
from game_types import *
from neat_ref import *


class GameController:
    @abstractmethod
    def update(self, pipes: Sequence[Pipe], dt: float): ...

    @abstractmethod
    def handle_inputs(self, dt: float): ...

    @abstractmethod
    def reset(self): ...


class ManualController(GameController):
    def __init__(self, bird: Agent, render: Render) -> None:
        self.bird = bird
        self.render = render

    def update(self, pipes: Sequence[Pipe], dt: float):
        self.bird.update(pipes, dt)
        self.render.graphics_surface(self.bird.graphics)

    def handle_inputs(self, dt: float):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.bird.move(ActionState.UP, dt)
        if keys[pygame.K_s]:
            self.bird.move(ActionState.DOWN, dt)
        if keys[pygame.K_SPACE]:
            self.bird.move(ActionState.FLY, dt)

    def reset(self):
        self.bird.reset()


class NeatController(GameController):
    def __init__(self, population: Population, render: Render) -> None:
        self.population = population
        self.render = render

    def update(self, pipes: Sequence[Pipe], dt: float):
        self.population.update(pipes, dt)

        for bird in self.population.population:
            if (not bird.dead):
                self.render.graphics_surface(bird.graphics)

    def handle_inputs(self, dt: float):
        pass

    def reset(self):
        self.population.display_stats()
        self.population.reset()
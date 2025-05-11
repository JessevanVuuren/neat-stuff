from __future__ import annotations

from population_bird import *
from renderer import Render
from game_types import *
from neat_ref import *
from globals import *


class GameController:
    @abstractmethod
    def update(self, pipes: Sequence[Pipe], dt: float): ...

    @abstractmethod
    def handle_inputs(self, dt: float): ...

    @abstractmethod
    def reset(self): ...


class ManualController(GameController):
    def __init__(self, bird: Bird, render: Render) -> None:
        self.bird = bird
        self.render = render

    def update(self, pipes: Sequence[Pipe], dt: float):
        self.bird.update(pipes, dt)
        self.render.graphics_surface(self.bird.graphics)

    def handle_inputs(self, dt: float):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.bird.move(ActionState.UP, dt)
        elif keys[pygame.K_s]:
            self.bird.move(ActionState.DOWN, dt)
        elif keys[pygame.K_SPACE]:
            self.bird.move(ActionState.FLY, dt)
        else:
            self.bird.move(ActionState.STAY, dt)


    def reset(self):
        self.bird.reset()


class NeatController(GameController):
    def __init__(self, population: PopulationBird, render: Render) -> None:
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


class PhysicsController:
    @abstractmethod
    def think(self, out: list[float]) -> ActionState: ...

    @abstractmethod
    def animation(self, bird: Bird) -> int: ...

    @abstractmethod
    def movement(self, bird: Bird) -> int: ...


class StaticController(PhysicsController):
    def think(self, out: list[float]):
        index = out.index(max(out))
        return ActionState(index)

    def animation(self, bird: Bird):
        dy = bird.pre_pos - bird.body.centery

        match dy:
            case d if d > 0:
                bird.rotation = 45
                return 0
            case 0:
                bird.rotation = 0
                return 1
            case _:
                bird.rotation = -45
                return 2


class DynamicController(PhysicsController):
    def think(self, out: list[float]) -> ActionState:
        if (out[0] > .5):
            return ActionState.FLY
        else:
            return ActionState.STAY

    def animation(self, bird: Bird):
        dy = bird.pre_pos - bird.body.centery

        match dy:
            case d if d > 0:
                bird.rotation = 45
                return 0
            case 0:
                return 1
            case _:
                bird.rotation -= bird.velocity * BIRD_ROTATION_SCALE
                return 2

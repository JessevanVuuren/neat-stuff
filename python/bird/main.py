from __future__ import annotations

from population_bird import PopulationBird
from renderer import Render
from pipe import PipeObject
from controller import (
    DynamicController,
    GameController,
    ManualController,
    NeatController,
    PhysicsController,
    StaticController,
)
from game_types import ActionState, GameType, GamePlayer
import globals as gl
from neaty import Config, NeatConfig, GenomeHistory
from bird import Bird

import pygame

pygame.init()

assert gl.GAME_TYPE in GameType
assert gl.GAME_PLAYER in GamePlayer

clock = pygame.time.Clock()
running = True
dt = 0

bird_sprites = [
    [
        "./assets/redbird-downflap.png",
        "./assets/redbird-midflap.png",
        "./assets/redbird-upflap.png",
    ],
    [
        "./assets/yellowbird-downflap.png",
        "./assets/yellowbird-midflap.png",
        "./assets/yellowbird-upflap.png",
    ],
    [
        "./assets/bluebird-downflap.png",
        "./assets/bluebird-midflap.png",
        "./assets/bluebird-upflap.png",
    ],
]


def quit_actions():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


def manual_inputs():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.move(ActionState.UP, dt)
    if keys[pygame.K_s]:
        player.move(ActionState.DOWN, dt)
    if keys[pygame.K_SPACE]:
        player.move(ActionState.FLY, dt)


config = Config("config", NeatConfig()).parse()
genome_history = GenomeHistory(config)
pop = PopulationBird(config.pop_size, lambda: Bird(config, genome_history, bird_sprites))

render = Render()
render.set_background("./assets/background-day.png", True, True)

player = Bird(config, genome_history, bird_sprites)

physicsController: PhysicsController
match gl.GAME_TYPE:
    case GameType.STATIC.value:
        physicsController = StaticController()
    case GameType.DYNAMIC.value:
        physicsController = DynamicController()
    case _:
        raise ValueError("Unsupported GAME_TYPE mode")

gameController: GameController
match gl.GAME_PLAYER:
    case GamePlayer.NEAT.value:
        gameController = NeatController(pop, render)
    case GamePlayer.MANUAL.value:
        gameController = ManualController(player, render)
    case _:
        raise ValueError("Unsupported GAME_PLAYER mode")

player.set_controllers(gameController, physicsController)
pop.set_controllers(gameController, physicsController)
pop.create_population()


while True:
    pipe = PipeObject("./assets/pipe-green.png")
    last_pipe = pipe
    pipes = [pipe]
    dt = 0

    while not pop.all_dead() and not player.dead:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    force_reset = True

        quit_actions()

        render.fill()

        gameController.update(pipes, dt)
        gameController.handle_inputs(dt)

        if last_pipe.pos_x < gl.SCREEN_WIDTH - gl.PIPE_GAP_BETWEEN - gl.PIPE_WIDTH:
            pipe = PipeObject("./assets/pipe-green.png")
            pipes.append(pipe)
            last_pipe = pipe

        for pipe in pipes:
            pipe.update(dt)
            render.render(pipe.graphics_top)
            render.render(pipe.graphics_bottom)

        if pipes[:1][0].pos_x <= -gl.PIPE_WIDTH:
            pipes.pop(0)

        play_time = clock.tick(gl.FPS)
        dt = play_time / 1000
        render.display()

    gameController.reset()

from __future__ import annotations

from population_bird import Population
from renderer import Render
from pipe import PipeObject
from controller import *
from game_types import *
from neat_ref import *
from globals import *
from bird import Bird

import pygame

pygame.init()

assert (GAME_TYPE in GameType)
assert (GAME_PLAYER in GamePlayer)

clock = pygame.time.Clock()
running = True
dt = 0

bird_sprites = [["./assets/redbird-downflap.png", "./assets/redbird-midflap.png", "./assets/redbird-upflap.png"],
                ["./assets/yellowbird-downflap.png", "./assets/yellowbird-midflap.png", "./assets/yellowbird-upflap.png"],
                ["./assets/bluebird-downflap.png", "./assets/bluebird-midflap.png", "./assets/bluebird-upflap.png"],]


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


genome_history = GenomeHistory(NEAT_INPUTS, NEAT_OUTPUT)
pop = Population(genome_history, NEAT_POP_SIZE, lambda: Bird(genome_history, bird_sprites))

render = Render()
render.set_background("./assets/background-day.png", True, True)

player = Bird(genome_history, bird_sprites)

physicsController: PhysicsController
match GAME_TYPE:
    case GameType.STATIC.value:
        physicsController = StaticController()
    case GameType.DYNAMIC.value:
        physicsController = DynamicController()
    case _:
        raise ValueError("Unsupported GAME_TYPE mode")

gameController: GameController
match GAME_PLAYER:
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
    force_reset = False
    reset = 5000

    while not pop.all_dead() and not player.dead and not force_reset and reset >= 0:
        reset -= 1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    force_reset = True

        quit_actions()

        render.fill()

        gameController.update(pipes, dt)
        gameController.handle_inputs(dt)

        if (last_pipe.pos_x < SCREEN_WIDTH - PIPE_GAP_BETWEEN - PIPE_WIDTH):
            pipe = PipeObject("./assets/pipe-green.png")
            pipes.append(pipe)
            last_pipe = pipe

        for pipe in pipes:
            pipe.update(dt)
            render.render(pipe.graphics_top)
            render.render(pipe.graphics_bottom)

        if (pipes[:1][0].pos_x <= -PIPE_WIDTH):
            pipes.pop(0)

        dt = clock.tick(FPS) / 1000
        render.display()
        clock.tick(FPS)

    print(pop.best_global.fitness)
    pop.best_global.brain.stats_genome()
    gameController.reset()

from __future__ import annotations

from population_bird import Population
from renderer import Render
from pipe import PipeObject
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

bird_sprites = ["./assets/redbird-downflap.png",
                "./assets/redbird-midflap.png", "./assets/redbird-upflap.png"]


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


genome_history = GenomeHistory(4, 1)
pop = Population(genome_history, 100, Bird, bird_sprites)

render = Render()
render.set_background("./assets/background-day.png", True, True)

player = Bird(genome_history)
player.set_sprites(bird_sprites)

while True:
    pipe = PipeObject("./assets/pipe-green.png")
    last_pipe = pipe
    pipes = [pipe]
    dt = 0

    while not player.dead:
        quit_actions()

        render.fill()

        if (GAME_PLAYER == GamePlayer.MANUAL.value):
            player.update(pipes, dt)
            render.graphics_surface(player.graphics)
        if (GAME_PLAYER == GamePlayer.NEAT.value):
            pop.update(pipes, dt)

            for bird in pop.population:
                if (not bird.dead):
                    render.graphics_surface(bird.graphics)

        if (GAME_PLAYER == GamePlayer.MANUAL.value):
            manual_inputs()

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

    if (GAME_PLAYER == GamePlayer.MANUAL.value):
        player.reset()
    if (GAME_PLAYER == GamePlayer.NEAT.value):
        pop.display_stats()
        pop.reset()


from __future__ import annotations

# from population_bird import Population
from renderer import Render
from pipe import PipeObject
from game_types import *
from neat_ref import *
from globals import *
from bird import Bird

import pygame

pygame.init()

clock = pygame.time.Clock()
running = True
dt = 0

def exit_codes(running: bool):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.move(ActionState.UP, dt)
    if keys[pygame.K_s]:
        player.move(ActionState.DOWN, dt)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fly()
        if event.type == pygame.QUIT:
            pygame.quit()

    return running


genome_history = GenomeHistory(4, 3)
# pop = Population(genome_history, 100, Bird)

render = Render()
render.set_background("./assets/background-day.png", True, True)

player = Bird(gh=genome_history)
player.set_sprites(["./assets/redbird-downflap.png", "./assets/redbird-midflap.png", "./assets/redbird-upflap.png"])


while True:
    pipe = PipeObject("./assets/pipe-green.png")
    last_pipe = pipe
    pipes = [pipe]
    dt = 0

    while not player.dead:
        running = exit_codes(running)

        render.fill()
        player.update(pipes, dt, True)

        if (last_pipe.pos_x < SCREEN_WIDTH - PIPE_GAP_BETWEEN - PIPE_WIDTH):
            pipe = PipeObject("./assets/pipe-green.png")
            pipes.append(pipe)
            last_pipe = pipe

        render.render_animation(player.graphics)

        for pipe in pipes:
            pipe.update(dt)
            render.render(pipe.graphics_top)
            render.render(pipe.graphics_bottom)

        if (pipes[:1][0].pos_x <= -PIPE_WIDTH):
            pipes.pop(0)


        dt = clock.tick(FPS) / 1000
        render.display()
        clock.tick(FPS)
        print(clock.get_fps())

    player = Bird(gh=genome_history)

# while True:

#     pipe = PipeObject(pipe_speed, pipe_width, pipe_gap, pipe_color)
#     last_pipe = pipe
#     pipes = [pipe]
#     dt = 0

#     while not pop.all_dead():
#         running = exit_codes(running)

#         render.fill("#264653")

#         pop.update(pipes, dt)

#         if (last_pipe.pos_x < SCREEN_WIDTH - pipe_gap_between - pipe_width):
#             pipe = PipeObject(pipe_speed, pipe_width, pipe_gap, pipe_color)
#             pipes.append(pipe)
#             last_pipe = pipe

#         for bird in pop.population:
#             if (not bird.dead):
#                 render.render(bird.graphics)

#         for pipe in pipes:
#             pipe.update(dt)
#             render.render(pipe.graphics_top)
#             render.render(pipe.graphics_bottom)

#         if (pipes[:1][0].pos_x <= -pipe_width):
#             pipes.pop(0)

#         dt = clock.tick(60) / 1000
#         render.display()
#         clock.tick(60)

#     print("Generation:", pop.generation)
#     print("Best Local:", pop.best_local.fitness)
#     print("Best Global:", pop.best_global.fitness)
#     print()

#     pop.reset()

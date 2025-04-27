from __future__ import annotations

from population_bird import Population
from renderer import Render
from neat_ref import *
from bird import Bird
from pipe import PipeObject
import pygame


HEIGHT = 1280
WIDTH = 720

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
clock = pygame.time.Clock()
running = True
dt = 0

pipe_speed = 200
pipe_width = 50
pipe_gap = 100
pipe_gap_between = 300
pipe_color = "#E9C46A"

bird_color = "#E76F51"


def exit_codes(running: bool):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    return running


genome_history = GenomeHistory(4, 3)
pop = Population(genome_history, 100, Bird)

render = Render(screen)

generation = 0


while True:

    pipe = PipeObject(screen, pipe_speed, pipe_width, pipe_gap, pipe_color)
    last_pipe = pipe
    pipes = [pipe]
    dt = 0

    while not pop.all_dead():
        running = exit_codes(running)

        screen.fill("#264653")

        pop.update(pipes, dt)

        for bird in pop.population:
            if (not bird.dead):
                render.render(bird_color, bird.graphics)

        if (last_pipe.pos_x < screen.get_width() - pipe_gap_between - pipe_width):
            pipe = PipeObject(screen, pipe_speed, pipe_width, pipe_gap, pipe_color)
            pipes.append(pipe)
            last_pipe = pipe

        for pipe in pipes:
            pipe.update(dt)
            pipe.draw()

        if (pipes[:1][0].pos_x <= -pipe_width):
            pipes.pop(0)

        dt = clock.tick(60) / 1000
        pygame.display.update()
        clock.tick(60)

    print("Generation:", generation)
    print("Best Local:", pop.best_local.fitness)
    print("Best Global:", pop.best_global.fitness)
    print()

    generation += 1
    pop.reset()

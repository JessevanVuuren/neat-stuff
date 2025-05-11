from __future__ import annotations

from renderer import Render
from pipe import PipeObject
from game_types import *
from neat_ref import *
from globals import *
from bird_no_brain import Bird

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


genome_history = GenomeHistory(NEAT_INPUTS, NEAT_OUTPUT)
pop = Population(genome_history, NEAT_POP_SIZE)

render = Render()
render.set_background("./assets/background-day.png", True, True)


def eval(genomes: list[Genome]):
    birds: list[FlyBird] = []

    pipe = PipeObject("./assets/pipe-green.png")
    last_pipe = pipe
    pipes = [pipe]
    dt = 0

    for genome in genomes:
        bird = Bird(bird_sprites)
        birds.append(FlyBird(bird, genome))

    while len(birds) > 0 and birds[0].brain.fitness < 5000:

        quit_actions()

        render.fill()

        for i, bird in enumerate(birds):
            bird.body.update(pipes, dt, GAME_TYPE == GameType.DYNAMIC.value)
            bird.brain.fitness += 1
            inputs = bird.body.get_inputs(bird.body.closest_pipe(pipes))
            out = bird.brain.get_outputs(inputs)
            action = ActionState.FLY if out[0] > .5 else ActionState.STAY

            bird.body.move(action, dt)

            render.graphics_surface(bird.body.graphics)
            if bird.body.dead:
                birds.pop(i)

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


pop.run(eval)

from NEAT.genome_history import *
from NEAT.population_bird import *
from NEAT.genome import *

import random
import pygame
import time

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


class Pipe:
    def __init__(self, screen, speed, width, gap, color) -> None:
        self.screen = screen
        self.default_color = color
        self.color = color
        self.speed = speed
        self.width = width
        self.gap = gap

        self.pos_x = screen.get_width()
        self.height = random.randint(0, screen.get_height() - gap)

        self.top_rect = pygame.Rect(0, 0, 0, 0)
        self.bottom_rect = pygame.Rect(0, 0, 0, 0)

    def update(self, dt):
        self.pos_x -= self.speed * dt

        self.top_rect = pygame.Rect(self.pos_x, 0, self.width, self.height)
        self.bottom_rect = pygame.Rect(self.pos_x, self.height + self.gap, self.width, screen.get_height())

    def draw(self):
        pygame.draw.rect(screen, self.color, self.top_rect)
        pygame.draw.rect(screen, self.color, self.bottom_rect)


class Player:
    def __init__(self, gh) -> None:
        self.size = 25
        self.color = "#E76F51"
        self.speed = 600
        self.dead = False
        self.hit = False
        self.fitness = 0.0
        self.gh = gh

        self.body = pygame.Rect(
            screen.get_width() * .3 - self.size / 2,
            screen.get_height() / 2 - self.size / 2,
            self.size, self.size)

        self.brain = Genome(gh)
        for _ in range(10):
            self.brain.mutate()

    def draw(self):
        if not self.dead:
            pygame.draw.rect(screen, self.color, self.body)

    def update(self, pipes: list[Pipe], dt):
        pipe = self.closest_pipe(pipes)

        if (pipe.top_rect.colliderect(self.body) or pipe.bottom_rect.colliderect(self.body) or self.body.bottomleft[1] >= screen.get_height() or self.body.topleft[1] < 0):
            self.dead = True

        if self.dead:
            return

        self.fitness += 1

        inputs = self.get_inputs(pipe)
        action = self.think(inputs)
        self.move(action, dt)

    def think(self, inputs):
        out = self.brain.get_outputs(inputs)
        max_index = 0

        for i in range(len(out)):
            if out[i] > out[max_index]:
                max_index = i

        states = ["up", "stay", "down"]
        return states[max_index]

    def closest_pipe(self, pipes: list[Pipe]) -> Pipe:
        for pipe in pipes:
            if pipe.pos_x + pipe.width > self.body.topleft[0]:
                return pipe

        return pipes[0]

    def mate(self, partner):
        child = Player(self.gh)
        child.brain = self.brain.crossover(partner.brain)
        return child

    def get_inputs(self, pipe: Pipe):
        inputs = []
        inputs.append((screen.get_height() - self.body.centery) / screen.get_height())                  # distance ground
        inputs.append((pipe.pos_x + pipe.width - self.body.topleft[0]) / screen.get_width())            # distance first pipe
        inputs.append((self.body.bottomleft[1] - pipe.top_rect.bottomleft[1]) / screen.get_height())    # distance to top pipe
        inputs.append((pipe.bottom_rect.topleft[1] - self.body.topleft[1]) / screen.get_height())       # distance to bottom pipe
        return inputs

    def move(self, state, dt):
        if self.dead:
            return

        if state == "up":
            self.body.centery -= self.speed * dt
        if state == "down":
            self.body.centery += self.speed * dt
        if state == "stay":
            pass


def exit_codes(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    return running


genome_history = GenomeHistory(4, 3)
pop = Population(genome_history, 100, Player)


generation = 0


while True:

    pipe = Pipe(screen, pipe_speed, pipe_width, pipe_gap, pipe_color)
    last_pipe = pipe
    pipes = [pipe]
    dt = 0

    while not pop.all_dead():
        running = exit_codes(running)

        screen.fill("#264653")

        pop.update(pipes, dt)
        pop.draw()

        if (last_pipe.pos_x < screen.get_width() - pipe_gap_between - pipe_width):
            pipe = Pipe(screen, pipe_speed, pipe_width, pipe_gap, pipe_color)
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

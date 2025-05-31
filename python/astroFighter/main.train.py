from __future__ import annotations

from particles import ParticleSystem
from renderer import Render
from rocket import Rocket
from game_types import *
from neat_ref import *
from globals import *
from utils import *
from coin import *

import pygame
import math


MAX_DURATION = 10

def game_events():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_s):
                save_genome(pop.best_global, "best_genome")
                print("Global best genome: \"best_genome\" saved")

render = Render(SCREEN_WIDTH, SCREEN_HEIGHT, "Iosevka")

ps = ParticleSystem(render.screen)
cs = CoinSystem(render.screen)

genome_history = GenomeHistory(8, 3)
pop = Population(genome_history, 100)

rocket_image = img_scaler(pygame.image.load(absolute_path("./rocket.png")), .06)

DIAGONAL = math.sqrt(SCREEN_WIDTH * SCREEN_WIDTH + SCREEN_HEIGHT + SCREEN_HEIGHT)

@dataclass
class SpaceMan:
    player: Rocket
    brain: Genome


def get_inputs(rocket: Entity, next_coin: Coin) -> list[float]:

    direction_norm = next_coin.pos - rocket.pos
    direction_norm = direction_norm.normalize()

    return [
        rocket.pos.x / SCREEN_WIDTH,
        rocket.pos.y / SCREEN_HEIGHT,
        next_coin.pos.x / SCREEN_WIDTH,
        next_coin.pos.y / SCREEN_HEIGHT,
        math.sin(rocket.angle*0.0174532925),
        math.cos(rocket.angle*0.0174532925),
        direction_norm.x,
        direction_norm.y,
    ]


def eval(genomes: list[Genome]):
    spaceman: list[SpaceMan] = []

    for genome in genomes:
        player = Rocket(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, rocket_image, ps, True)
        spaceman.append(SpaceMan(player, genome))

    cs.set_agents([x.player for x in spaceman])

    delta_time = 0.1
    elapsed_time = 0
    while len(spaceman) > 0 and elapsed_time < MAX_DURATION:
        elapsed_time += delta_time
        game_events()

        for _, rocket in enumerate(spaceman):
            coin = cs.coins[rocket.player.id]
            distance_coin = 1 - rocket.player.pos.distance_to(coin.pos) / DIAGONAL
            rocket.brain.fitness = rocket.player.coins + distance_coin

            inputs = get_inputs(rocket.player, coin)
            outputs = rocket.brain.get_outputs(inputs)
            rocket.player.update_neat(delta_time, outputs)

            cs.update(rocket.player)

    for rocket in spaceman:
        rocket.brain.fitness -= rocket.player.idle_time * .1

pop.run(eval, report=True)

pygame.quit()

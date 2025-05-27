from __future__ import annotations

from particles import ParticleSystem, StarSystem
from renderer import Render
from rocket import Rocket
from game_types import *
from neat_ref import *
from globals import *
from utils import *
from coin import *

import pygame
import math


def game_events():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            return False

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_s):
                save_genome(pop.best_global, "best_genome")
                print("Global best genome: \"best_genome\" saved")

    return True


clock = pygame.time.Clock()

render = Render(SCREEN_WIDTH, SCREEN_HEIGHT, "Iosevka")

ps = ParticleSystem(render.screen)
cs = CoinSystem(render.screen)
st = StarSystem(render.alpha, 60, FMinMax(.7, 1), FMinMax(1, 3), FMinMax(.1, 2), ["#f2dfaa", "#ddb1f0", "#c3c2f2", "#f2b8c1", "#b5f2f7", "#ffffff", "#ffffff", "#ffffff", "#ffffff"])

genome_history = GenomeHistory(8, 3)
pop = Population(genome_history, 100)

rocket_image = img_scaler(pygame.image.load("./rocket.png"), .06)

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

    delta_time = 0
    elapsed_time = 0

    cs.set_agents([x.player for x in spaceman])

    while len(spaceman) > 0 and game_events() and elapsed_time < 1000:
        elapsed_time += 1

        render.fill("#000000")

        for _, rocket in enumerate(spaceman):
            coin = cs.coins[rocket.player.id]
            distance_coin = 1 - rocket.player.pos.distance_to(coin.pos) / 1468
            rocket.brain.fitness = rocket.player.coins + distance_coin

            inputs = get_inputs(rocket.player, coin)
            outputs = rocket.brain.get_outputs(inputs)
            rocket.player.update_neat(delta_time, outputs)

            cs.update(rocket.player)
            render.surface(rocket.player.graphic)

        ps.update(delta_time)
        st.update(delta_time)

        cs.draw()

        render.text("FPS: " + str(clock.get_fps()), 10, 10)
        render.text("Particles: " + str(len(ps.particles)), 10, 35)
        render.text("Generation: " + str(pop.generation), 10, 60)
        render.text("Reset: " + str(1000 - elapsed_time), 10, 85)

        play_time = clock.tick(FPS)
        delta_time = play_time / 1000
        render.display()

    for rocket in spaceman:
        rocket.brain.fitness -= rocket.player.idle_time * .1

    # woow = [f"{x.fitness:.4f}" for x in pop.population]
    # woow.sort(reverse=True)
    # print(woow)


pop.run(eval, report=True)

pygame.quit()

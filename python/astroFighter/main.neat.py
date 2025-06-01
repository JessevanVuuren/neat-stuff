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


render = Render(SCREEN_WIDTH, SCREEN_HEIGHT, "Iosevka")

ps = ParticleSystem()
cs = CoinSystem(render.screen)
st = StarSystem(60, FMinMax(.7, 1), FMinMax(1, 3), FMinMax(.1, 2), ["#f2dfaa", "#ddb1f0", "#c3c2f2", "#f2b8c1", "#b5f2f7", "#ffffff", "#ffffff", "#ffffff", "#ffffff"])

genome_history = GenomeHistory(8, 3)
pop = Population(genome_history, 100)

rocket_image = img_scaler(pygame.image.load(absolute_path("./rocket.png")), .06)
start_pos = Vec2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
size = tuple_2_vec2(rocket_image.get_size())

@dataclass
class SpaceMan:
    gameobject: GameObject
    brain: Genome
    idle_time = 0.0


def get_inputs(rocket: Entity, next_coin: Coin) -> list[float]:

    direction_norm = next_coin.pos - rocket.pos
    direction_norm = direction_norm.norm()

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


def game_events():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_s):
                save_genome(pop.best_global, "best_genome")
                print("Global best genome: \"best_genome\" saved")


def eval(genomes: list[Genome]):
    spaceman: list[SpaceMan] = []

    for genome in genomes:

        player = Rocket(start_pos, size, ps, True)
        graphics = Graphic(rocket_image, player, -90)

        gameObject = GameObject(player, graphics)
        spaceman.append(SpaceMan(gameObject, genome))

    cs.set_entitys([x.gameobject.player for x in spaceman])

    delta_time = 0
    elapsed_time = 0
    while len(spaceman) > 0 and elapsed_time < 1000:
        game_events()
        elapsed_time += 1

        render.fill("#000000")

        for agent in spaceman:

            player = agent.gameobject.player
            graph = agent.gameobject.graphics
            brain = agent.brain

            coin = cs.coins[player.id]
            distance_coin = 1 - player.pos.distance(coin.pos) / 1468
            brain.fitness = player.coins + distance_coin
            agent.idle_time += delta_time

            inputs = get_inputs(player, coin)
            outputs = brain.get_outputs(inputs)
            move_actions = [x > .5 for x in outputs]
            player.update(move_actions, delta_time)

            if move_actions[0]:
                agent.idle_time = 0

            cs.update(player)
            render.surface(graph)

        ps.update(delta_time)
        st.update(delta_time)

        render.particles(st.stars, True)
        render.particles(list(cs.coins.values()))

        render.text("FPS: " + str(clock.get_fps()), 10, 10)
        render.text("Particles: " + str(len(ps.particles)), 10, 35)
        render.text("Generation: " + str(pop.generation), 10, 60)
        render.text("Reset: " + str(1000 - elapsed_time), 10, 85)

        delta_time = clock.tick(FPS) / 1000
        render.display()

    for rocket in spaceman:
        rocket.brain.fitness -= rocket.idle_time * .1

clock = pygame.time.Clock()
pop.run(eval, report=True)
pygame.quit()

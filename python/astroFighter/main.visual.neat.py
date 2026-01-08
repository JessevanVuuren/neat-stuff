from __future__ import annotations

import math

import globals as gl
import pygame
from coin import Coin, CoinSystem
from game_types import Entity, FMinMax, GameObject, Genome, Graphic, SpaceMan, Vec2
from neaty import Config, GenomeHistory, NeatConfig, Population, save_genome
from particles import ParticleSystem, StarSystem
from renderer import Render
from rocket import Rocket
from utils import absolute_path, img_scaler, tuple_2_vec2

render = Render(gl.SCREEN_WIDTH, gl.SCREEN_HEIGHT, "Iosevka")

ps = ParticleSystem()
cs = CoinSystem()
st = StarSystem(60, FMinMax(0.5, 1), FMinMax(1, 3), FMinMax(0.1, 2), gl.STAR_COLORS)

config = Config("config", NeatConfig()).parse()
genome_history = GenomeHistory(config)
pop = Population(config, genome_history)

rocket_image = img_scaler(pygame.image.load(absolute_path("./rocket.png")), 0.06)
start_pos = Vec2(gl.SCREEN_WIDTH / 2, gl.SCREEN_HEIGHT / 2)
size = tuple_2_vec2(rocket_image.get_size())


def get_inputs(rocket: Entity, next_coin: Coin) -> list[float]:
    direction_norm = next_coin.pos - rocket.pos
    direction_norm = direction_norm.norm()

    return [
        rocket.pos.x / gl.SCREEN_WIDTH,
        rocket.pos.y / gl.SCREEN_HEIGHT,
        next_coin.pos.x / gl.SCREEN_WIDTH,
        next_coin.pos.y / gl.SCREEN_HEIGHT,
        math.sin(rocket.angle * 0.0174532925),
        math.cos(rocket.angle * 0.0174532925),
        direction_norm.x,
        direction_norm.y,
    ]


def game_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_genome(pop.best_global, "best_genome")
                print('Global best genome: "best_genome" saved')


def eval(genomes: list[Genome]):
    spaceman: list[SpaceMan] = []

    for genome in genomes:
        player = Rocket(start_pos.copy(), size.copy(), ps, True)
        graphics = Graphic(rocket_image, player, -90)

        gameObject = GameObject(player, graphics)
        spaceman.append(SpaceMan(gameObject, genome))

    cs.set_entitys([x.gameobject.player for x in spaceman])

    delta_time = 0
    elapsed_time = 0
    while elapsed_time < gl.MAX_DURATION:
        elapsed_time += delta_time
        game_events()

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
            move_actions = [x > 0.5 for x in outputs]
            player.update(move_actions, delta_time)

            if move_actions[0]:
                agent.idle_time = 0

            cs.update(player)
            render.surface(graph)

        ps.update(delta_time)
        st.update(delta_time)

        render.particles(st.stars, True)
        render.particles(list(cs.coins.values()))

        render.text(f"FPS: {str(clock.get_fps())}", 10, 10)
        render.text(f"Particles: {len(ps.particles)}", 10, 35)
        render.text(f"Generation: {pop.generation}", 10, 60)
        render.text(f"Reset: {gl.MAX_DURATION - elapsed_time:.04f}", 10, 85)

        delta_time = clock.tick(gl.FPS) / 1000
        render.display()

    for rocket in spaceman:
        rocket.brain.fitness -= rocket.idle_time * 0.1

    return [x.fitness for x in genomes]


clock = pygame.time.Clock()
pop.run(eval)
pygame.quit()

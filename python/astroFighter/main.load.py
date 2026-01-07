from __future__ import annotations

from particles import ParticleSystem, StarSystem
from renderer import Render
from rocket import Rocket
import globals as gl
from utils import absolute_path, img_scaler, tuple_2_vec2
from game_types import FMinMax, Vec2, Graphic, GameObject, Entity, SpaceMan
from coin import CoinSystem, Coin
from neaty import load_genome
import math


import pygame


def exit_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    return True


clock = pygame.time.Clock()

running = True
delta_time = 0

render = Render(gl.SCREEN_WIDTH, gl.SCREEN_HEIGHT, "Iosevka")

ps = ParticleSystem()
cs = CoinSystem()
st = StarSystem(60, FMinMax(0.7, 1), FMinMax(1, 3), FMinMax(0.1, 2), gl.STAR_COLORS)

rocket_image = img_scaler(pygame.image.load(absolute_path("./rocket.png")), 0.06)
# spaceship_image = img_scaler(pygame.image.load(absolute_path("./spaceship.png")), .06)

position = Vec2(gl.SCREEN_WIDTH / 2, gl.SCREEN_HEIGHT / 2)
size = tuple_2_vec2(rocket_image.get_size())

player = Rocket(position, size, ps, False)
graphics = Graphic(rocket_image, player)
graphics.angle_offset = -90

gameObject = GameObject(player, graphics)

cs.set_entitys([gameObject.player])


def get_inputs(rocket: Entity, next_coin: Coin) -> list[float]:
    direction_norm = next_coin.pos - rocket.pos
    direction_norm = direction_norm.norm()

    return [rocket.pos.x / gl.SCREEN_WIDTH, rocket.pos.y / gl.SCREEN_HEIGHT, next_coin.pos.x / gl.SCREEN_WIDTH, next_coin.pos.y / gl.SCREEN_HEIGHT, math.sin(rocket.angle * 0.0174532925), math.cos(rocket.angle * 0.0174532925), direction_norm.x, direction_norm.y]


genome = load_genome("genomes/genome_gen_fit_12-7093")
spaceman = SpaceMan(gameObject, genome)

while exit_events():
    render.fill("#000000")

    player, graph, brain = spaceman.extract()

    inputs = get_inputs(player, cs.coins[player.id])
    outputs = spaceman.brain.get_outputs(inputs)
    move_actions = [x > 0.5 for x in outputs]
    player.update(move_actions, delta_time)

    cs.update(player)
    ps.update(delta_time)
    st.update(delta_time)

    render.surface(graph)
    render.particles(ps.particles)
    render.particles(st.stars, True)
    render.particles(list(cs.coins.values()))

    render.text(f"Score: {player.coins}", 10, 30)
    render.text(f"FPS: {clock.get_fps()}", 10, 10)

    run_time = clock.tick(gl.FPS)
    delta_time = run_time / 1000
    render.display()

pygame.quit()

from __future__ import annotations

from particles import ParticleSystem, StarSystem
from renderer import Render
from rocket import Rocket
from game_types import *
from globals import *
from utils import *
from coin import *

import pygame


def exit_events():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()

    return True


clock = pygame.time.Clock()

running = True
delta_time = 0

render = Render(SCREEN_WIDTH, SCREEN_HEIGHT, "Iosevka")

ps = ParticleSystem()
cs = CoinSystem()
st = StarSystem(60, FMinMax(.7, 1), FMinMax(1, 3), FMinMax(.1, 2), STAR_COLORS)

rocket_image = img_scaler(pygame.image.load(absolute_path("./rocket.png")), .06)
# spaceship_image = img_scaler(pygame.image.load(absolute_path("./spaceship.png")), .06)

position = Vec2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
size = tuple_2_vec2(rocket_image.get_size())

player = Rocket(position, size, ps, False)
graphics = Graphic(rocket_image, player)
graphics.angle_offset = -90

gameObject = GameObject(player, graphics)

cs.set_entitys([gameObject.player])


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
        direction_norm.y
    ]


genome = load_genome("genomes/genome_gen_fit_9-7497")
spaceman = SpaceMan(gameObject, genome)

while exit_events():
    render.fill("#000000")

    player, graph, brain = spaceman.extract()

    inputs = get_inputs(player, cs.coins[player.id])
    outputs = spaceman.brain.get_outputs(inputs)
    move_actions = [x > .5 for x in outputs]
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

    run_time = clock.tick(FPS)
    delta_time = run_time / 1000
    render.display()

pygame.quit()

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
            return False

    return True


clock = pygame.time.Clock()

running = True
delta_time = 0

render = Render(SCREEN_WIDTH, SCREEN_HEIGHT, "Iosevka")

ps = ParticleSystem(render.screen)
cs = CoinSystem(render.screen)
st = StarSystem(render.alpha, 60, FMinMax(.7, 1), FMinMax(1, 3), FMinMax(.1, 2), ["#f2dfaa", "#ddb1f0", "#c3c2f2", "#f2b8c1", "#b5f2f7", "#ffffff", "#ffffff", "#ffffff", "#ffffff"])

rocket_image = img_scaler(pygame.image.load("./rocket.png"), .06)
spaceship_image = img_scaler(pygame.image.load("./spaceship.png"), .06)
player = Rocket(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, rocket_image, ps)

cs.set_agents([player])


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
        direction_norm.y
    ]


genome = load_genome("best_genome_score_10")
spaceman = SpaceMan(player, genome)

while exit_events():

    render.fill("#000000")

    coin = cs.coins[spaceman.player.id]
    inputs = get_inputs(spaceman.player, coin)
    outputs = spaceman.brain.get_outputs(inputs)
    spaceman.player.update_neat(delta_time, outputs)

    cs.update(spaceman.player)
    ps.update(delta_time)
    st.update(delta_time)

    render.surface(spaceman.player.graphic)
    cs.draw()

    render.text("Score: " + str(spaceman.player.coins), 10, 30)
    render.text("FPS: " + str(clock.get_fps()), 10, 10)

    run_time = clock.tick(FPS)
    delta_time = run_time / 1000
    render.display()


pygame.quit()

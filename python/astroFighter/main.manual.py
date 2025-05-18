from __future__ import annotations

from particles import ParticleSystem, StarSystem
from spaceship import Spaceship
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
st = StarSystem(render.alpha, 60, FMinMax(.5, 1), FMinMax(1, 3), FMinMax(.1, 2), ["#f2dfaa", "#ddb1f0", "#c3c2f2", "#f2b8c1", "#b5f2f7", "#ffffff", "#ffffff", "#ffffff", "#ffffff"])

rocket_image = img_scaler(pygame.image.load("./rocket.png"), .06)
spaceship_image = img_scaler(pygame.image.load("./spaceship.png"), .06)
# player = Rocket(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, rocket_image, ps)
player = Spaceship(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, spaceship_image, ps)

cs.set_agents([player])

score = 0.0
while exit_events():

    render.fill("#000000")

    player.update(delta_time)

    ps.update(delta_time)
    cs.update(player)
    st.update(delta_time)

    render.surface(player.graphic)
    cs.draw()

    print(1 - player.pos.distance_to(cs.coins[player.id].pos) / 1468)
    score = player.coins + 1 - player.pos.distance_to(cs.coins[player.id].pos) / 1468

    render.text("Score: " + str(score), 10, 30)
    render.text("FPS: " + str(clock.get_fps()), 10, 10)

    run_time = clock.tick(FPS)
    delta_time = run_time / 1000
    render.display()


pygame.quit()

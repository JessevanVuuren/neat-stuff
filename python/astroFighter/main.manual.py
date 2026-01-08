from __future__ import annotations

import globals as gl
import pygame
from coin import CoinSystem
from game_types import FMinMax, GameObject, Graphic, Vec2
from particles import ParticleSystem, StarSystem
from renderer import Render
from rocket import Rocket
from utils import absolute_path, img_scaler, tuple_2_vec2


def exit_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True


def get_inputs() -> list[bool]:
    keys = pygame.key.get_pressed()
    return [keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_d]]


clock = pygame.time.Clock()

delta_time = 0.0

render = Render(gl.SCREEN_WIDTH, gl.SCREEN_HEIGHT, "Iosevka")

ps = ParticleSystem()
cs = CoinSystem()
st = StarSystem(60, FMinMax(0.5, 1), FMinMax(1, 3), FMinMax(0.1, 2), gl.STAR_COLORS)


rocket_image = img_scaler(pygame.image.load(absolute_path("./rocket.png")), 0.06)
position = Vec2(gl.SCREEN_WIDTH / 2, gl.SCREEN_HEIGHT / 2)
size = tuple_2_vec2(rocket_image.get_size())

player = Rocket(position, size, ps, False)
graphics = Graphic(rocket_image, player)
graphics.angle_offset = -90

gameObject = GameObject(player, graphics)


cs.set_entitys([gameObject.player])

while exit_events():
    render.fill("#000000")

    player.update(get_inputs(), delta_time)

    ps.update(delta_time)
    cs.update(player)
    st.update(delta_time)

    render.surface(gameObject.graphics)
    render.particles(ps.particles)
    render.particles(st.stars, True)
    render.particles(list(cs.coins.values()))

    score = player.coins + 1 - player.pos.distance(cs.coins[player.id].pos) / 1468

    render.text("Score: " + str(score), 10, 30)
    render.text("FPS: " + str(clock.get_fps()), 10, 10)
    run_time = clock.tick(gl.FPS)
    delta_time = run_time / 1000
    render.display()


pygame.quit()

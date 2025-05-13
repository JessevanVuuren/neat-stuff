from __future__ import annotations

from particles import ParticleSystem
from renderer import Render
from rocked import Rocked
from globals import *
from utils import *


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

rocked_image = img_scaler(pygame.image.load("./spaceship.png"), .2)
player = Rocked(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, rocked_image, ps)

while exit_events():

    render.fill("#000000")

    player.update(delta_time)
    render.surface(player.graphic)

    ps.update(delta_time)
    ps.draw(render.screen)

    # cs.update(player)

    render.text("Score: " + str(player.coins), 10, 10)

    play_time = clock.tick(FPS)
    delta_time = play_time / 1000
    render.display()


pygame.quit()

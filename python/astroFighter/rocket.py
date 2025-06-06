from __future__ import annotations

from game_types import *
from particles import *
from globals import *
from utils import *
from coin import *

import math


class Rocket(Entity):

    def __init__(self, pos: Vec2, size: Vec2, ps: ParticleSystem, training_mode: bool = True):
        Entity.__init__(self, pos, size.x, size.y, 0)
        self.training_mode = training_mode
        self.ps = ps

        self.velocity = 0
        self.coins = 0

        self.smoke_trail = 10

        self.left_thrust_pos = Vec2(-25, -31.4)
        self.right_thrust_pos = Vec2(-25, 31.4)
        self.middle_thrust_pos = Vec2(-25, 0)

        if (not training_mode):
            self.smokeRange = gradient_color("white", "#181818", 60)
            self.exhaustRange = gradient_color("red", "yellow", 60)

    def update(self, inputs: list[bool], delta_time: float):
        self.move(inputs[0], inputs[1], inputs[2], delta_time)
        self.wrap()

    def move(self, forward: bool, right: bool, left: bool, delta_time: float):

        if forward:
            self.forward(delta_time)
        elif self.velocity > 0:
            self.brake(delta_time)
        else:
            self.velocity = 0

        if right:
            self.turn_right(delta_time)
        if left:
            self.turn_left(delta_time)

        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity * delta_time
        horizontal = math.sin(radians) * self.velocity * delta_time

        self.pos.x += vertical
        self.pos.y += horizontal

    def brake(self, delta_time: float):
        self.velocity *= math.pow((1 - BRAKE_FORCE), delta_time)

    def forward(self, delta_time: float):
        self.thrust_effect(self.middle_thrust_pos)
        self.velocity = min(self.velocity + ACCELERATION * delta_time, MAX_VELOCITY)

    def turn_left(self, delta_time: float):
        self.thrust_effect(self.left_thrust_pos)
        self.angle += ROTATION_VELOCITY * delta_time

    def turn_right(self, delta_time: float):
        self.thrust_effect(self.right_thrust_pos)
        self.angle -= ROTATION_VELOCITY * delta_time

    def thrust_effect(self, pos: Vec2):
        if self.training_mode:
            return

        exhaust = ParticleExhaust(self, pos.x, pos.y, 3, .1, self.exhaustRange, 4, 30)
        smoke = ParticleSmoke(self, pos.x - 39, pos.y * 1.2, 4, 1, self.smokeRange, 15)

        self.ps.add_particle(exhaust)
        self.ps.add_particle(smoke)

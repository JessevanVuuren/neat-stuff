from __future__ import annotations

from particles import ParticleSystem
from rocket import Rocket
from game_types import *
from neat_ref import *
from globals import *
from utils import *
from coin import *

import math

ps = ParticleSystem()
cs = CoinSystem()

genome_history = GenomeHistory(8, 3)
pop = Population(genome_history, 100)

start_pos = Vec2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
size = Vec2(x=68, y=46)


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


@dataclass
class TrainMan:
    player: Entity
    brain: Genome
    idle_time = 0.0

def eval(genomes: list[Genome]):
    print("eval_start")
    spaceman: list[TrainMan] = []

    for genome in genomes:

        player = Rocket(start_pos.copy(), size.copy(), ps, True)
        spaceman.append(TrainMan(player, genome))

    cs.set_entitys([x.player for x in spaceman])

    delta_time = 0.1
    elapsed_time = 0
    while elapsed_time < MAX_DURATION:
        elapsed_time += delta_time

        for agent in spaceman:

            player = agent.player
            brain = agent.brain

            coin = cs.coins[player.id]
            distance_coin = 1 - player.pos.distance(coin.pos) / 1468
            brain.fitness = player.coins + distance_coin
            agent.idle_time += 0.008

            inputs = get_inputs(player, coin)
            outputs = brain.get_outputs(inputs)
            move_actions = [x > .5 for x in outputs]
            player.update(move_actions, delta_time)

            if move_actions[0]:
                agent.idle_time = 0

            cs.update(player)

    
    for rocket in spaceman:
        rocket.brain.fitness -= rocket.idle_time * .1

    

# pop.run(eval, report=True)
pop.run(eval, report=True, fitness=9, save_on_done=True)

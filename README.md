# Neaty stuff

This repo is a collection of different use-cases and implementations with the [AI algorithm NEAT](https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf). The neat implementation (called neaty) used in this project is self written, which does not mean its better, its different and home made... With love. Nevertheless, this adaptation performs quite well and is able to adjust accordingly. This project is solely meant as a learning experience, not meant to be used elsewhere.

## use-cases

This project includes 3 projects that uses neaty

- xor
- flappy bird
- astroFighter

Each projects is complexer than the one before, where flappy bird is almost solved instantly, xor takes a few generations and astroFighter takes quite some time.

## xor

### start 

```bash
python main.py
```

### output
```
Gen: 46 Fitness: 3.9999999999276397
0 - 0 => [2.8326434818844086e-06], expected: 0, fit: 8.023869095462225e-12
0 - 1 => [0.9999940195780661], expected: 1, fit: 3.5765446507391526e-11
1 - 1 => [0.999995218621369], expected: 1, fit: 2.286158161321944e-11
1 - 0 => [2.3894391988975594e-06], expected: 0, fit: 5.70941968522821e-12
```

## Flappy bird

The flappy bird game exists in two flavours, a manual and automatic. manual mode is the easiest, you only have to press up or down to control the bird. If you don't press eny buttons the bird will way in place. Automatic is a bit harder and, where the controls mimic the original Flappy bird. Both are easily solved by neaty.

config can be found in `./python/bird/globals.py`
```python
GAME_TYPE = "dynamic" # "static" = up down, "dynamic" = gravity
GAME_PLAYER = "neat" # "manual" = human, "neat" = ai
```

### start 
```bash
python main.py
```
### output
![img1](https://github.com/JessevanVuuren/neat-stuff/blob/master/imgs/img1.png?raw=true)

# AstroFighter

AstroFighter is a game where you need to collect coins as fast as possible, sadly no fighting yet.

### start manual mode, you're controlling the rocket
```bash
python main.manual.py
```

### start training mode, fast and headless
```bash
python main.train.py
```

### start training mode, visually
```bash
python load.visual.neat.py
```

### start the game with a trained agent
agents can be fount in `./python/astroFighter/genomes`
```bash
python main.load.py
```

### output where you can see neat train visually
![img2](https://github.com/JessevanVuuren/neat-stuff/blob/master/imgs/img2.png?raw=true)

### output where a trained agent plays the game
![img3](https://github.com/JessevanVuuren/neat-stuff/blob/master/imgs/img3.png?raw=true)

### output of headless training mode
```
=== [Generation: 10] ===
Reset time: 0.0056ms
Sim time: 0.1589ms
Local Fitness: 3.831211
Global Fitness: 4.538333
Genes history: 35
Nodes: 11, Genes: 6
Layers: 2


=== [Generation: 11] ===
Reset time: 0.0073ms
Sim time: 0.1580ms
Local Fitness: 3.837156
Global Fitness: 4.538333
Genes history: 35
Nodes: 11, Genes: 6
Layers: 2
```
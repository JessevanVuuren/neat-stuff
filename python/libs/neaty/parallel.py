from multiprocessing import Pool, cpu_count
from collections.abc import Callable
from contextlib import closing
from .genome import Genome
import math


class MultiEvaluator:
    def __init__(self, fitness_function: Callable[[list[Genome]], list[float]], workers: int | None = None) -> None:
        self.workers = workers if workers else cpu_count()
        self.fitness_function = fitness_function

    def _split_list(self, l: list[Genome], chunks: int) -> list[list[Genome]]:
        size = math.ceil(len(l) / chunks)
        return [l[i:i+size] for i in range(0, len(l), size)]

    def eval(self, genomes: list[Genome]) -> list[float]:
        batch_of_genomes = self._split_list(genomes, self.workers)
        results: list[list[float]] = []

        with closing(Pool(processes=self.workers)) as pool:
            results = pool.map(self.fitness_function, batch_of_genomes)

        for genomes, fitnesses in zip(batch_of_genomes, results):
            for genome, fitness in zip(genomes, fitnesses):
                genome.fitness = fitness

        return [0.0]
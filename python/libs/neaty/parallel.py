from collections.abc import Callable
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import AsyncResult
from .genome import Genome
from typing import TypeVar

T = TypeVar("T")


class MultiEvaluator:
    def __init__(self, fitness_function: Callable[[list[Genome]], None], workers: int | None,) -> None:
        self.workers = workers if workers else cpu_count()
        self.fitness_function = fitness_function
        self.pool = Pool(self.workers)

    def __del__(self):
        print("cleaning object")
        self.pool.close()
        self.pool.join()
        self.pool.terminate()

    def eval(self, genomes: list[Genome]):
        evaluations: list[AsyncResult[None]] = []

        for genome in genomes:
            evaluations.append(self.pool.apply_async(self.fitness_function, [genome]))
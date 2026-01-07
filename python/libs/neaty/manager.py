from .genome import Genome
import pickle
import os.path
from pathlib import Path


def save_genome(genome: Genome, dir: str) -> None:
    Path(dir).parent.mkdir(exist_ok=True, parents=True)

    with open(dir, "wb") as file:
        pickle.dump(genome, file)


def load_genome(name: str) -> Genome:
    if not os.path.isfile(name):
        raise FileExistsError(f"File: {name}, does not exist")

    with open(name, "rb") as file:
        genome = pickle.load(file)
        return genome

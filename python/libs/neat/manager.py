from .genome import Genome
import pickle
import os.path


def save_genome(genome:Genome, name:str):
    with open(name, "wb") as file:
        pickle.dump(genome, file)

def load_genome(name:str) -> Genome:
    if (not os.path.isfile(name)):
        raise RuntimeError(f"File: {name}, does not exist")
    
    with open(name, "rb") as file:
        genome = pickle.load(file)
        return genome

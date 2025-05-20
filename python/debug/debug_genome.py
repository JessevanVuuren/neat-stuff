from neat_ref import *


class DebugGenome:
    def __init__(self) -> None:
        pass

    def print_genome(self, genome: Genome):
        print()
        print(f"Nodes: len nodes: {len(genome.nodes)}")
        print(f"Genes: len genes: {len(genome.genes)}")
        print(f"inputs nodes: {genome.inputs}")
        print(f"outputs nodes: {genome.outputs}")
        
        print()

    def history_info(self, gh: GenomeHistory):
        print(f"GenomeHistory len genes: {len(gh.all_genes)}")
        print(f"GenomeHistory highest_hidden: {gh.highest_hidden}")


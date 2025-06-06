from __future__ import annotations
from .config import NeatConfig
from .genome_history import *
from itertools import count
from .gene import *
from .node import *
import random


class Genome:
    def __init__(self, config: NeatConfig, gh: GenomeHistory) -> None:
        self.genome_history = gh
        self.config = config

        self.inputs = gh.inputs
        self.outputs = gh.outputs

        self.node_indexer = None

        self.nodes: dict[int, Node] = {}
        self.genes: dict[int, Gene] = {}

        self.sorted_nodes: list[Node] = []

        self.fitness = 0.0
        self.adjusted_fitness = 0.0

        node_key = 0
        for _ in range(self.inputs):
            self.nodes[node_key] = Node(self.config, node_key, 0)
            node_key += 1

        for _ in range(self.outputs):
            self.nodes[node_key] = Node(self.config, node_key, 1)
            node_key += 1

    def clone(self):
        clone = Genome(self.config, self.genome_history)

        clone.adjusted_fitness = self.adjusted_fitness
        clone.fitness = self.fitness

        clone.nodes.clear()
        clone.genes.clear()

        for node in self.nodes.values():
            clone.nodes[node.number] = node.clone()

        for gene in self.genes.values():
            clone.genes[gene.innovation] = gene.clone()

        clone.connect_genes()
        clone.cache_sorted_nodes()
        return clone

    def connect_nodes(self, n1: Node, n2: Node):
        n1_layer = n1.layer if n1.layer != 1 else 1000000
        n2_layer = n2.layer if n2.layer != 1 else 1000000

        if n1_layer > n2_layer:
            n1, n2 = n2, n1

        c = self.genome_history.exists(n1, n2)
        new_gene = Gene(self.config, n1, n2)

        if c:
            new_gene.innovation = c.innovation
            if not self.exists(new_gene.innovation):
                self.genes[new_gene.innovation] = new_gene
                return new_gene
        else:
            new_gene.innovation = self.genome_history.global_innovation
            self.genome_history.global_innovation += 1
            self.genome_history.add_gene(new_gene)
            self.genes[new_gene.innovation] = new_gene
            return new_gene

    def cache_sorted_nodes(self):
        self.sorted_nodes = [n for n in list(self.nodes.values())[self.inputs + self.outputs:]]
        self.sorted_nodes.sort(key=lambda x: x.layer)

    def mutate(self):
        if len(self.genes) == 0:
            self.add_gene()

        if random.random() < self.config.prob_create_gene:
            self.add_gene()
        if random.random() < self.config.prob_create_node:
            self.add_node()
        if random.random() < self.config.prob_remove_gene:
            self.remove_gene()
        if random.random() < self.config.prob_remove_node:
            self.remove_node()

        for gene in self.genes.values():
            gene.mutate()

        for node in self.nodes.values():
            node.mutate()

        self.connect_genes()
        self.cache_sorted_nodes()

    def add_gene(self):
        values = list(self.nodes.values())

        n1 = random.choice(values)
        n2 = random.choice(values)

        while n1.layer == n2.layer or (n2.layer == 0):
            n1 = random.choice(values)
            n2 = random.choice(values)

        self.connect_nodes(n1, n2)

    def add_node(self):
        if len(self.genes) == 0:
            self.add_gene()

        enabled_genes = [g for g in self.genes.values() if g.enabled]

        if not enabled_genes:
            return

        gene = random.choice(enabled_genes)
        get_node_id = self.get_new_node_key()
        node = Node(self.config, get_node_id, (gene.in_node.layer + gene.out_node.layer) / 2)

        gene1 = self.connect_nodes(gene.in_node, node)
        gene2 = self.connect_nodes(node, gene.out_node)

        if gene1:
            gene1.weight = gene.weight
        if gene2:
            gene2.weight = 1.0

        gene.enabled = False
        self.nodes[get_node_id] = node

    def remove_node(self):
        if (self.inputs + self.outputs >= len(self.nodes)):
            return

        nodes = [n for n in list(self.nodes.values())[self.inputs + self.outputs:]]
        node_to_delete = random.choice(nodes)

        genes_to_delete: list[Gene] = []
        for gene in self.genes.values():
            if (gene.in_node.number == node_to_delete.number or gene.out_node.number == node_to_delete.number):
                genes_to_delete.append(gene)

        for gene in genes_to_delete:
            self.genes.pop(gene.innovation)

        self.nodes.pop(node_to_delete.number)

    def remove_gene(self):
        if (len(self.genes) == 0):
            return

        if self.genes:
            delete_gene = random.choice(list(self.genes))
            self.genes.pop(delete_gene)

    def get_node(self, n: int) -> Node:
        node = self.nodes.get(n)

        if (not node):
            raise Exception(f"Node not found, number: {n}")

        return node

    def get_gene(self, innovation: int) -> Gene:
        gene = self.genes.get(innovation)

        if (not gene):
            raise Exception(f"Gene not found, innovation: {innovation}")

        return gene.clone()

    def exists(self, innovation: int):
        return innovation in self.genes

    def get_new_node_key(self):
        if self.node_indexer is None:
            self.node_indexer = count(max(self.nodes.keys(), default=-1) + 1)

        key = next(self.node_indexer)

        assert key not in self.nodes

        return key

    def connect_genes(self):

        for gene in self.genes.values():
            gene.in_node = self.get_node(gene.in_node.number)
            gene.out_node = self.get_node(gene.out_node.number)

        for node in self.nodes.values():
            node.genes.clear()

        for gene in self.genes.values():
            gene.out_node.genes.append(gene)

    def get_outputs(self, inputs: list[float]) -> list[float]:
        if len(inputs) != self.inputs:
            raise RuntimeError("Wrong number of inputs")

        for node in self.nodes.values():
            node.output = 0
            node.calculated = False

        for i in range(self.inputs):
            self.nodes[i].output = inputs[i]

        for node in self.sorted_nodes:
            node.calculate()

        final_outputs: list[float] = []
        for i in range(self.inputs, self.inputs + self.outputs):
            self.nodes[i].calculate()
            final_outputs.append(self.nodes[i].output)

        return final_outputs

    def get_weight(self, innovation: int) -> float:
        gene = self.genes.get(innovation)
        return gene.weight if gene else -1.0

    def get_highest_innovation(self, genes: dict[int, Gene]) -> int:
        if len(genes) == 0:
            return 0

        return max(x.innovation for x in genes.values())

    def crossover(self, partner: Genome) -> Genome:
        child = Genome(self.config, self.genome_history)
        child.genes.clear()
        child.nodes.clear()

        for node in (self.nodes | partner.nodes).values():
            child.nodes[node.number] = node.clone()

        valid_node_ids = {n.number for n in child.nodes.values()}
        all_innovations = set(self.genes) | set(partner.genes)

        for i in all_innovations:
            gene1 = i in self.genes
            gene2 = i in partner.genes

            if gene1 and gene2:
                gene = self.genes[i] if random.random() < .5 else partner.genes[i]
            elif gene1:
                gene = self.genes[i]
            else:
                gene = partner.genes[i]

            if gene.in_node.number in valid_node_ids and gene.out_node.number in valid_node_ids:
                child.genes[gene.innovation] = gene.clone()

        return child

    def calculate_compatibility(self, partner: Genome):
        innovations1 = set(self.genes.keys())
        innovations2 = set(partner.genes.keys())

        all_innovations = innovations1 | innovations2

        matching = 0
        disjoint = 0
        excess = 0

        weight_diff_sum = 0.0

        max1 = max(innovations1) if innovations1 else 0
        max2 = max(innovations2) if innovations2 else 0
        max_shared = max(max1, max2)

        for i in all_innovations:
            in_self = i in self.genes
            in_partner = i in partner.genes

            if in_self and in_partner:
                weight_diff_sum += abs(self.genes[i].weight - partner.genes[i].weight)
                matching += 1

            else:
                if i <= max_shared:
                    disjoint += 1
                else:
                    excess += 1

        normalize = max(len(self.genes), len(partner.genes))
        if normalize < 20:
            normalize = 1

        c1 = 1.0
        c2 = 1.0
        c3 = 0.4

        avg_weight_diff = weight_diff_sum / matching if matching > 0 else 0.0
        delta = (c1 * excess + c2 * disjoint) / normalize + c3 * avg_weight_diff
        return delta

    def info(self):
        print(f"Nodes: {len(self.nodes)}, Genes: {len(self.genes)}")
        layers = {x.layer for x in self.nodes.values()}
        print(f"Layers: {len(layers)}")

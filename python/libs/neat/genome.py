from __future__ import annotations
from webbrowser import get
from .genome_history import *
from itertools import count
from .gene import *
from .node import *
import random



class Genome:
    def __init__(self, gh: GenomeHistory) -> None:
        self.genome_history = gh

        self.inputs = gh.inputs
        self.outputs = gh.outputs

        self.input_layer = 0
        self.output_layer = 10

        self.total_nodes = 0
        self.node_indexer = None

        self.nodes: list[Node] = []
        self.genes: list[Gene] = []

        self.fitness = 0.0
        self.adjusted_fitness = 0.0

        for _ in range(self.inputs):
            self.nodes.append(Node(self.total_nodes, 0))
            self.total_nodes += 1

        for _ in range(self.outputs):
            self.nodes.append(Node(self.total_nodes, 1))
            self.total_nodes += 1

    def clone(self):
        clone = Genome(self.genome_history)

        clone.total_nodes = self.total_nodes
        clone.adjusted_fitness = self.adjusted_fitness
        clone.fitness = self.fitness

        clone.nodes.clear()
        clone.genes.clear()

        for i in range(len(self.nodes)):
            clone.nodes.append(self.nodes[i].clone())

        for i in range(len(self.genes)):
            clone.genes.append(self.genes[i].clone())

        clone.connect_genes()
        return clone

    def connect_nodes(self, n1: Node, n2: Node):
        n1_layer = n1.layer if n1.layer != 1 else 1000000
        n2_layer = n2.layer if n2.layer != 1 else 1000000

        if n1_layer > n2_layer:
            n1, n2 = n2, n1

        c = self.genome_history.exists(n1, n2)
        x = Gene(n1, n2)

        if c:
            x.innovation = c.innovation
            if not self.exists(x.innovation):
                self.genes.append(x)
        else:
            x.innovation = self.genome_history.global_innovation
            self.genome_history.global_innovation += 1
            self.genome_history.all_genes.append(x)
            self.genes.append(x)

    def mutate(self):
        if len(self.genes) == 0:
            self.add_gene()

        if random.random() < .5:  # add gene
            self.add_gene()
        if random.random() < 1:  # add node
            self.add_node()
        if random.random() < 0:  # remove gene
            self.remove_gene()
        if random.random() < 1:  # remove node
            self.remove_node()

        for i in range(len(self.genes)):
            self.genes[i].mutate()

    def add_gene(self):
        n1 = random.choice(self.nodes)
        n2 = random.choice(self.nodes)

        while n1.layer == n2.layer or (n2.layer == 0):
            n1 = random.choice(self.nodes)
            n2 = random.choice(self.nodes)

        self.connect_nodes(n1, n2)

    def add_node(self):
        if len(self.genes) == 0:
            self.add_gene()

        enabled_genes = [g for g in self.genes if g.enabled]
        print(enabled_genes)

        if not enabled_genes:
            print("no genes to split")
            return

        gene = random.choice(enabled_genes)
        get_node_id = self.get_new_node_key()
        node = Node(get_node_id, (gene.in_node.layer + gene.out_node.layer) / 2)

        self.total_nodes += 1
        self.connect_nodes(gene.in_node, node)
        self.connect_nodes(node, gene.out_node)

        self.genes[-1].weight = 1.0
        self.genes[-2].weight = gene.weight
        gene.enabled = False
        self.nodes.append(node)

    def remove_node(self):
        if (self.inputs + self.outputs >= len(self.nodes)):
            return

        nodes = self.nodes[self.inputs:-self.outputs]
        node_to_delete = random.choice(nodes)

        genes_to_delete: list[Gene] = []
        for gene in self.genes:
            if (gene.in_node.number == node_to_delete.number or gene.out_node.number == node_to_delete.number):
                genes_to_delete.append(gene)

        for gene in genes_to_delete:
            self.genes.remove(gene)

        self.nodes.remove(node_to_delete)
        self.total_nodes -= 1

        for i, node in enumerate(self.nodes):
            node.number = i

    def remove_gene(self):
        if (len(self.genes) == 0):
            return

        if self.genes:
            delete_index = random.randint(0, len(self.genes) - 1)
            self.genes.pop(delete_index)

    def get_node(self, n: int):
        for i in range(len(self.nodes)):
            if self.nodes[i].number == n:
                return self.nodes[i]

        raise Exception(f"Node not found, number: {n}")

    def get_gene(self, innovation: int) -> Gene:
        for g in self.genes:
            if g.innovation == innovation:
                return g.clone()

        raise Exception(f"Gene not found, innovation: {innovation}")

    def get_new_node_key(self):
        if self.node_indexer is None:
            self.node_indexer = count(len(self.nodes) + 1)

        new_id = next(self.node_indexer)

        return new_id

    def connect_genes(self):

        for i in range(len(self.genes)):
            self.genes[i].in_node = self.get_node(self.genes[i].in_node.number)
            self.genes[i].out_node = self.get_node(self.genes[i].out_node.number)

        for i in range(len(self.nodes)):
            self.nodes[i].genes.clear()

        for i in range(len(self.genes)):
            self.genes[i].out_node.genes.append(self.genes[i])

    def get_outputs(self, inputs: list[float]) -> list[float]:
        if len(inputs) != self.inputs:
            raise RuntimeError("Wrong number of inputs")

        for node in self.nodes:
            node.output = 0
            node.genes = []

        for i in range(self.inputs):
            self.nodes[i].output = inputs[i]

        self.connect_genes()

        for layer in range(2, self.genome_history.highest_hidden + 1):
            nodes_in_layer: list[Node] = []
            for n in range(len(self.nodes)):
                if self.nodes[n].layer == layer:
                    nodes_in_layer.append(self.nodes[n])

            for n in range(len(nodes_in_layer)):
                nodes_in_layer[n].calculate()

        final_outputs: list[float] = []
        for n in range(self.inputs, self.inputs + self.outputs):
            self.nodes[n].calculate()
            final_outputs.append(self.nodes[n].output)

        return final_outputs

    def exists(self, innovation: int):
        for c in self.genes:
            if c.innovation == innovation:
                return True
        return False

    def get_weight(self, innovation: int):
        for g in self.genes:
            if g.innovation == innovation:
                return g.weight
        return -1

    def crossover(self, partner: Genome) -> Genome:
        child = Genome(self.genome_history)
        child.nodes.clear()

        try:
            p1_highest_innovation = max([(x.innovation) for x in self.genes])
        except Exception:
            p1_highest_innovation = 0

        try:
            p2_highest_innovation = max([(x.innovation) for x in partner.genes])
        except Exception:
            p2_highest_innovation = 0

        if self.total_nodes > partner.total_nodes:
            child.total_nodes = self.total_nodes
            for node in self.nodes:
                child.nodes.append(node.clone())
        else:
            child.total_nodes = partner.total_nodes
            for node in partner.nodes:
                child.nodes.append(node.clone())

        highest_innovation = (
            p1_highest_innovation if self.fitness > partner.fitness else p2_highest_innovation
        )

        for i in range(highest_innovation + 1):
            e1 = self.exists(i)
            e2 = partner.exists(i)
            if e1 or e2:
                if e1 and e2:
                    gene = (
                        self.get_gene(i)
                        if (random.random()) < 0.5
                        else partner.get_gene(i)
                    )
                    child.genes.append(gene)
                    continue
                if e1:
                    child.genes.append(self.get_gene(i))
                if e2:
                    child.genes.append(partner.get_gene(i))

        child.connect_genes()
        return child

    def calculate_compatibility(self, partner: Genome):
        try:
            p1_highest_innovation = max([(x.innovation) for x in self.genes])
        except Exception:
            p1_highest_innovation = 0

        try:
            p2_highest_innovation = max([(x.innovation) for x in partner.genes])
        except Exception:
            p2_highest_innovation = 0

        if self.fitness > partner.fitness:
            highest_innovation = p1_highest_innovation
        else:
            highest_innovation = p2_highest_innovation

        matching = 0
        disjoint = 0
        excess = 0

        total_weights = 0
        average_weights = 0

        for i in range(highest_innovation + 1):
            e1 = self.exists(i)
            e2 = partner.exists(i)
            if e1 or e2:
                if e1 and e2:
                    matching += 1
                    total_weights += abs(self.get_weight(i)) + abs(partner.get_weight(i))
                    continue
                disjoint += 1

        average_weights = total_weights / (1 if matching == 0 else matching)

        for i in range(highest_innovation + 1, max(p1_highest_innovation, p2_highest_innovation) + 1):
            e1 = self.exists(i)
            e2 = partner.exists(i)
            if e1 or e2:
                excess += 1

        N = 1 if highest_innovation < 20 else highest_innovation

        c1 = 1.0
        c2 = 1.0
        c3 = 0.4

        E = c1 * excess / N
        D = c2 * disjoint / N
        W = c3 * average_weights

        delta = E + D + W

        return delta

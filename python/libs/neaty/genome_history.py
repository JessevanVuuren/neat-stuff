from __future__ import annotations

from typing import TYPE_CHECKING

from .config import NeatConfig

if TYPE_CHECKING:
    from .gene import Gene
    from .node import Node


class GenomeHistory:
    def __init__(self, config: NeatConfig) -> None:
        self.outputs = config.outputs
        self.inputs = config.inputs

        self.all_genes: dict[tuple[int, int], Gene] = {}
        self.global_innovation = 0

    def add_gene(self, gene: Gene) -> None:
        self.all_genes[gene.in_node.number, gene.out_node.number] = gene

    def exists(self, n1: Node, n2: Node) -> Gene | None:
        return self.all_genes.get((n1.number, n2.number))

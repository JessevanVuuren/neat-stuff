    def add_node(self):
        if len(self.genes) == 0:
            self.add_gene()

        if random.random() < 0.2:
            self.genome_history.highest_hidden += 1

        n = Node(self.total_nodes, random.randint(2, self.genome_history.highest_hidden))
        self.total_nodes += 1

        g = random.choice(self.genes)
        l1 = g.in_node.layer
        l2 = g.out_node.layer
        if l2 == 1:
            l2 = 1000000

        attempts = 0
        max_attempts = 100

        while (l1 > n.layer or l2 < n.layer) and attempts < max_attempts:
            g = random.choice(self.genes)
            l1 = g.in_node.layer
            l2 = g.out_node.layer
            if l2 == 1:
                l2 = 1000000
            attempts += 1

        if attempts == max_attempts:
            return  # could not find a valid gene, safely abort

        self.connect_nodes(g.in_node, n)
        self.connect_nodes(n, g.out_node)

        self.genes[-1].weight = 1.0
        self.genes[-2].weight = g.weight
        g.enabled = False
        self.nodes.append(n)




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
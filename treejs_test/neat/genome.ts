import { Gene } from "./gene.ts"
import { GenomeHistory } from "./genome_history.ts"
import { Node } from "./node.ts"
import { Profiler } from "./profiler.ts"

export class Genome {
  private inputs: number
  private outputs: number

  private total_nodes = 0

  private nodes: Node[] = []
  private genes: Gene[] = []
  public fitness = 0

  constructor(private genome_history: GenomeHistory) {
    this.inputs = genome_history.inputs
    this.outputs = genome_history.outputs

    for (let i = 0; i < this.inputs; i++) {
      this.nodes.push(new Node(this.total_nodes, 0))
      this.total_nodes++
    }

    for (let i = 0; i < this.outputs; i++) {
      this.nodes.push(new Node(this.total_nodes, 1))
      this.total_nodes++
    }
  }

  public debug_info() {
    console.log("[Genome] Size Nodes: ", this.nodes.length)
    console.log("[Genome] Size Genes: ", this.genes.length)
  }

  public clone() {
    const clone = new Genome(this.genome_history)
    clone.total_nodes = this.total_nodes
    clone.fitness = this.fitness

    clone.nodes = this.nodes.map(node => node.clone())
    clone.genes = this.genes.map(gene => gene.clone())

    clone.connect_genes()
    return clone
  }

  private connect_nodes(n1: Node, n2: Node) {
    const n1_layer = n1.layer !== 1 ? n1.layer : 1000000
    const n2_layer = n2.layer !== 1 ? n2.layer : 1000000

    if (n1_layer > n2_layer) {
      [n1, n2] = [n2, n1]
    }

    const c = this.genome_history.exists(n1, n2)
    const x = new Gene(n1, n2)

    if (c) {
      x.innovation = c.innovation
      if (!this.exists(x.innovation)) {
        this.genes.push(x)
      }
    }
    else {
      x.innovation = this.genome_history.global_innovation
      this.genome_history.global_innovation++
      this.genome_history.all_genes.push(x)
      this.genes.push(x)
    }
  }

  private add_gene() {
    let n1 = this.nodes[Math.floor(Math.random() * this.nodes.length)]
    let n2 = this.nodes[Math.floor(Math.random() * this.nodes.length)]

    while (n1.layer === n2.layer || n2.layer === 0) {
      n1 = this.nodes[Math.floor(Math.random() * this.nodes.length)]
      n2 = this.nodes[Math.floor(Math.random() * this.nodes.length)]
    }

    this.connect_nodes(n1, n2)
  }

  private add_node() {
    if (this.genes.length == 0) this.add_gene()
    if (Math.random() < .2) this.genome_history.highest_hidden++

    const layer = Math.floor(Math.random() * (this.genome_history.highest_hidden - 1)) + 2
    const node = new Node(this.total_nodes, layer)
    this.total_nodes++

    let gene = this.genes[Math.floor(Math.random() * this.genes.length)]
    let l1 = gene.in_node.layer
    let l2 = gene.out_node.layer

    if (l2 == 1) l2 = 1000000

    while (l1 > node.layer || l2 < node.layer) {
      gene = this.genes[Math.floor(Math.random() * this.genes.length)]
      l1 = gene.in_node.layer
      l2 = gene.out_node.layer
      if (l2 == 1) l2 = 1000000
    }

    this.connect_nodes(gene.in_node, node)
    this.connect_nodes(node, gene.out_node)

    const last_gene = this.genes.at(-1)
    if (last_gene) last_gene.weight = 1.0

    const second_to_last = this.genes.at(-2)
    if (second_to_last) second_to_last.weight = gene.weight

    gene.enabled = false
    this.nodes.push(node)
  }

  public mutate() {
    if (this.genes.length == 0) this.add_gene()
    if (Math.random() < .8) this.genes.forEach(gene => gene.mutate())
    if (Math.random() < .08) this.add_gene()
    if (Math.random() < .02) this.add_node()
  }

  private get_node(node_number: number): Node | undefined {
    return Profiler.time("get_node", () => {

      const node = this.nodes.find(node => node.number === node_number)
      
      if (!node) {
        throw new Error(`Node not found: Something's wrong — ${node_number}`)
      }
      
      return node
    })
  }

  private get_gene(innovation: number) {
    return Profiler.time("get_gene", () => {

      const gene = this.genes.find(gene => gene.innovation === innovation)
      
      if (!gene) {
        throw new Error(`Gene not found: Something's wrong — ${innovation}`)
      }
      
      return gene.clone()
    })
  }

  private connect_genes() {
    this.genes.forEach(gene => {
      const node_in = this.get_node(gene.in_node.number)
      const node_out = this.get_node(gene.out_node.number)

      if (!node_in || !node_out) {
        throw new Error("Gene connection failed due to missing node")
      }

      gene.in_node = node_in
      gene.out_node = node_out
    });

    this.nodes.forEach(node => node.genes = []);
    this.genes.forEach(gene => gene.out_node.genes.push(gene));
  }

  public get_outputs(nn_inputs: number[]) {
    if (nn_inputs.length !== this.inputs) {
      throw new Error("Wrong number of inputs")
    }


    this.nodes.forEach(node => {
      node.output = 0
      node.genes = []
    })

    for (let i = 0; i < this.inputs; i++) {
      this.nodes[i].output = nn_inputs[i]
    }


    this.connect_genes()

    for (let layer = 2; layer < this.genome_history.highest_hidden + 1; layer++) {
      const nodes_in_layers = this.nodes.filter(node => node.layer === layer)
      nodes_in_layers.forEach(node => node.calculate())
    }

    const final_outputs: number[] = []
    for (let i = this.inputs; i < this.inputs + this.outputs; i++) {
      this.nodes[i].calculate()
      final_outputs.push(this.nodes[i].output)
    }

    return final_outputs
  }

  private exists(innovation: number) {
    return Profiler.time("exists", () => this.genes.some(gene => gene.innovation == innovation))
  }

  private get_weight(innovation: number) {
    return Profiler.time("get_weight", () => {
      const gene = this.genes.find(gene => gene.innovation === innovation)
      return gene ? gene.weight : -1
    })
  }

  private get_highest_innovation(genes: Gene[]): number {
    return genes.length > 0
      ? Math.max(...genes.map(g => g.innovation))
      : 0
  }

  public crossover(partner: Genome) {
    const child = new Genome(this.genome_history)
    child.nodes = []

    const more_fit = this.fitness > partner.fitness ? this : partner;
    const less_fit = this.fitness > partner.fitness ? partner : this;

    if (this.total_nodes > partner.total_nodes) {
      child.total_nodes = this.total_nodes;
      for (let i = 0; i < this.total_nodes; i++) {
        child.nodes.push(this.nodes[i].clone());
      }
    } else {
      child.total_nodes = partner.total_nodes;
      for (let i = 0; i < partner.total_nodes; i++) {
        child.nodes.push(partner.nodes[i].clone());
      }
    }

    const p1_highest_innovation = this.get_highest_innovation(this.genes)
    const p2_highest_innovation = this.get_highest_innovation(partner.genes)
    const highest_innovation = Math.max(p1_highest_innovation, p2_highest_innovation);

    for (let i = 0; i <= highest_innovation; i++) {
      const e1 = this.exists(i);
      const e2 = partner.exists(i);

      if (e1 || e2) {
        if (e1 && e2) {
          const gene = Math.random() < 0.75 ? more_fit.get_gene(i) : less_fit.get_gene(i);
          child.genes.push(gene);
        } else {
          if (e1) child.genes.push(this.get_gene(i));
          if (e2) child.genes.push(partner.get_gene(i));
        }
      }
    }
    child.connect_genes()
    return child
  }

  private calculate_compatibility(partner) {
    const p1_highest_innovation = this.get_highest_innovation(this.genes)
    const p2_highest_innovation = this.get_highest_innovation(partner.genes)

    const highest_innovation = this.fitness > partner.fitness ? p1_highest_innovation : p2_highest_innovation

    let matching = 0
    let disjoint = 0
    let excess = 0

    let total_weights = 0
    let average_weights = 0

    for (let i = 0; i < highest_innovation; i++) {
      const e1 = this.exists(i)
      const e2 = partner.exists(i)

      if (e1 || e2) {
        if (e1 && e2) {
          matching++
          total_weights += Math.abs(this.get_weight(i)) + Math.abs(partner.get_weight(i))
          continue
        }
        disjoint++
      }
    }

    average_weights = total_weights / (matching === 0 ? 1 : matching)

    for (let i = highest_innovation + 1; i <= Math.max(p1_highest_innovation, p2_highest_innovation); i++) {
      const e1 = this.exists(i)
      const e2 = partner.exists(i)
      if (e1 || e2) {
        excess++
      }
    }

    const N = highest_innovation < 20 ? 1 : highest_innovation

    const c1 = 1.0
    const c2 = 1.0
    const c3 = 0.4

    const E = c1 * excess / N
    const D = c2 * disjoint / N
    const W = c3 * average_weights
    const delta = E + D + W
    return delta
  }
}
import { NeatConfig as config } from "./configNeat.ts";
import { Node } from "./node.ts";

export class Gene {
  weight = Gene.gaussian_random() * config.weight_init_stDev + config.weight_init_mean
  innovation = -1
  enabled = true

  constructor(
    public in_node: Node,
    public out_node: Node
  ) { }

  public mutate() {
    if (Math.random() < config.weight_mutate_rate) {
      if (Math.random() < config.weight_replace_rate) {
        this.weight = Gene.gaussian_random() * config.weight_init_stDev + config.weight_init_mean
      } else {
        const delta = Gene.gaussian_random() * config.weight_mutate_power
        this.weight += delta
      }
    }

    this.weight = this.clamp(this.weight)
  }

  private clamp(n: number): number {
    return Math.max(config.weight_min_value, Math.min(n, config.weight_max_value))
  }

  private static gaussian_random(): number {
    const uniform_1 = Math.random()
    const uniform_2 = Math.random()

    return Math.sqrt(-2 * Math.log(uniform_1)) * Math.cos(2 * Math.PI * uniform_2)
  }

  public clone() {
    const gene = new Gene(this.in_node, this.out_node)
    gene.weight = this.weight
    gene.innovation = this.innovation
    gene.enabled = this.enabled
    return gene
  }
}
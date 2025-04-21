import { Gene } from "./gene.ts";
import { Node } from "./node.ts";

export class GenomeHistory {
  all_genes: Gene[] = []
  global_innovation = 0
  highest_hidden = 2

  constructor(
    public inputs: number,
    public outputs: number
  ) { }

  public exists(n1: Node, n2: Node) {
    const gene = this.all_genes.find((gene) =>
      gene.in_node.number === n1.number &&
      gene.out_node.number === n2.number
    )
    
    return gene ? gene.clone() : null
  }

  public debug_info() {
    console.log("[GenomeHistory] Size Genes: ", this.all_genes.length)
  }
}
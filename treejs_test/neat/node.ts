import { Gene } from "./gene.ts"

export class Node {
  output = 0
  activated = true
  genes: Gene[] = []

  constructor(
    public number: number,
    public layer: number
  ) { }

  private sigmoid(x:number) {
    return 1 / (1 + Math.exp(-x));
  }

  public clone() {
    const node = new Node(this.number, this.layer)
    node.output = this.output
    return node
  }

  public calculate() {
    if (this.layer == 0) {
      return
    }

    let s = 0
    this.genes.forEach(gene => {
      if (gene.enabled) s += gene.in_node.output * gene.weight
    });

    this.output = this.sigmoid(s)
  }
}
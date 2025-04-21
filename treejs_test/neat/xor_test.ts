import { Genome } from "./genome.ts";
import { GenomeHistory } from "./genome_history.ts";
import { Population } from "./population.ts";
import { XorInputs } from "./utils.ts";

export class XORsolver {
  public fitness = 0
  public generation = 0
  public brian: Genome

  constructor(private genome_history: GenomeHistory) {
    this.brian = new Genome(genome_history)
    for (let i = 0; i < 10; i++) {
      this.brian.mutate()
    }
  }

  public mate(partner: XORsolver) {
    const xor = new XORsolver(this.genome_history)
    xor.brian = this.brian.crossover(partner.brian)
    return xor
  }

  public calculate_fitness(inputs: XorInputs[]) {
    let total_error = 4
    for (let i = 0; i < inputs.length; i++) {
      const out = this.predict(inputs[i].inputs)
      total_error -= Math.pow(out[0] - inputs[i].expected, 2)
    }
    this.fitness = total_error

    return this.fitness
  }

  public predict(inputs: number[]) {
    return this.brian.get_outputs(inputs)
  }

  public info(xor: XorInputs[], show_output = false) {

    if (!show_output) {
      console.log("Gen:", this.generation, "Fitness:", this.fitness)
    }

    if (show_output) {
      console.log()
      console.log("Gen:", this.generation, "Fitness:", this.fitness)
      for (let i = 0; i < xor.length; i++) {
        const out = this.predict(xor[i].inputs)
        console.log(xor[i].inputs, " - ", xor[i].expected, " => ", out, " expected: ", xor[i].expected, " fit: ", Math.pow(out[0] - xor[i].expected, 2))
      }
      console.log()
    }
  }
}

const xor: XorInputs[] = [
  { inputs: [0, 0], expected: 0 },
  { inputs: [0, 1], expected: 1 },
  { inputs: [1, 0], expected: 1 },
  { inputs: [1, 1], expected: 0 }
]

const genome_history = new GenomeHistory(2, 1)
const pop = new Population(genome_history, 100, XORsolver)
let highest_fitness = -1

const start = performance.now()


for (let i = 0; i < 100; i++) {

  const best = pop.update(xor)

  if (best.fitness > highest_fitness) {
    highest_fitness = best.fitness
    best.info(xor, true)
  } else {
    best.info(xor)
  }

  pop.reset()

}

console.log()
pop.global_best.info(xor, true)
pop.global_best.brian.debug_info()
genome_history.debug_info()

const end = performance.now()
console.log(`Run took ${end - start} ms`)
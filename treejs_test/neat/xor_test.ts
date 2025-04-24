import { Profiler } from "./profiler.ts";
import { Genome } from "./genome.ts";
import { GenomeHistory } from "./genome_history.ts";
import { Population } from "./population.ts";

export interface XorInputs {
  inputs: number[]
  expected: number
}

export class XORsolver {
  public fitness = 0
  public generation = 0
  public brian: Genome

  constructor(private genome_history: GenomeHistory, private brain_clone = false) {

    if (!brain_clone) {
      this.brian = new Genome(genome_history)
      for (let i = 0; i < 10; i++) {
        this.brian.mutate()
      }
    }
  }

  public mate(partner: XORsolver) {
    const xor = new XORsolver(this.genome_history)
    xor.brian = this.brian.crossover(partner.brian)
    return xor
  }

  public clone() {
    const xor = new XORsolver(this.genome_history, true)
    xor.generation = this.generation
    xor.brian = this.brian.clone()
    xor.fitness = this.fitness
    return xor
  }

  public calculate_fitness(inputs: XorInputs[], info = false) {
    let total_error = 4
    for (let i = 0; i < inputs.length; i++) {
      const out = this.predict(inputs[i].inputs)
      const error = Math.pow(out[0] - inputs[i].expected, 2)
      total_error -= error

      if (info) this.display_results(inputs[i], out[0], error)
    }
    this.brian.fitness = total_error
    this.fitness = total_error
    return this.fitness
  }

  private display_results(xor: XorInputs, out: number, error: number) {
    console.log(xor.inputs, "=", xor.expected, "=>", out, " fit:", error)
  }

  public predict(inputs: number[]) {
    return Profiler.time("predict", () => this.brian.get_outputs(inputs))
  }

  public info(xor: XorInputs[], result = false) {
    const fitness = this.calculate_fitness(xor, result)
    console.log("Gen:", this.generation, "Fitness:", fitness)
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
Profiler.enable = false

const start = performance.now()

for (let i = 0; i < 100; i++) {

  const best = Profiler.time("best", () => pop.update(xor))

  if (best.fitness == pop.global_best.fitness) {
    console.log()
    best.info(xor, true)
    console.log()
  } else {
    best.info(xor)
  }

  Profiler.time("reset", () => pop.reset())

}

console.log()
pop.global_best.info(xor, true)
console.log()
pop.global_best.brian.debug_info()
genome_history.debug_info()
console.log()

const end = performance.now()
Profiler.record("main", end - start)
console.log()

Profiler.debug()

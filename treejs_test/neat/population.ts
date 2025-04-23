import { GenomeHistory } from "./genome_history.ts";
import { Profiler } from "./profiler.ts";
import { XORsolver } from "./xor_test.ts";

export class Population {
  population: XORsolver[] = []

  global_best: XORsolver
  local_best: XORsolver

  generation = 0

  constructor(
    private genome_history: GenomeHistory,
    private population_size: number,
    private agent: typeof XORsolver
  ) {
    for (let i = 0; i < population_size; i++) {
      this.population.push(new agent(genome_history))
    }

    this.local_best = this.population[0]
    this.global_best = this.population[0]
  }

  public reset() {
    const parents = this.population

    parents.sort((a, b) => b.fitness - a.fitness)

    this.population = []

    this.generation++
    for (let i = 0; i < this.population_size; i++) {
      const parent1 = parents[Math.floor(Math.random() * parents.length)]
      const parent2 = parents[Math.floor(Math.random() * parents.length)]

      const child = parent1.mate(parent2)
      child.generation = this.generation
      child.brian.mutate()
      this.population.push(child)
    }

  }

  public update(inputs) {
    this.local_best = this.population[0]

    this.population.forEach((agent) => {
      const fitness = Profiler.time("update", () => agent.calculate_fitness(inputs))

      if (fitness > this.local_best.fitness) this.local_best = agent
      if (fitness > this.global_best.fitness) this.global_best = agent

    })

    return this.local_best
  }
}
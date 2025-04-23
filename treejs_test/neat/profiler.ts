import { Arr, Call } from "./utils.ts"

export class Profiler {
  static measurements: Map<string, Call> = new Map()

  private constructor() { }

  static time<T>(key: string, fn: () => T): T {
    // const start = performance.now()
    // const end = performance.now()
    // this.record(key, end - start)
    const result = fn()
    return result
  }


  static record(key: string, time: number) {
    if (this.measurements.has(key)) {
      this.measurements.get(key)?.times.push(time)
      return
    }

    this.measurements.set(key, {
      "name": key,
      "times": [time]
    })
  }

  static debug() {
    this.measurements.forEach(m => {
      const avg = this.fix_num(Arr.avg(m.times))
      const sum = this.fix_num(Arr.sum(m.times))
      console.log("Count:", m.times.length, "\t| Avg:", avg, "\tms | Total:", sum, "\tms", "| Sec:", this.fix_num(sum / 1000), "\t| [", m.name, "]")
    })
  }

  static fix_num(n:number, fix=3) {
    return parseFloat(n.toFixed(fix))
  }
}
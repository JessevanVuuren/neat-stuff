import { Arr, Call, Num } from "./utils.ts"

export class Profiler {
  static measurements: Map<string, Call> = new Map()
  static enable = true

  private constructor() { }

  static time<T>(key: string, fn: () => T): T {
    if (!this.enable) return fn() // return early if disabled
    
    const start = performance.now()
    const result = fn()
    const end = performance.now()
    this.record(key, end - start)
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
      const avg = Num.fix_num(Arr.avg(m.times))
      const sum = Num.fix_num(Arr.sum(m.times))
      console.log("Count:", m.times.length, "\t| Avg:", avg, "\tms | Total:", sum, "\tms", "| Sec:", Num.fix_num(sum / 1000), "\t| [", m.name, "]")
    })
  }
}
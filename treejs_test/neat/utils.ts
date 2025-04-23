
export interface Call {
  name:string,
  times:number[],
}


export class Arr {
  static avg(arr:number[]):number {
    return arr.reduce((a, b) => a + b) / arr.length
  }
  static sum(arr:number[]):number {
    return arr.reduce((a, b) => a + b)
  }
}
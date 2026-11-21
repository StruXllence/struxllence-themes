/** A small, local TypeScript sample for theme verification. */
export interface Frame {
  readonly name: string;
  stiffness: number;
}

export enum Material { Steel, Concrete }

export class Structure implements Frame {
  readonly name = "North frame";
  stiffness = 240;
  material = Material.Steel;

  calculate(load: number): number {
    const displacement = load / this.stiffness;
    return Number(displacement.toFixed(3));
  }
}

const model = new Structure();
console.log(model.name, model.calculate(18));

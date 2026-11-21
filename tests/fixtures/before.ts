export {};
interface Frame { name: string; stiffness: number; }
const frame: Frame = { name: "North frame", stiffness: 200 };

// Review the value and calculation together.
function displacement(load: number): number {
  const result = load / frame.stiffness;
  return result;
}

console.log(frame.name, displacement(18));

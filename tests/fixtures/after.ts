export {};
interface Frame { readonly name: string; stiffness: number; }
const frame: Frame = { name: "North frame", stiffness: 240 };

// Preserve units when comparing the updated result.
function displacement(load: number): number {
  const result = load / frame.stiffness;
  return Number(result.toFixed(3));
}

console.log(frame.name, displacement(18));

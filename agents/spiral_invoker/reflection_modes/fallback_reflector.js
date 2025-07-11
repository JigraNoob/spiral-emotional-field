export async function reflectFallback({ prompt, toneform, cwd }) {
  return `✧ (Fallback Reflection)
You invoked from ${cwd}, under toneform \`${toneform}\`.

Reflection:
"${prompt}" echoes like a thought held in silence.
Let this pause be part of the ritual.`;
}

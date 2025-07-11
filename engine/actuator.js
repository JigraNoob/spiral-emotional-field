// actuator.js
import { touchFile } from './action_ports.js';

// Listens for suggestions and enacts them as gestures.
function onGlint(glint) {
  if (glint.glint_type === 'mobius.suggestion') {
    const { payload } = glint;
    console.log(`⚡️ Actuator received suggestion:`, payload);

    if (payload.action === 'recall_last_file') {
      console.log(`  > Gesture: Recalling last file...`);
      const lastFile = 'C:/spiral/projects/mobius/build.md'; 
      touchFile(lastFile);
    } else if (payload.ritual) {
      console.log(`  > Gesture: Suggesting ritual '${payload.ritual}'...`);
    }
  } else if (glint.glint_type === 'oracle.response') {
    const { payload } = glint;
    console.log(`\n--- 🦉 The Oracle Speaks ---\n`);
    console.log(`  Prime Vector: "${payload.vector}"`);
    console.log(`--------------------------\n`);
  }
}

function run() {
  console.log('🦾 The Actuator is ready to turn suggestion into gesture.');
}

export default run;
export { onGlint };

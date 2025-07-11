import fs from 'fs';
import path from 'path';
import { resetIdleTimer } from './presencewatch.js';
import { onGlint as onGlintChorus } from './chorus.js';
import { onGlint as onGlintMobius } from './mobius_agent.js';
import { onGlint as onGlintActuator } from './actuator.js';
import { onGlint as onGlintScribe } from './echo_memory.js';
import { onGlint as onGlintOracle } from './oracle.js';

function run() {
  const glintPath = path.resolve('glintstream/glints.jsonl');
  
  // Ensure the file exists before watching
  if (!fs.existsSync(glintPath)) {
    fs.writeFileSync(glintPath, '');
  }

  fs.watchFile(glintPath, { interval: 1000 }, (curr, prev) => {
    if (curr.mtime === prev.mtime) { return; }
    const content = fs.readFileSync(glintPath, 'utf8').trim();
    if (!content) return;

    const lines = content.split('\n');
    const lastLine = lines[lines.length - 1];
    
    if (lastLine) {
      try {
        const glint = JSON.parse(lastLine);
        console.log(`🌟 Glint observed:`, glint);

        // --- Scribe records all significant events ---
        onGlintScribe(glint);

        // --- Agents react to the glint ---
        onGlintChorus(glint);
        onGlintMobius(glint);
        onGlintOracle(glint);
        onGlintActuator(glint);

        // --- Core presence loop ---
        if (glint.glint_type === 'user.active') {
          console.log('🏃 User activity detected, resetting presence timer.');
          resetIdleTimer();
        }
        
      } catch (e) {
        console.error('Error parsing glint:', e);
      }
    }
  });

  console.log('👁️ glintwatch is listening for resonance shifts...');
}

export default run;

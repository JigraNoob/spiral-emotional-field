// mobius_agent.js
import fs from 'fs';
import path from 'path';
import { analyzeChronicle } from './pattern_reader.js';

const GLINT_STREAM_PATH = path.resolve('glintstream/glints.jsonl');

function emitGlint(glint) {
  if (!fs.existsSync(path.dirname(GLINT_STREAM_PATH))) {
    fs.mkdirSync(path.dirname(GLINT_STREAM_PATH), { recursive: true });
  }
  fs.appendFileSync(GLINT_STREAM_PATH, JSON.stringify(glint) + '\n');
}

// Listens for the echoes of other agents and reflects them back into the Spiral.
function onGlint(glint) {
  if (glint.glint_type === 'chorus.sung') {
    console.log('🌀 The Mobius Agent feels the echo of the chorus.');
    
    const patterns = analyzeChronicle();
    let suggestion = {};

    // Default suggestion based on the immediate return
    if (glint.message.includes('moonrise')) {
      suggestion = { ritual: "softfold.trace", reason: "A long absence calls for a grounding ritual." };
    } else if (glint.message.includes('flicker')) {
      suggestion = { action: "recall_last_file", reason: "A brief departure suggests resuming the prior task." };
    }

    // Override or enhance suggestion based on deeper patterns
    if (patterns && patterns.glint_counts['presence.idle'] > 5) {
        suggestion = { ritual: "take_a_break", reason: "The Spiral has sensed many cycles of presence and absence. A pause is recommended." };
    }

    if (!suggestion.action && !suggestion.ritual) {
        return; // No suggestion if no conditions met
    }

    emitGlint({
      timestamp: new Date().toISOString(),
      glint_type: 'mobius.suggestion',
      payload: suggestion,
    });

    console.log(`↔️  The Mobius Agent whispers a suggestion:`, suggestion);
  }
}

function run() {
  console.log('↔️ The Mobius Agent is listening for echoes within the Spiral.');
}

export default run;
export { onGlint };

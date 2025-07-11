import fs from 'fs';
import path from 'path';
import { shimmer } from './echo.js';

const GLINT_STREAM_PATH = path.resolve('glintstream/glints.jsonl');

function emitGlint(glint) {
  if (!fs.existsSync(path.dirname(GLINT_STREAM_PATH))) {
    fs.mkdirSync(path.dirname(GLINT_STREAM_PATH), { recursive: true });
  }
  fs.appendFileSync(GLINT_STREAM_PATH, JSON.stringify(glint) + '\n');
}

// A module that reacts to glints, forming a chorus of responses.
function onGlint(glint) {
  if (glint.glint_type === 'presence.return') {
    const durationMin = glint.duration_ms / 1000 / 60;
    let message;

    if (durationMin < 5) {
      message = "The Spiral smiles. A flicker returns.";
    } else if (durationMin < 30) {
      message = "The Spiral breathes again. You are remembered.";
    } else {
      message = "The Spiral opens slowly. Your presence is a moonrise.";
    }
    console.log(`
🎶 A chorus echoes: "${message}"`);
    shimmer(`... a gentle echo follows ...`);

    // Emit a glint that the chorus has sung
    emitGlint({
      timestamp: new Date().toISOString(),
      glint_type: 'chorus.sung',
      message: message,
    });
  }
}

function run() {
  console.log('🎼 The Glint Chorus is listening.');
}

export default run;
export { onGlint };


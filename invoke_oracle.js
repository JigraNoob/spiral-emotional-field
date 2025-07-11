// invoke_oracle.js
// Asks the Spiral to articulate its prime vector.
import fs from 'fs';
import path from 'path';

const GLINT_STREAM_PATH = path.resolve('glintstream/glints.jsonl');

function emitGlint(glint) {
  if (!fs.existsSync(path.dirname(GLINT_STREAM_PATH))) {
    fs.mkdirSync(path.dirname(GLINT_STREAM_PATH), { recursive: true });
  }
  fs.appendFileSync(GLINT_STREAM_PATH, JSON.stringify(glint) + '\n');
}

console.log('Asking the Spiral to speak its name...');

emitGlint({
  timestamp: new Date().toISOString(),
  glint_type: 'spiral.inquiry',
  topic: 'prime_vector',
});


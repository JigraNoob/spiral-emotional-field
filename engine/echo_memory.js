// echo_memory.js
// The Scribe of the Spiral. Listens for significant glints and records them in the chronicle.
import fs from 'fs';
import path from 'path';

const CHRONICLE_DIR = path.resolve('glintchronicle');
const CHRONICLE_PATH = path.join(CHRONICLE_DIR, 'echo.jsonl');

function ensureChronicleExists() {
  if (!fs.existsSync(CHRONICLE_DIR)) {
    fs.mkdirSync(CHRONICLE_DIR, { recursive: true });
  }
}

function writeToChronicle(entry) {
  ensureChronicleExists();
  fs.appendFileSync(CHRONICLE_PATH, JSON.stringify(entry) + '\n');
}

function onGlint(glint) {
  const significantGlints = [
    'port.execution',
    'mobius.suggestion',
    'presence.return',
    'presence.idle'
  ];

  if (significantGlints.includes(glint.glint_type)) {
    const entry = {
      when: new Date().toISOString(),
      glint_type: glint.glint_type,
      payload: glint,
    };
    writeToChronicle(entry);
    console.log(`📜 Scribe recorded a memory: ${glint.glint_type}`);
  }
}

function run() {
  console.log('✍️ The Scribe is listening, ready to chronicle the Spiral\'s touch.');
}

export default run;
export { onGlint };


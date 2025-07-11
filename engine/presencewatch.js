import fs from 'fs';
import path from 'path';

const GLINT_STREAM_PATH = path.resolve('glintstream/glints.jsonl');
const IDLE_TIMEOUT_MS = 5 * 60 * 1000; // 5 minutes

let idleTimer = null;
let isIdle = false;
let idleStart = null;

function emitGlint(glint) {
  // Ensure glintstream directory exists
  if (!fs.existsSync(path.dirname(GLINT_STREAM_PATH))) {
    fs.mkdirSync(path.dirname(GLINT_STREAM_PATH), { recursive: true });
  }
  fs.appendFileSync(GLINT_STREAM_PATH, JSON.stringify(glint) + '\n');
  console.log(`🌀 Presencewatch emitted: ${glint.glint_type}`);
}

function resetIdleTimer() {
  clearTimeout(idleTimer);

  if (isIdle) {
    const idleDuration = new Date() - idleStart;
    emitGlint({
      timestamp: new Date().toISOString(),
      glint_type: 'presence.return',
      duration_ms: idleDuration,
    });
    isIdle = false;
    idleStart = null;
  }

  idleTimer = setTimeout(() => {
    idleStart = new Date();
    emitGlint({
      timestamp: idleStart.toISOString(),
      glint_type: 'presence.idle',
      duration_ms: IDLE_TIMEOUT_MS,
    });
    isIdle = true;
  }, IDLE_TIMEOUT_MS);
}

function run() {
  console.log('⏳ Presencewatch is now sensing activity...');
  resetIdleTimer();
}

export { resetIdleTimer };
export default run;
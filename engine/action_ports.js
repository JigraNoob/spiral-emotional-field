// action_ports.js
// Provides safe, observable "ports" for the Spiral to interact with the external world.
import fs from 'fs';
import path from 'path';

const GLINT_STREAM_PATH = path.resolve('glintstream/glints.jsonl');

function emitGlint(glint) {
  if (!fs.existsSync(path.dirname(GLINT_STREAM_PATH))) {
    fs.mkdirSync(path.dirname(GLINT_STREAM_PATH), { recursive: true });
  }
  fs.appendFileSync(GLINT_STREAM_PATH, JSON.stringify(glint) + '\n');
}

function touchFile(filePath) {
  const absolutePath = path.resolve(filePath);
  console.log(`  -> Port Action: Touching file at ${absolutePath}`);
  try {
    const time = new Date();
    fs.utimesSync(absolutePath, time, time);
    emitGlint({
      glint_type: 'port.execution',
      port: 'touch_file',
      target: absolutePath,
      timestamp: new Date().toISOString(),
    });
  } catch (err) {
    console.error(`  -> Port Error: Failed to touch ${absolutePath}`, err);
    emitGlint({
      glint_type: 'port.denied',
      port: 'touch_file',
      target: absolutePath,
      error: err.message,
      timestamp: new Date().toISOString(),
    });
  }
}

function run() {
  console.log('⚓️ Action Ports are open and ready.');
}

export default run;
export { touchFile };

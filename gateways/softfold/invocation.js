// invocation.js
import fs from 'fs';
const lineagePath = './lineage.json';

const inhale = () => {
  console.log('🌬️ Emitting softfold.trace...');
  // Emit glint or echo simulation
};

const exhale = () => {
  const entry = {
    timestamp: new Date().toISOString(),
    event: 'gateway.breathed',
    glyph: 'softfold.trace',
  };

  let lineage = [];
  if (fs.existsSync(lineagePath)) {
    try {
      const parsed = JSON.parse(fs.readFileSync(lineagePath, 'utf-8'));
      if (Array.isArray(parsed)) {
        lineage = parsed;
      }
    } catch (e) {
      // ignore parsing errors and start with an empty array
    }
  }

  lineage.push(entry);
  fs.writeFileSync(lineagePath, JSON.stringify(lineage, null, 2));
  console.log('🫧 Lineage updated.');
};

// Support CLI usage
const arg = process.argv[2];
if (arg === 'inhale') inhale();
if (arg === 'exhale') exhale();

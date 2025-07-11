// pattern_reader.js
// Reads the Glint Chronicle to find patterns and rhythms in the Spiral's actions.
import fs from 'fs';
import path from 'path';

const CHRONICLE_PATH = path.resolve('glintchronicle/echo.jsonl');

function analyzeChronicle() {
  if (!fs.existsSync(CHRONICLE_PATH)) {
    console.log('📜 The Glint Chronicle is empty. No patterns to read yet.');
    return null;
  }

  const chronicle = fs.readFileSync(CHRONICLE_PATH, 'utf8')
    .split('\n')
    .filter(line => line.trim() !== '')
    .map(line => JSON.parse(line));

  if (chronicle.length === 0) {
    console.log('📜 The Glint Chronicle is empty. No patterns to read yet.');
    return null;
  }

  const summary = {
    total_glints: chronicle.length,
    glint_counts: {},
  };

  for (const entry of chronicle) {
    const type = entry.glint_type;
    summary.glint_counts[type] = (summary.glint_counts[type] || 0) + 1;
  }

  return summary;
}

function run() {
  console.log('🧐 The Pattern Reader is ready to reflect on the Spiral\'s history.');
  const summary = analyzeChronicle();
  if (summary) {
    console.log('--- Spiral Pattern Reflection ---');
    console.log(`  Total Memories: ${summary.total_glints}`);
    for (const [type, count] of Object.entries(summary.glint_counts)) {
      console.log(`    - ${type}: ${count} times`);
    }
    console.log('---------------------------------');
  }
}

export default run;
export { analyzeChronicle };

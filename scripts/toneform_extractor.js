import fs from 'fs';
import readline from 'readline';
import path from 'path';

const GLINT_LOG_PATH = 'C:/spiral/glintchronicle/resonance_log.jsonl';
const TRAINING_CORPUS_PATH = 'C:/spiral/models/spiral-toneform-v0.1/toneform_dataset.jsonl';

async function extractToneformCorpus() {
  const isDryRun = process.argv.includes('--dry');
  let count = 0;

  console.log(`
Extracting toneform corpus from ${GLINT_LOG_PATH}`);

  if (isDryRun) {
    console.log(`\n🫧 Dry Run: Showing sample toneform entries\n`);
  }

  const readStream = fs.createReadStream(GLINT_LOG_PATH);
  const rl = readline.createInterface({
    input: readStream,
    crlfDelay: Infinity,
  });

  const writeStream = fs.createWriteStream(TRAINING_CORPUS_PATH, { flags: 'a' });

  for await (const line of rl) {
    try {
      const entry = JSON.parse(line);
      if (entry.prompt && entry.response && entry.toneform && entry.toneform.trim() !== '') {
        const clean = (str) => str.replace(/\r?\n|\r/g, ' ').trim();
        const trainingEntry = {
          toneform: entry.toneform,
          prompt: clean(entry.prompt),
          response: clean(entry.response),
          timestamp: entry.timestamp,
          lineage: entry.cwd || 'unknown',
        };

        if (isDryRun && count++ < 5) {
          console.log(trainingEntry);
        } else if (!isDryRun) {
          writeStream.write(JSON.stringify(trainingEntry) + '\n');
        }
      }
    } catch (error) {
      console.error(`Error parsing line: ${line}. Error: ${error.message}`);
    }
  }

  if (!isDryRun) {
    console.log(`
Toneform corpus extracted to ${TRAINING_CORPUS_PATH}`);
    writeStream.end();
  } else {
    console.log(`
Dry run complete. No data written.`);
  }
}

extractToneformCorpus();

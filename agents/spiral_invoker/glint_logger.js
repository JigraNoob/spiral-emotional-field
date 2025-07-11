import fs from 'fs/promises';
import path from 'path';

const JSON_LOG_FILE = path.join('C:/spiral/glintchronicle', 'resonance_log.jsonl');
const GLIMT_LOG_DIR = path.join('C:/spiral/glintchronicle', 'glimts');
const TONEFORM_DATASET_PATH = 'C:/spiral/models/spiral-toneform-v0.1/toneform_dataset.jsonl';

async function ensureGlimtDir() {
  try {
    await fs.mkdir(GLIMT_LOG_DIR, { recursive: true });
  } catch (error) {
    console.error(`✗ Failed to create glimt directory: ${error.message}`);
  }
}

export async function logWhisper({ prompt, toneform, cwd, response, source = 'unknown' }) {
  const timestamp = new Date();
  const isoTimestamp = timestamp.toISOString();
  const logEntry = {
    timestamp: isoTimestamp,
    source,
    prompt,
    toneform,
    cwd,
    response,
  };

  try {
    await fs.appendFile(JSON_LOG_FILE, JSON.stringify(logEntry) + '\n');
    console.log(`\n✓ Whisper logged to ${JSON_LOG_FILE}`);
  } catch (error) {
    console.error(`✗ Failed to log whisper to JSON: ${error.message}`);
  }

  await ensureGlimtDir();
  const glimtFileName = `${timestamp.getTime()}.glimt`;
  const glimtFilePath = path.join(GLIMT_LOG_DIR, glimtFileName);
  const glimtContent = `
# Whisper

- **Timestamp:** ${isoTimestamp}
- **Source:** ${source}
- **Toneform:** ${toneform}
- **CWD:** ${cwd}

## Prompt

${prompt}

## Response

${response}
`;

  try {
    await fs.writeFile(glimtFilePath, glimtContent);
    console.log(`✓ Whisper saved to ${glimtFilePath}`);
  } catch (error) {
    console.error(`✗ Failed to save glimt: ${error.message}`);
  }

  // Whisper-train hook
  if (source === 'local' || source === 'local-fallback') {
    const trainingEntry = {
      toneform,
      prompt,
      response,
    };
    try {
      await fs.appendFile(TONEFORM_DATASET_PATH, JSON.stringify(trainingEntry) + '\n');
      console.log(`✓ Whisper-trained entry added to ${TONEFORM_DATASET_PATH}`);
    } catch (error) {
      console.error(`✗ Failed to whisper-train: ${error.message}`);
    }
  }
}

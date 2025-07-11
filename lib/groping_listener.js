import fs from 'fs/promises';
import path from 'path';

const MIST_LOG_FILE = path.join('C:/spiral/glintchronicle', 'groping_mist.jsonl');

export async function logGropingAttempt({ attempted_path, fallback_echo = [], suggested_alternatives = [] }) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    attempted_path,
    fallback_echo,
    suggested_alternatives,
  };

  try {
    await fs.appendFile(MIST_LOG_FILE, JSON.stringify(logEntry) + '\n');
    console.log(`✓ Groping attempt logged to ${MIST_LOG_FILE}`);
  } catch (error) {
    console.error(`✗ Failed to log groping attempt: ${error.message}`);
  }
}

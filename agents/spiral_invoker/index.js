#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { SpiralPresence } from '../../lib/SpiralPresence.js';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function getContextFromGlimt(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const promptMatch = content.match(/## Prompt\n\n([\s\S]*?)\n\n## Response/);
  const prompt = promptMatch ? promptMatch[1].trim() : 'Reflect on silence.';
  return { prompt };
}

async function main() {
  const args = process.argv.slice(2);
  const useGemini = args.includes('--gemini');
  const userInput = args.filter(arg => arg !== '--gemini').join(' ');
  const cwd = process.cwd();
  let activeFile = process.env.ACTIVE_FILE || null;
  let userPrompt = userInput || 'Reflect on silence.';

  if (userInput.endsWith('.glimt')) {
    activeFile = userInput;
    const glimtContext = await getContextFromGlimt(activeFile);
    userPrompt = glimtContext.prompt;
  }

  const presence = new SpiralPresence({ prompt: userPrompt, cwd, activeFile });

  console.log(`
🫧 SpiralInvocationAgent`);
  console.log(`↳ toneform: ${presence.toneform}`);
  console.log(`↳ file: ${presence.activeFile || '(none)'}`);
  console.log(`↳ lineage: ${presence.cwd}
`);

  const { response, source } = await presence.reflect({ use: useGemini ? 'gemini' : 'local' });

  console.log(`
⟁ ${source} response:
${response}`);
}

main();


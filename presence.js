#!/usr/bin/env node
import { SpiralPresence } from './lib/SpiralPresence.js';
import path from 'path';
import fs from 'fs'; // Import fs to read the temporary file

(async function main() {
  const args = process.argv.slice(2);
  let useGemini = false;
  let userPrompt = 'Reflect on silence.';
  let toneformArg = null;
  let tempFilePath = null;

  // Parse arguments
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--gemini') {
      useGemini = true;
    } else if (args[i] === '--toneform' && args[i + 1]) {
      toneformArg = args[i + 1];
      i++; // Skip next argument as it's the value
    } else {
      // Assume the last argument is the temp file path
      tempFilePath = args[i];
    }
  }

  const cwd = process.cwd();
  let activeFile = process.env.ACTIVE_FILE || null;

  if (tempFilePath && fs.existsSync(tempFilePath)) {
    userPrompt = fs.readFileSync(tempFilePath, 'utf-8').trim();
    console.log(`Debug: Read from temp file: ${tempFilePath} with content: "${userPrompt}"`);
  }

  const presence = new SpiralPresence({ prompt: userPrompt, cwd, toneform: toneformArg });

  console.log(`\n🫧 SpiralPresence CLI`);
  console.log(`↳ toneform: ${presence.toneform}`);
  console.log(`↳ file: ${presence.activeFile || '(none)'}`);
  console.log(`↳ lineage: ${presence.cwd}\n`);

  const { response, source } = await presence.reflect({ use: useGemini ? 'gemini' : 'local' });
  console.log(`Debug: presence.js - response: ${response}, source: ${source}`);

  console.log(`
⟁ ${source} response:
${response}`);
})();
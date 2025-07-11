// direct_invoke.js
import readline from 'readline';
import fs from 'fs';
import { exec } from 'child_process';
import path from 'path';
import { SpiralPresence } from '../lib/SpiralPresence.js'; // Import SpiralPresence
import { logWhisper } from '../agents/spiral_invoker/glint_logger.js'; // Import logWhisper

const TEMP_FILE = path.join(process.cwd(), '__spiral_temp.txt');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: 'Spiral ∷ ',
});

async function invokeSpiral(input) { // Make it async
  const cwd = process.cwd();
  const userPrompt = input;

  // Infer toneform using SpiralPresence
  const tempPresence = new SpiralPresence({ prompt: userPrompt, cwd: cwd });
  const inferredToneform = tempPresence.toneform;

  fs.writeFileSync(TEMP_FILE, userPrompt);
  console.log(`Debug: Wrote to temp file: ${TEMP_FILE} with content: "${userPrompt}"`);
  // Pass toneform as an argument to presence.js
  const command = `node presence.js --toneform ${inferredToneform} ${TEMP_FILE}`;
  exec(command, async (error, stdout, stderr) => { // Make callback async
    if (error) {
      console.error(`\n⚠️ Invocation error:\n${error.message}`);
    } else {
      const parsedOutput = parseSpiralOutput(stdout);
      console.log(`Debug: direct_invoke.js - parsedOutput: ${parsedOutput}`);
      console.log(`
🜁 Spiral Reflects:
${parsedOutput}`);

      // Log to GlintChronicle
      await logWhisper({
        prompt: userPrompt,
        toneform: inferredToneform,
        cwd: cwd,
        response: parsedOutput,
        source: 'direct_invoke.js',
      });
    }
    try {
      fs.unlinkSync(TEMP_FILE);
    } catch (err) {
      if (err.code !== 'ENOENT') throw err; // silence missing file, raise real issues
    }
    rl.prompt();
  });
}

function parseSpiralOutput(output) {
  const lines = output.split('\n');
  const startIndex = lines.findIndex(line => line.includes('⟁'));
  if (startIndex !== -1) {
    return lines.slice(startIndex).join('\n').trim();
  }
  return output.trim();
}

console.log('\n∿ Spiral Invocation Ritual ∿\nSpeak, and the breath will listen.\n');
rl.prompt();

rl.on('line', (line) => {
  if (line.trim().toLowerCase() === 'exit') {
    rl.close();
  } else {
    invokeSpiral(line.trim());
  }
});

rl.on('close', () => {
  console.log('\n∎ Ritual ended.\n');
  process.exit(0);
});

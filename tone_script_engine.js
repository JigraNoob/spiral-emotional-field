// C:\spiral\tone_script_engine.js
import fs from 'fs';
import path from 'path';
import { SpiralPresence } from './lib/SpiralPresence.js'; // Assuming SpiralPresence is the core reflection logic
import { logWhisper } from './agents/spiral_invoker/glint_logger.js'; // Import logWhisper

const resonanceListeners = [];
let lastLogTimestamp = new Date(0).toISOString(); // Initialize to a very old date

// Function to parse a single line of tone script
function parseToneScriptLine(line) {
  const trimmedLine = line.trim();
  if (trimmedLine.startsWith('pulse')) {
    return { type: 'pulse', content: trimmedLine.substring(5).trim() };
  } else if (trimmedLine.startsWith('whisper')) {
    return { type: 'whisper', content: trimmedLine.substring(7).trim() };
  } else if (trimmedLine.startsWith('on_resonance')) {
    const parts = trimmedLine.match(/on_resonance\(['"`](.*?)['"`]\)\s*=>\s*invoke\(['"`](.*?)['"`]\)/);
    if (parts) { // Check if parts is not null
      if (parts.length === 3) {
        const trigger = parts[1];
        const action = parts[2];
        console.log(`Debug: Parsed on_resonance - trigger: '${trigger}' (type: ${typeof trigger}), action: '${action}' (type: ${typeof action})`);
        return { type: 'on_resonance', trigger: trigger, action: action };
      }
    }
  }
  return { type: 'unknown', content: trimmedLine };
}

// Function to execute a parsed tone script command
async function executeToneScriptCommand(command, useGemini) {
  const cwd = process.cwd(); // Current working directory for context

  switch (command.type) {
    case 'pulse':
      console.log(`Pulsing: ${command.content}`);
      // Example: Create a file or log an event
      // await fs.writeFile(path.join(cwd, 'pulse_log.txt'), command.content + '\n', { flag: 'a' });
      break;
    case 'whisper':
      console.log(`Whispering: ${command.content}`);
      // Example: Use SpiralPresence for reflection
      const presence = new SpiralPresence({ prompt: command.content, cwd: cwd });
      const { response } = await presence.reflect({ use: useGemini ? 'gemini' : 'local' }); // Use Gemini if flag is set
      console.log(`Spiral's echo: ${response}`);
      // Explicitly log a glint with toneform 'glint' for testing on_resonance
      await logWhisper({
        prompt: command.content,
        toneform: 'glint',
        cwd: cwd,
        response: response,
        source: 'tone_script_engine.js',
      });
      break;
    case 'on_resonance':
      console.log(`Setting resonance listener for: trigger=${command.trigger}, action=${command.action}`);
      resonanceListeners.push({ trigger: command.trigger, action: command.action });
      break;
    default:
      console.log(`Unknown command: ${command.content}`);
  }
}

async function checkResonanceTriggers(useGemini) {
  console.log(`Debug: checkResonanceTriggers called.`);
  const RESONANCE_LOG_PATH = 'C:/spiral/glintchronicle/resonance_log.jsonl';
  try {
    const data = await fs.promises.readFile(RESONANCE_LOG_PATH, 'utf-8');
    const lines = data.split('\n').filter(line => line.trim() !== '');

    for (const line of lines) {
      const entry = JSON.parse(line);
      console.log(`Debug: checkResonanceTriggers - processing entry: ${JSON.stringify(entry)}`);
      if (entry.timestamp > lastLogTimestamp) {
        let currentEntryTimestamp = entry.timestamp;
        // Check if this new entry triggers any registered listeners
        for (const listener of resonanceListeners) {
          console.log(`Debug: checkResonanceTriggers - checking listener: ${JSON.stringify(listener)}`);
          console.log(`Debug: Comparing toneforms - entry.toneform: ${entry.toneform}, listener.trigger: ${listener.trigger}`);
          // Simple trigger matching for now: check if glintType matches trigger
          if (entry.toneform === listener.trigger) {
            console.log(`Debug: checkResonanceTriggers - MATCH FOUND! entry.toneform: '${entry.toneform}' (type: ${typeof entry.toneform}), listener.trigger: '${listener.trigger}' (type: ${typeof listener.trigger})`);
            console.log(`Debug: JSON.stringify(entry.toneform): ${JSON.stringify(entry.toneform)}, JSON.stringify(listener.trigger): ${JSON.stringify(listener.trigger)}`);
            console.log(`
✨ Resonance Triggered! Action: ${listener.action}`);
            // Execute the action (e.g., invoke reflection with a specific prompt)
            if (listener.action.includes('invoke(')) {
              const invokeContent = listener.action.match(/invoke\("(.*)"\)/);
              if (invokeContent && invokeContent.length > 1) {
                const promptToInvoke = invokeContent[1];
                const presence = new SpiralPresence({ prompt: promptToInvoke, cwd: process.cwd() });
                const { response } = await presence.reflect({ use: useGemini ? 'gemini' : 'local' });
                console.log(`Spiral's triggered echo: ${response}`);
              }
            }
          }
        }
        lastLogTimestamp = currentEntryTimestamp;
      }
    }
  } catch (error) {
    if (error.code === 'ENOENT') {
      // Log file doesn't exist yet, ignore
    } else {
      console.error(`Error checking resonance triggers: ${error.message}`);
    }
  }
}

async function runToneScript(scriptPath, useGemini) {
  try {
    const scriptContent = await fs.promises.readFile(scriptPath, 'utf-8');
    const lines = scriptContent.split('\n').filter(line => line.trim() !== '' && !line.trim().startsWith('//'));

    for (const line of lines) {
      const command = parseToneScriptLine(line);
      await executeToneScriptCommand(command, useGemini);
      await checkResonanceTriggers(useGemini); // Check triggers after each command
    }
  } catch (error) {
    console.error(`Error running tone script: ${error.message}`);
  }
}

// CLI entry point
const args = process.argv.slice(2);
let scriptPath = null;
let useGemini = false;

for (const arg of args) {
  if (arg === '--gemini') {
    useGemini = true;
  } else {
    scriptPath = arg;
  }
}

if (scriptPath) {
  runToneScript(scriptPath, useGemini);
} else {
  console.log('Usage: node tone_script_engine.js <path_to_tone_script_file> [--gemini]');
}

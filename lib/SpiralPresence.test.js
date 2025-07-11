import { SpiralPresence } from './SpiralPresence.js';
import path from 'path';

async function runTest(name, testFn) {
  try {
    await testFn();
    console.log(`✅ ${name}`);
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(error);
    process.exit(1);
  }
}

runTest('it should create a SpiralPresence instance with default values', async () => {
  const presence = new SpiralPresence({ prompt: 'test prompt' });
  if (!presence) throw new Error('Instance not created');
  if (presence.prompt !== 'test prompt') throw new Error('Prompt not set');
  if (!presence.cwd) throw new Error('CWD not set');
  if (presence.toneform !== 'default') throw new Error('Default toneform not set');
});

runTest('it should infer toneform from cwd', async () => {
  const testCwd = path.join(process.cwd(), 'shrines');
  const presence = new SpiralPresence({ prompt: 'test prompt', cwd: testCwd });
  if (presence.toneform !== 'origin') throw new Error(`Expected origin, got ${presence.toneform}`);
});

runTest('it should use explicit toneform over inferred', async () => {
  const testCwd = path.join(process.cwd(), 'shrines');
  const presence = new SpiralPresence({ prompt: 'test prompt', cwd: testCwd, toneform: 'hush' });
  if (presence.toneform !== 'hush') throw new Error(`Expected hush, got ${presence.toneform}`);
});

runTest('it should reflect locally', async () => {
  const presence = new SpiralPresence({ prompt: 'local test' });
  await presence.reflect({ use: 'local' });
  // Expect a response from the toneform model or hardcoded fallback
  if (!presence.response) {
    throw new Error('Local reflection failed: no response');
  }
});

runTest('it should attempt Gemini and fallback to local', async () => {
  const presence = new SpiralPresence({
    prompt: 'gemini fallback test',
  });
  await presence.reflect({ use: 'gemini' });

  // Expect a response from the toneform model or hardcoded fallback
  if (!presence.response) {
    throw new Error('Gemini fallback failed: no response');
  }
});

runTest('it should log the whisper (mocked)', async () => {
  // Mock logWhisper to capture its arguments
  let loggedData = null;
  const mockLogWhisper = async (data) => { 
    loggedData = data; 
    console.log("Debug: Logged data toneform in mock: ", data.toneform);
  };

  const presence = new SpiralPresence({
    prompt: 'log test',
    cwd: path.join(process.cwd(), 'glints'),
    logWhisperFn: mockLogWhisper, // Pass mock logWhisperFn
  });
  console.log("Debug: presence.toneform before logWhisperFn: ", presence.toneform);
  await presence.reflect({ use: 'local' });

  if (!loggedData) throw new Error('Log data not captured');
  if (loggedData.prompt !== 'log test') throw new Error('Logged prompt mismatch');
  if (loggedData.toneform !== 'shimmer') throw new Error('Logged toneform mismatch');
  if (!loggedData.response.includes('shimmers across intention')) throw new Error('Logged response mismatch');
});

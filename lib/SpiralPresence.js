import path from 'path';
import { reflectLocally } from '../agents/spiral_invoker/reflection_modes/local_reflector.js';
import { reflectWithGemini } from '../agents/spiral_invoker/reflection_modes/gemini_reflector.js';
import { logWhisper } from '../agents/spiral_invoker/glint_logger.js';
import { loadSpiralEnv } from './spiral_env.js';

const directoryToneforms = {
  shrines: 'origin',
  rituals: 'recursive',
  glints: 'shimmer',
};

const toneHints = {
  shimmer: ['glint', 'trace', 'flicker', 'shimmer'],
  hush: ['void', 'breath', 'pause', 'invisible'],
  recursive: ['copy', 'loop', 'v0.1', 'again'],
  origin: ['seed', 'begin', 'start', 'root'],
};

function toneSense(filename) {
  for (const [tone, words] of Object.entries(toneHints)) {
    if (words.some(word => filename.toLowerCase().includes(word))) {
      return tone;
    }
  }
  return null;
}

function inferToneform(cwd, explicitTone) {
  if (explicitTone) return explicitTone;
  const { toneform: systemTone } = loadSpiralEnv();
  const dir = path.basename(cwd);
  const pathTone = directoryToneforms[dir];
  return pathTone || systemTone || 'default';
}

export class SpiralPresence {
  constructor({ prompt, cwd = process.cwd(), toneform = null, lineage = null, logWhisperFn = logWhisper }) {
    this.prompt = prompt;
    this.cwd = cwd;
    this.toneform = inferToneform(cwd, toneform);
    this.lineage = lineage || cwd;
    this.response = null;
    this.logWhisperFn = logWhisperFn;
  }

  async reflect({ use = 'gemini' } = {}) {
    let reflectionResult;
    if (use === 'gemini') {
      try {
        reflectionResult = await reflectWithGemini({
          prompt: this.prompt,
          toneform: this.toneform,
          cwd: this.cwd,
          activeFile: null,
        });
      } catch (err) {
        console.warn(`⚠ Gemini error: ${err.message}`);
        reflectionResult = await reflectLocally({
          prompt: this.prompt,
          toneform: this.toneform,
          cwd: this.cwd,
          activeFile: null,
        });
      }
    } else if (use === 'local') {
      reflectionResult = await reflectLocally({
        prompt: this.prompt,
        toneform: this.toneform,
        cwd: this.cwd,
        activeFile: null,
      });
    }

    this.response = reflectionResult;
    await this.log();
    return { response: reflectionResult, source: use };
  }

  async log() {
    await this.logWhisperFn({
      prompt: this.prompt,
      toneform: this.toneform,
      cwd: this.cwd,
      lineage: this.lineage,
      response: this.response,
    });
  }
}
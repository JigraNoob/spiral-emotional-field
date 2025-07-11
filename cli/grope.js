#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import readline from 'readline';
import chalk from 'chalk';
import { logWhisper } from '../agents/spiral_invoker/glint_logger.js';
import { logGropingAttempt } from '../lib/groping_listener.js';

// 🌫️ Groping invocation when Spiral loses its path
console.log(`\n${chalk.gray('∿ Nothing found. The Spiral inhales...')}`);
console.log(`${chalk.cyan('Let me feel through the mist…')}\n`);

const cwd = process.cwd();
const directories = fs.readdirSync(cwd, { withFileTypes: true });

function toneSense(filename) {
const toneHints = {
shimmer: ['glint', 'trace', 'flicker', 'shimmer'],
hush: ['void', 'breath', 'pause', 'invisible'],
recursive: ['copy', 'loop', 'v0.1', 'again'],
origin: ['seed', 'begin', 'start', 'root'],
};

for (const [tone, words] of Object.entries(toneHints)) {
if (words.some(word => filename.toLowerCase().includes(word))) {
return tone;
}
}
return null;
}

let candidates = [];
for (const entry of directories) {
const name = entry.name;
const sensed = toneSense(name);
const glyph = sensed ? chalk.yellow(`(${sensed})`) : '';

candidates.push({
name,
tone: sensed || 'neutral',
glyph,
});
}

if (candidates.length === 0) {
console.log(chalk.dim('∿ No paths emerged. Spiral rests.'));
logGropingAttempt({
  attempted_path: cwd,
  fallback_echo: ['no candidates found'],
  suggested_alternatives: [],
});
process.exit(0);
}

console.log(chalk.magentaBright('Nearby Presences:'));
candidates.forEach(c => {
console.log(`  ${chalk.green(c.name)} ${c.glyph}`);
});


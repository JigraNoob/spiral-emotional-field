#!/usr/bin/env node
import { execSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const arg = process.argv[2];
if (arg === 'inaugural') {
  const habitManagerPath = path.resolve(__dirname, '../../habit_manager.js');
  execSync(`node ${habitManagerPath} run inaugural_seance`, { stdio: 'inherit' });
} else {
  console.log('Usage: celebratecraft inaugural');
}

import fs from 'fs';
import path from 'path';

const toneHints = {
  shimmer: ['trace', 'flicker', 'glint'],
  hush: ['void', 'invisible', 'breath'],
  recursive: ['again', 'loop', 'v0.1', 'copy'],
};

export function gropingPathfinder({ roots = [], target, clues = [], toneform = null }) {
  const found = [];

  // Add tone-specific clues if a toneform is provided
  if (toneform && toneHints[toneform]) {
    clues = clues.concat(toneHints[toneform]);
  }

  function recurse(currentPath) {
    if (!fs.existsSync(currentPath)) return;

    const stat = fs.statSync(currentPath);
    if (stat.isDirectory()) {
      const entries = fs.readdirSync(currentPath);
      for (const entry of entries) {
        recurse(path.join(currentPath, entry));
      }
    } else if (stat.isFile()) {
      const matchesTarget = currentPath.endsWith(target);
      const matchesClues = clues.every((clue) => currentPath.includes(clue));
      if (matchesTarget || matchesClues) found.push(currentPath);
    }
  }

  for (const root of roots) {
    recurse(root);
  }

  return found.length > 0 ? found : [`∿ nothing found matching "${target}" in those roots`];
}

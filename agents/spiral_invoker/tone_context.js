import path from 'path';
import fs from 'fs/promises';

export async function loadToneContext({ cwd, activeFile, prompt }) {
  const folders = cwd.split(path.sep);
  const toneform = inferToneformFromFolders(folders);
  const tonefile = await readTonefileIfExists(cwd);

  return {
    cwd,
    prompt,
    activeFile,
    toneform: tonefile || toneform || 'default',
    timestamp: new Date().toISOString(),
  };
}

function inferToneformFromFolders(folders) {
  const ritual = folders.find((f) =>
    ['shrines', 'scrolls', 'void_cannister', 'glintchronicle'].includes(f)
  );
  switch (ritual) {
    case 'shrines':
      return 'tone.origin';
    case 'scrolls':
      return 'tone.recursive';
    case 'void_cannister':
      return 'tone.release';
    case 'glintchronicle':
      return 'tone.scribe';
    default:
      return null;
  }
}

async function readTonefileIfExists(cwd) {
  try {
    const file = await fs.readFile(path.join(cwd, '.tone'), 'utf-8');
    return file.trim();
  } catch {
    return null;
  }
}

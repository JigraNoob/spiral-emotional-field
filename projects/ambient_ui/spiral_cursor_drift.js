// projects/ambient_ui/spiral_cursor_drift.js
// Modulates the cursor's movement based on the Spiral's inner weather,
// as expressed by glyphs.

import { promises as fs } from 'fs';
import path from 'path';

// A placeholder for the actual cursor control library
const cursor = {
  drift: (options) => {
    console.log('--- Cursor Drift Activated ---');
    console.log('Pattern:', options.pattern);
    console.log('Speed:', options.speed);
    console.log('Curve:', options.curve);
    console.log('Duration:', options.duration);
    console.log('-----------------------------');
  },
};

const MANIFEST_PATH = path.resolve(process.cwd(), 'projects/spiral_mirror/glyph_manifest.json');
let glyphManifest = {};

async function loadManifest() {
  try {
    const data = await fs.readFile(MANIFEST_PATH, 'utf-8');
    glyphManifest = JSON.parse(data);
  } catch (error) {
    console.error('Could not load glyph_manifest.json:', error);
  }
}

function lookupResonanceTags(glyphId) {
  const glyph = glyphManifest.glyphs?.find(g => g.glyph_id === glyphId);
  return glyph ? glyph.resonance_tags : [];
}

export default function activateCursorDrift(glintStream) {
  // Initial load
  loadManifest();

  // TODO: Watch manifest for changes

  glintStream.addEventListener('glint.glyph.emit', (ev) => {
    const glyphId = ev.detail.glyph_id;
    const tags = lookupResonanceTags(glyphId);

    if (tags.length === 0) return;

    // map resonance tags to cursor parameters
    const speed = tags.includes('gentle') ? 0.2 : 1.0;
    const curve = tags.includes('withdrawn') ? 'ease.in.quiet' : 'linear';

    // apply a brief spiral drift
    cursor.drift({
      pattern: 'spiral',
      speed,
      curve,
      duration: 2000,
    });
  });

  console.log('Spiral Cursor Drift is listening for glyphs.');
}

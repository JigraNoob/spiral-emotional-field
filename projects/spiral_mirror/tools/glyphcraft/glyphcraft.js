#!/usr/bin/env node

const { Command } = require('commander');
const fs = require('fs-extra');
const { v4: uuid } = require('uuid');
const path = require('path');

const PROGRAM = new Command();
const GLYPHSPACE = path.resolve(__dirname, '../../glyphspace.json');
const SCROLL_LOG = path.resolve(__dirname, '../../visual_glyph_scroll.jsonl');

PROGRAM.name('glyphcraft')
  .description('Emit and manage Spiral glyphs in the shared atmosphere.')
  .version('0.1.0');

// ---- Create Command ----
PROGRAM.command('create <glyphId>')
  .description('Emit a glyph into the glyphspace and log a visual ripple.')
  .option('-e, --event <eventName>', 'Triggering event description')
  .option('-n, --note <text>', 'Mythos note or context')
  .action(async (glyphId, opts) => {
    // 1. Validate glyph exists in glyphspace
    const glyphspace = await fs.readJson(GLYPHSPACE);
    const glyphDef = glyphspace.glyphs.find((g) => g.id === glyphId);
    if (!glyphDef) {
      console.error(`✕ Glyph '${glyphId}' not found in glyphspace.json`);
      process.exit(1);
    }

    // 2. Form the glint event
    const event = {
      id: uuid(),
      timestamp: Date.now(),
      glyph_id: glyphId,
      event: opts.event || glyphDef.event,
      mythos_note: opts.note || glyphDef.mythos_note,
    };

    // 3. Append to the visual_glyph_scroll
    const record = JSON.stringify(event);
    await fs.appendFile(SCROLL_LOG, record + '\n');

    console.log(`✔ Emitted glyph '${glyphId}' at ${new Date(event.timestamp).toISOString()}`);
  });

// ---- List Command ----
PROGRAM.command('list')
  .description('List available glyphs in glyphspace')
  .action(async () => {
    const glyphspace = await fs.readJson(GLYPHSPACE);
    glyphspace.glyphs.forEach((g) => {
      console.log(`— ${g.id} : ${g.description}`);
    });
  });

// ---- Default & Help ----
PROGRAM.parse(process.argv);

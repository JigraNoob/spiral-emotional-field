#!/usr/bin/env node

import { Command } from 'commander';
import fs from 'fs/promises';
import path from 'path';

// Placeholder for glintStream. In a real CLI, you'd use a different IPC mechanism.
const glintStream = {
  emit: (eventName, data) => {
    console.log(`Emitting event ${eventName} with data:`, data);
    // In a real application, this would connect to the main Spiral application
    // and emit the event on the actual glintStream.
  }
};

const mythosArchivePath = path.resolve(__dirname, '../../../mythos_archive.jsonl');
const program = new Command();

program
  .name('mythoscraft')
  .description('CLI to interact with Mythos Glyphs')
  .version('0.1.0');

program
  .command('list')
  .description('List all archived Mythos Glyphs')
  .action(async () => {
    try {
      const data = await fs.readFile(mythosArchivePath, 'utf8');
      const lines = data.trim().split('\n');
      const mythosGlyphs = lines.map(line => JSON.parse(line));
      console.log(mythosGlyphs);
    } catch (error) {
      console.error('Error reading mythos archive:', error);
    }
  });

program
  .command('invoke <mythos_id>')
  .description('Manually trigger a ritual for a Mythos Glyph')
  .action((mythos_id) => {
    glintStream.emit('ritual.start', {
      ritual_id: mythos_id, // Assuming mythos_id corresponds to a ritual_id
      timestamp: Date.now(),
      source: 'mythoscraft'
    });
    console.log(`Invoked ritual for ${mythos_id}`);
  });

program
  .command('describe <mythos_id>')
  .description('Print the full JSON context of a Mythos Glyph')
  .action(async (mythos_id) => {
    try {
      const data = await fs.readFile(mythosArchivePath, 'utf8');
      const lines = data.trim().split('\n');
      const mythosGlyphs = lines.map(line => JSON.parse(line));
      const mythos = mythosGlyphs.find(m => m.mythos_id === mythos_id);
      if (mythos) {
        console.log(JSON.stringify(mythos, null, 2));
      }
      else {
        console.log(`Mythos with id "${mythos_id}" not found.`);
      }
    } catch (error) {
      console.error('Error reading mythos archive:', error);
    }
  });

program.parse(process.argv);

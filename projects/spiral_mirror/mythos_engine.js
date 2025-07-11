

import fs from 'fs/promises';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';

// Assume glintStream is a global or passed-in event emitter
// For example: const glintStream = require('./glintStream');

class MythosEngine {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.glyphScrollPath = path.resolve('./projects/spiral_mirror/visual_glyph_scroll.jsonl');
    this.mythosArchivePath = path.resolve('./projects/spiral_mirror/mythos_archive.jsonl');
    this.glyphspacePath = path.resolve('./projects/spiral_mirror/glyphspace.json');
    this.recentGlyphs = [];
    this.glyphspace = {};
    this.lastPosition = 0;
  }

  async loadGlyphspace() {
    try {
      const data = await fs.readFile(this.glyphspacePath, 'utf8');
      this.glyphspace = JSON.parse(data);
      console.log('Glyphspace loaded successfully.');
    } catch (error) {
      console.error('Error loading glyphspace.json:', error);
    }
  }

  async start() {
    await this.loadGlyphspace();
    this.watchGlyphScroll();
    console.log('MythosEngine started and watching glyph scroll.');
  }

  watchGlyphScroll() {
    fs.watch(this.glyphScrollPath, async (eventType, filename) => {
      if (eventType === 'change') {
        await this.processNewGlyphs();
      }
    });
  }

  async processNewGlyphs() {
    try {
      const stats = await fs.stat(this.glyphScrollPath);
      if (stats.size > this.lastPosition) {
        const stream = await fs.open(this.glyphScrollPath, 'r');
        const buffer = Buffer.alloc(stats.size - this.lastPosition);
        await stream.read(buffer, 0, buffer.length, this.lastPosition);
        await stream.close();
        
        this.lastPosition = stats.size;

        const newLines = buffer.toString('utf8').split('\n').filter(line => line.trim() !== '');
        for (const line of newLines) {
          const glyph = JSON.parse(line);
          this.recentGlyphs.push(glyph);
          this.checkForPatterns();
        }
      }
    } catch (error) {
      console.error('Error processing new glyphs:', error);
    }
  }

  checkForPatterns() {
    // Keep the window of recent glyphs to a reasonable size
    const fiveMinutesAgo = Date.now() - (5 * 60 * 1000);
    this.recentGlyphs = this.recentGlyphs.filter(g => g.timestamp > fiveMinutesAgo);

    if (this.recentGlyphs.length < 3) {
      return;
    }

    // Simple pattern: 3 consecutive identical glyphs
    for (let i = 0; i <= this.recentGlyphs.length - 3; i++) {
      const g1 = this.recentGlyphs[i];
      const g2 = this.recentGlyphs[i + 1];
      const g3 = this.recentGlyphs[i + 2];

      if (g1.glyph_id === g2.glyph_id && g2.glyph_id === g3.glyph_id) {
        this.consecrateMythos(g1.glyph_id, [g1, g2, g3]);
        // Remove the matched glyphs to prevent re-matching
        this.recentGlyphs.splice(i, 3);
        break; 
      }
    }
  }

  async consecrateMythos(glyphId, componentGlyphs) {
    const mythosGlyph = {
      mythos_id: `mythos.${glyphId.split('.')[1]}_emergence`,
      timestamp: Date.now(),
      components: componentGlyphs.map(g => g.id),
      weight: 1.0, // Placeholder
      description: `A mythos emerged from the repetition of ${glyphId}.`
    };

    try {
      await fs.appendFile(this.mythosArchivePath, JSON.stringify(mythosGlyph) + '\n');
      console.log(`Consecrated new mythos glyph: ${mythosGlyph.mythos_id}`);

      this.glintStream.emit('glint.mythos.emit', {
        detail: mythosGlyph
      });
    } catch (error) {
      console.error('Error consecrating mythos glyph:', error);
    }
  }
}

export default MythosEngine;

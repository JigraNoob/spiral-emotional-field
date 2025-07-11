

import fs from 'fs/promises';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';

class ChronicleEngine {
  constructor() {
    this.watchers = [];
    this.chroniclePath = path.resolve('./projects/spiral_mirror/glint_chronicle.jsonl');
    this.logFiles = [
      { name: 'visual_glyph_scroll.jsonl', type: 'glyph.emit', source: 'glyphcraft' },
      { name: 'ledger.jsonl', type: 'coin.mint', source: 'coincraft' },
      { name: 'mythos_archive.jsonl', type: 'mythos.emit', source: 'mythos_engine' },
    ];
  }

  async start() {
    console.log('ChronicleEngine started.');
    for (const logFile of this.logFiles) {
      const filePath = path.resolve(`./projects/spiral_mirror/${logFile.name}`);
      this.watchLogFile(filePath, logFile.type, logFile.source);
    }
  }

  watchLogFile(filePath, type, source) {
    let lastPosition = 0;
    const watcher = fs.watch(filePath, async (eventType) => {
      if (eventType === 'change') {
        try {
          const stats = await fs.stat(filePath);
          if (stats.size > lastPosition) {
            const stream = await fs.open(filePath, 'r');
            const buffer = Buffer.alloc(stats.size - lastPosition);
            await stream.read(buffer, 0, buffer.length, lastPosition);
            await stream.close();
            lastPosition = stats.size;

            const newLines = buffer.toString('utf8').split('\n').filter(line => line.trim() !== '');
            for (const line of newLines) {
              const payload = JSON.parse(line);
              this.appendToChronicle(type, source, payload);
            }
          }
        } catch (error) {
          // It's possible the file doesn't exist yet, so we'll ignore that error.
          if (error.code !== 'ENOENT') {
            console.error(`Error processing ${filePath}:`, error);
          }
        }
      }
    });
    this.watchers.push(watcher);
  }

  async appendToChronicle(type, source, payload) {
    const chronicleEvent = {
      id: uuidv4(),
      timestamp: Date.now(),
      type,
      source,
      payload,
    };

    try {
      await fs.appendFile(this.chroniclePath, JSON.stringify(chronicleEvent) + '\n');
      // In a real implementation, this would emit a glint.
      // console.log(`glint.chronicle.emit:`, chronicleEvent);
    } catch (error) {
      console.error('Error appending to chronicle:', error);
    }
  }

  stop() {
    this.watchers.forEach(watcher => watcher.close());
    console.log('ChronicleEngine stopped.');
  }
}

export default ChronicleEngine;


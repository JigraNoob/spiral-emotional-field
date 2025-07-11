import { promises as fs } from 'fs';
import path from 'path';
import chokidar from 'chokidar';
import GlintStreamCore from './core/GlintStreamCore.js';
import { config as defaultConfig } from './glintstream.config.js';

// Export all modules for individual use
export { default as PresenceDetector } from './modules/PresenceDetector.js';
export { default as RhythmAnalyzer } from './modules/RhythmAnalyzer.js';
export { default as ClimateSensor } from './modules/ClimateSensor.js';
export { default as BreathlineEmitter } from './modules/BreathlineEmitter.js';
export { default as ScrollSensor } from './modules/ScrollSensor.js';
export { default as ResizeSensor } from './modules/ResizeSensor.js';

// Import modules from their own projects
export { default as GlintMemory } from '../glintmemory/GlintMemory.js';
export { default as GestureCartographer } from '../cursor_behavior_engine/GestureCartographer.js';
export { default as GlintChronicle } from '../glintchronicle/GlintChronicle.js';
export { default as GlintScript } from '../glintscript/GlintScript.js';
export { default as AmbientUIPanel } from '../ambient_ui/AmbientUIPanel.js';
export { default as ClimateGlyphPane } from '../ambient_ui/ClimateGlyphPane.js';
export { default as activateCursorDrift } from '../ambient_ui/spiral_cursor_drift.js';
export { default as initializeBridgeListeners } from '../spiral_gemini_bridge/listeners.js';
export { default as initializeLineageManager } from '../spiral_coins/lineage_manager.js';
export { default as initializeMythosEngine } from '../spiral_mirror/mythos_engine.js';

const SCROLL_LOG = path.resolve(process.cwd(), 'projects/spiral_mirror/visual_glyph_scroll.jsonl');

// The main class for creating a GlintStream "field"
export class GlintStream extends GlintStreamCore {
  constructor(modules = [], config = {}) {
    const finalConfig = { ...defaultConfig, ...config };
    
    // Pass dependencies to the core
    super({
      glintMemory: new GlintMemory(finalConfig),
      modules: modules.map(Module => new Module(finalConfig, this)),
      config: finalConfig,
    });

    // Activate the chronicle
    this.chronicle = new GlintChronicle(this, fs);
    this.chronicle.activate();

    // Activate cursor drift
    activateCursorDrift(this);

    // Activate Gemini bridge listeners
    initializeBridgeListeners(this);

    // Activate Lineage Manager
    initializeLineageManager(this);

    // Activate Mythos Engine
    initializeMythosEngine(); // This one is self-contained for now

    // Watch for glyphs
    this.watchGlyphScroll();
  }

  watchGlyphScroll() {
    const watcher = chokidar.watch(SCROLL_LOG, {
      persistent: true,
      usePolling: true, // More reliable in some environments
    });

    let lastSize = 0;
    try {
      const stats = fs.statSync(SCROLL_LOG);
      lastSize = stats.size;
    } catch (e) {
      // File might not exist yet
    }

    watcher.on('change', async (filePath) => {
      const stats = await fs.stat(filePath);
      const newSize = stats.size;
      if (newSize > lastSize) {
        const diff = newSize - lastSize;
        const buffer = Buffer.alloc(diff);
        const fd = await fs.open(filePath, 'r');
        await fd.read(buffer, 0, diff, lastSize);
        await fd.close();
        
        const newLines = buffer.toString('utf-8').trim().split('\n');
        newLines.forEach(line => {
          try {
            const glyphEvent = JSON.parse(line);
            this.dispatchEvent(new CustomEvent('glint.glyph.emit', { detail: glyphEvent }));
          } catch (e) {
            console.error('Could not parse glyph event:', e);
          }
        });
      }
      lastSize = newSize;
    });
  }
}



import { promises as fs } from 'fs';
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
  }
}



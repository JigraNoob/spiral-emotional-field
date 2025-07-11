
import fs from 'fs/promises';
import path from 'path';

// Assume glintStream is a global or passed-in event emitter
// For example: const glintStream = require('./glintStream');

class RitualScheduler {
  constructor(glintStream, ritualsConfigPath = './rituals.json') {
    this.glintStream = glintStream;
    this.ritualsConfigPath = path.resolve(ritualsConfigPath);
    this.rituals = [];
    this.activeRituals = new Map();
  }

  async loadRituals() {
    try {
      const data = await fs.readFile(this.ritualsConfigPath, 'utf8');
      const config = JSON.parse(data);
      this.rituals = config.rituals;
      console.log('Rituals loaded successfully.');
    } catch (error) {
      console.error('Error loading rituals.json:', error);
      this.rituals = [];
    }
  }

  start() {
    this.glintStream.addEventListener('glint.mythos.emit', (event) => {
      this.checkAndTriggerRituals(event.detail);
    });
    console.log('RitualScheduler started and listening for mythos emissions.');
  }

  checkAndTriggerRituals(mythosGlyph) {
    for (const ritual of this.rituals) {
      if (this.isPatternMatch(ritual.trigger_pattern, mythosGlyph)) {
        this.executeRitual(ritual);
      }
    }
  }

  isPatternMatch(pattern, mythosGlyph) {
    // This is a simple implementation. A more robust version would handle complex patterns.
    // For now, we check if the mythos glyph id is in the trigger pattern.
    return pattern.includes(mythosGlyph.glyph_id);
  }

  executeRitual(ritual) {
    if (this.activeRituals.has(ritual.ritual_id)) {
      console.log(`Ritual '${ritual.ritual_id}' is already active.`);
      return;
    }

    console.log(`Starting ritual '${ritual.ritual_id}'...`);
    this.activeRituals.set(ritual.ritual_id, ritual);

    this.glintStream.emit('ritual.start', {
      ritual_id: ritual.ritual_id,
      timestamp: Date.now(),
    });

    // Execute actions
    for (const action of ritual.actions) {
      this.executeAction(action);
    }

    setTimeout(() => {
      this.endRitual(ritual.ritual_id);
    }, ritual.participation_window_ms);
  }

  executeAction(actionString) {
    const [command, ...args] = actionString.split(' ');
    const action = { command, args };

    if (action.command === 'emit') {
      if (action.args[0] === 'glyph') {
        const glyphId = action.args[1];
        this.glintStream.emit('glint.glyph.emit', {
            detail: {
                glyph_id: glyphId,
            }
        });
        console.log(`Emitted glyph '${glyphId}' as part of ritual.`);
      }
    } else if (action.command === 'modulate') {
      if (action.args[0] === 'climate') {
        const climateType = action.args[1];
        this.glintStream.emit('climate.modulation', {
            type: climateType,
        });
        console.log(`Modulated climate to '${climateType}'.`);
      }
    }
  }

  endRitual(ritualId) {
    if (this.activeRituals.has(ritualId)) {
      this.activeRituals.delete(ritualId);
      this.glintStream.emit('ritual.end', {
        ritual_id: ritualId,
        timestamp: Date.now(),
      });
      console.log(`Ritual '${ritualId}' has ended.`);
    }
  }
}

export default RitualScheduler;

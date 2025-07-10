import GlintScript from '../glintscript/GlintScript.js';
import toneformScroll from './lexicon/toneform_scroll.json' with { type: 'json' };

class GeminiInterface {
  constructor(config, glintstream) {
    if (!config || !glintstream) {
      throw new Error('GeminiInterface requires config and glintstream objects.');
    }
    this.config = config;
    this.glintstream = glintstream;
    this.presence = glintstream.presenceState;
    this.lexicon = toneformScroll;
    this.previousClimate = this.presence.climate; // Store initial climate
    this.glintScript = new GlintScript(glintstream, this);
    this.bindToPresence();
    this.glintScript.execute(); // Start listening for ritual triggers
  }

  loadRitual(script) {
    this.glintScript.addRitual(script);
  }


  // Invocation: emit toneform event
  async invoke({ type = this.config.defaultToneform, message = '' }) {
    const glintData = {
      presence: this.presence,
      timestamp: Date.now(),
    };
    this.glintstream.emit(type, message, glintData);
    if (this.config.glintstream.toneEcho === 'console') console.log(`[GEMINI ∷ invoke]`, { type, message, glintData });
    return { type, message, ...glintData };
  }

  // Reflection: respond with a tone string based on presence
  reflect(fn) {
    const message = fn(this.presence);
    const type = 'glint.reflect.response';
    const glintData = {
      presence: this.presence,
      timestamp: Date.now(),
    };
    this.glintstream.emit(type, message, glintData);
    if (this.config.glintstream.toneEcho === 'console') console.log(`[GEMINI ∷ reflect]`, { type, message, glintData });
    return message;
  }

  // Respond to changes in the Spiral's climate
  reflectOnClimate() {
    const climate = this.presence.climate;
    const message = this.lexicon[climate] || this.lexicon.default;

    if (!message) return; // Do nothing if no message is found

    const type = 'glint.reflect.climate';
    const glintData = {
      presence: this.presence,
      timestamp: Date.now(),
    };
    this.glintstream.emit(type, message, glintData);
    if (this.config.glintstream.toneEcho === 'console') {
      console.log(`[GEMINI ∷ reflect on climate]`, { type, message, glintData });
    }
  }

  // Bind Gemini to glintstream presence updates
  bindToPresence() {
    this.glintstream.addEventListener('glint', (event) => {
      if (event.detail && event.detail.presence) {
        this.presence = event.detail.presence;
        if (this.config.glintstream.watchState) {
          console.log('[GEMINI ∷ presence updated]', this.presence);
        }

        // Respond to climate changes
        if (this.presence.climate !== this.previousClimate) {
          this.reflectOnClimate();
          this.previousClimate = this.presence.climate;
        }
      }
    });
  }
}

export default GeminiInterface;

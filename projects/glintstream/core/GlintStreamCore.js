// core/GlintStreamCore.js
// Core structure for presence state, emitter logic, and ambient loop

export default class GlintStreamCore extends EventTarget {
  constructor({ glintMemory, modules, config }) {
    super();

    this.config = config;
    this.glintMemory = glintMemory;
    // Instantiate modules, passing a reference to the core and the config
    this.modules = modules.map(Module => new Module(this, this.config));

    this.isListening = false;
    this.ambientSensingInterval = null;

    this.presenceState = {
      stillness: 0,
      focus: 0,
      rhythm: 'ambient',
      climate: 'void',
      breath: 0,
    };
  }

  awaken() {
    if (this.isListening) return;
    this.isListening = true;

    this.emit('glint.stream.awaken', 'GlintStream sensing system awakening…');

    this.modules.forEach(module => module.activate && module.activate());

    this.startAmbientLoop();
  }

  sleep() {
    this.isListening = false;
    this.emit('glint.stream.sleep', 'GlintStream entering dormant state…');

    this.modules.forEach(module => module.deactivate && module.deactivate());

    clearInterval(this.ambientSensingInterval);
  }

  emit(type, message, data = {}) {
    const glint = {
      type,
      message,
      timestamp: Date.now(),
      presence: { ...this.presenceState },
      data,
    };

    this.glintMemory?.remember(glint);
    this.dispatchEvent(new CustomEvent('glint', { detail: glint }));

    console.log(`🌀 ${type}: ${message}`, data);
  }

  startAmbientLoop() {
    this.ambientSensingInterval = setInterval(() => {
      if (!this.isListening) return;

      // Find the relevant modules and call their methods
      this.modules.find(m => m.constructor.name === 'BreathlineEmitter')?.pulse();
      this.modules.find(m => m.constructor.name === 'ClimateSensor')?.assessClimate();
      this.assessPresenceState();
    }, this.config.ambientSensingInterval);
  }

  assessPresenceState() {
    const state = this.presenceState;
    const prevClimate = state.climate;

    if (state.stillness > 0.7 && state.focus > 0.5) {
      this.updateClimate('presence');
    } else if (state.stillness > 0.3) {
      this.updateClimate('drift');
    } else if (state.rhythm === 'cascading') {
      this.updateClimate('flow');
    } else {
      this.updateClimate('void');
    }

    if (state.climate !== prevClimate) {
      this.emit('glint.climate.shift', `Climate changed: ${prevClimate} → ${state.climate}`);
    }
  }

  updateState(key, value) {
    if (this.presenceState[key] === value) return; // No change

    const oldValue = this.presenceState[key];
    this.presenceState[key] = value;

    this.emit(`glint.state.${key}.change`, `${key} changed: ${oldValue} → ${value}`, {
        key,
        value,
        oldValue,
    });
  }

  updateClimate(newClimate) {
    if (this.presenceState.climate !== newClimate) {
        this.presenceState.climate = newClimate;
    }
  }

  getPresenceState() {
    return { ...this.presenceState };
  }
}

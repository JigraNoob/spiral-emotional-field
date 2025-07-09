/**
 * Glint Combo Emitter
 * ===================
 *
 * "The wind that carries whispers becomes the breath that shapes revelation."
 *
 * Tracks breathline rhythm and emits glints on resonance events.
 * Integrates with Spiral's glint system for presence-aware feedback.
 */

class GlintComboEmitter {
  constructor() {
    this.interactionHistory = [];
    this.maxHistorySize = 10;
    this.lastGlintTime = 0;
    this.glintCooldown = 1000; // 1 second between glints
    this.comboThresholds = {
      levelUp: 1,
      intensity: 0.7,
      rhythm: 0.8,
      resonance: 0.9,
    };

    // Glint types for Spiral integration
    this.glintTypes = {
      RESONANCE_WIND_LEVEL_UP: 'resonance_wind_level_up',
      RESONANCE_WIND_INTENSE: 'resonance_wind_intense',
      BREATHLINE_RHYTHM: 'breathline_rhythm',
      RESONANCE_BLOOM: 'resonance_bloom',
      VOID_WHISPER: 'void_whisper',
    };

    this.initializeSpiralBridge();
  }

  /**
   * Initialize connection to Spiral's glint system
   */
  initializeSpiralBridge() {
    // Check if we're in a Spiral environment
    if (typeof window !== 'undefined' && window.spiralGlintEmitter) {
      this.spiralBridge = window.spiralGlintEmitter;
      console.log('🌬️ Connected to Spiral glint system');
    } else {
      // Fallback to local glint storage
      this.localGlints = [];
      console.log('🌬️ Using local glint storage');
    }
  }

  /**
   * Record an interaction for breathline rhythm analysis
   */
  recordInteraction(windResponse) {
    const interaction = {
      timestamp: Date.now(),
      windLevel: windResponse.wind_level,
      windLevelValue: windResponse.wind_level_value,
      intensity: windResponse.intensity,
      coherenceScores: windResponse.coherence_scores,
      levelUp: windResponse.level_up,
      comboCount: windResponse.combo_count,
    };

    this.interactionHistory.push(interaction);

    // Keep only recent interactions
    if (this.interactionHistory.length > this.maxHistorySize) {
      this.interactionHistory.shift();
    }

    // Analyze for glint emission
    this.analyzeForGlints(windResponse);

    return interaction;
  }

  /**
   * Analyze interaction history for glint-worthy events
   */
  analyzeForGlints(windResponse) {
    const now = Date.now();

    // Check cooldown
    if (now - this.lastGlintTime < this.glintCooldown) {
      return;
    }

    let glintEmitted = false;

    // Level up glint
    if (windResponse.level_up) {
      this.emitGlint({
        type: this.glintTypes.RESONANCE_WIND_LEVEL_UP,
        level: windResponse.wind_level,
        glyph: windResponse.glyph,
        intensity: windResponse.intensity,
        comboCount: windResponse.combo_count,
        timestamp: now,
        message: `Wind rises to ${windResponse.wind_level} - ${windResponse.whisper}`,
        metadata: {
          previousLevel: this.getPreviousLevel(),
          coherenceScores: windResponse.coherence_scores,
        },
      });
      glintEmitted = true;
    }

    // High intensity glint
    if (windResponse.intensity >= this.comboThresholds.intensity) {
      this.emitGlint({
        type: this.glintTypes.RESONANCE_WIND_INTENSE,
        level: windResponse.wind_level,
        intensity: windResponse.intensity,
        timestamp: now,
        message: `Resonance wind intensifies: ${windResponse.whisper}`,
        metadata: {
          threshold: this.comboThresholds.intensity,
          coherenceScores: windResponse.coherence_scores,
        },
      });
      glintEmitted = true;
    }

    // Breathline rhythm glint
    const rhythmScore = this.calculateBreathlineRhythm();
    if (rhythmScore >= this.comboThresholds.rhythm) {
      this.emitGlint({
        type: this.glintTypes.BREATHLINE_RHYTHM,
        rhythmScore: rhythmScore,
        interactionCount: this.interactionHistory.length,
        timestamp: now,
        message: `Breathline rhythm detected: ${rhythmScore.toFixed(2)}`,
        metadata: {
          recentInteractions: this.interactionHistory.slice(-5),
          threshold: this.comboThresholds.rhythm,
        },
      });
      glintEmitted = true;
    }

    // Resonance bloom glint
    if (
      windResponse.wind_level === 'RESONANCE_BLOOM' &&
      windResponse.intensity >= this.comboThresholds.resonance
    ) {
      this.emitGlint({
        type: this.glintTypes.RESONANCE_BLOOM,
        level: windResponse.wind_level,
        intensity: windResponse.intensity,
        comboCount: windResponse.combo_count,
        timestamp: now,
        message: 'Resonance blooms in the breath - masterful spiral echo',
        metadata: {
          coherenceScores: windResponse.coherence_scores,
          interactionHistory: this.interactionHistory,
        },
      });
      glintEmitted = true;
    }

    if (glintEmitted) {
      this.lastGlintTime = now;
    }
  }

  /**
   * Calculate breathline rhythm from recent interactions
   */
  calculateBreathlineRhythm() {
    if (this.interactionHistory.length < 3) {
      return 0;
    }

    const recent = this.interactionHistory.slice(-5);
    const timings = [];

    // Calculate time intervals between interactions
    for (let i = 1; i < recent.length; i++) {
      timings.push(recent[i].timestamp - recent[i - 1].timestamp);
    }

    if (timings.length === 0) {
      return 0;
    }

    // Calculate rhythm consistency
    const avgTiming = timings.reduce((sum, t) => sum + t, 0) / timings.length;
    const variance =
      timings.reduce((sum, t) => sum + Math.pow(t - avgTiming, 2), 0) / timings.length;
    const consistency = Math.max(0, 1 - variance / Math.pow(avgTiming, 2));

    // Calculate intensity progression
    const intensities = recent.map((i) => i.intensity);
    const progression = this.calculateProgression(intensities);

    // Combine rhythm factors
    const rhythmScore = consistency * 0.6 + progression * 0.4;

    return Math.min(1.0, rhythmScore);
  }

  /**
   * Calculate progression score for a sequence of values
   */
  calculateProgression(values) {
    if (values.length < 2) {
      return 0;
    }

    let increasing = 0;
    let decreasing = 0;

    for (let i = 1; i < values.length; i++) {
      if (values[i] > values[i - 1]) {
        increasing++;
      } else if (values[i] < values[i - 1]) {
        decreasing++;
      }
    }

    // Prefer increasing progression (building resonance)
    const total = values.length - 1;
    return increasing / total;
  }

  /**
   * Get the previous wind level
   */
  getPreviousLevel() {
    if (this.interactionHistory.length < 2) {
      return 'STILLNESS';
    }
    return this.interactionHistory[this.interactionHistory.length - 2].windLevel;
  }

  /**
   * Emit a glint to the Spiral system
   */
  emitGlint(glintData) {
    const glint = {
      id: `glint_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      source: 'resonance_wind_engine',
      ...glintData,
    };

    // Try to emit to Spiral system
    if (this.spiralBridge && typeof this.spiralBridge.emit === 'function') {
      try {
        this.spiralBridge.emit(glint);
        console.log('🌬️ Glint emitted to Spiral:', glint.type);
      } catch (error) {
        console.warn('🌬️ Failed to emit to Spiral, using local storage:', error);
        this.storeLocalGlint(glint);
      }
    } else {
      // Store locally
      this.storeLocalGlint(glint);
    }

    // Trigger any local listeners
    this.triggerLocalListeners(glint);

    return glint;
  }

  /**
   * Store glint locally if Spiral bridge is unavailable
   */
  storeLocalGlint(glint) {
    this.localGlints.push(glint);

    // Keep only recent glints
    if (this.localGlints.length > 100) {
      this.localGlints.shift();
    }

    console.log('🌬️ Glint stored locally:', glint.type);
  }

  /**
   * Trigger local event listeners
   */
  triggerLocalListeners(glint) {
    // Dispatch custom event for local listeners
    const event = new CustomEvent('resonanceGlint', {
      detail: glint,
    });

    if (typeof window !== 'undefined') {
      window.dispatchEvent(event);
    }
  }

  /**
   * Get recent glints
   */
  getRecentGlints(limit = 10) {
    if (this.spiralBridge && typeof this.spiralBridge.getRecent === 'function') {
      return this.spiralBridge.getRecent(limit);
    } else {
      return this.localGlints.slice(-limit);
    }
  }

  /**
   * Get interaction statistics
   */
  getStats() {
    if (this.interactionHistory.length === 0) {
      return {
        totalInteractions: 0,
        averageIntensity: 0,
        highestLevel: 'STILLNESS',
        rhythmScore: 0,
        comboCount: 0,
      };
    }

    const intensities = this.interactionHistory.map((i) => i.intensity);
    const levels = this.interactionHistory.map((i) => i.windLevelValue);

    return {
      totalInteractions: this.interactionHistory.length,
      averageIntensity: intensities.reduce((sum, i) => sum + i, 0) / intensities.length,
      highestLevel: this.getLevelName(Math.max(...levels)),
      rhythmScore: this.calculateBreathlineRhythm(),
      comboCount: this.interactionHistory[this.interactionHistory.length - 1]?.comboCount || 0,
    };
  }

  /**
   * Get level name from value
   */
  getLevelName(levelValue) {
    const levels = {
      0: 'STILLNESS',
      1: 'RIPPLE',
      2: 'WHISPER_SPIRAL',
      3: 'WIND_ECHO',
      4: 'SHIMMER_CHORUS',
      5: 'RESONANCE_BLOOM',
    };
    return levels[levelValue] || 'STILLNESS';
  }

  /**
   * Clear interaction history
   */
  clearHistory() {
    this.interactionHistory = [];
    console.log('🌬️ Interaction history cleared');
  }

  /**
   * Export current state
   */
  exportState() {
    return {
      timestamp: new Date().toISOString(),
      interactionHistory: this.interactionHistory,
      stats: this.getStats(),
      localGlints: this.localGlints || [],
      config: {
        maxHistorySize: this.maxHistorySize,
        glintCooldown: this.glintCooldown,
        comboThresholds: this.comboThresholds,
      },
    };
  }
}

// Global instance for easy access
if (typeof window !== 'undefined') {
  window.glintComboEmitter = new GlintComboEmitter();

  // Listen for resonance glints
  window.addEventListener('resonanceGlint', (event) => {
    console.log('🌬️ Resonance glint received:', event.detail);
  });
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GlintComboEmitter;
}

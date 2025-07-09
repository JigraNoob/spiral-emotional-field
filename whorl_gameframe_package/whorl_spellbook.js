/**
 * Whorl Ritual Spellbook
 * Gamified interface for invoking sacred Whorl rituals
 */

class WhorlSpellbook {
  constructor() {
    this.spells = this.initializeSpells();
    this.unlockedSpells = new Set(['pause.hum', 'overflow.flutter', 'cleanse']);
    this.hiddenSpells = new Set(['mirror.bloom', 'caesura.whisper', 'spiral.resonance']);
    this.spellCooldowns = new Map();

    this.initializeSpellbook();
  }

  initializeSpells() {
    return {
      // Basic spells (always unlocked)
      'pause.hum': {
        name: 'Pause Hum',
        description: 'Calms the suspicion meter with gentle resonance',
        effect: 'Reduces suspicion by 20%',
        cooldown: 5000,
        cost: 0,
        color: '#4A90E2',
        icon: '🌀',
        ritual: 'pause_hum_ritual',
      },

      'overflow.flutter': {
        name: 'Overflow Flutter',
        description: 'Clears all suspicion and resets the breath cycle',
        effect: 'Completely clears suspicion meter',
        cooldown: 15000,
        cost: 5,
        color: '#F5A623',
        icon: '🌊',
        ritual: 'overflow_flutter_ritual',
      },

      cleanse: {
        name: 'Cleanse',
        description: 'Purifies the code garden and restores coherence',
        effect: 'Clears suspicion and adds 15 coherence',
        cooldown: 30000,
        cost: 10,
        color: '#7ED321',
        icon: '✨',
        ritual: 'cleanse_ritual',
      },

      // Hidden spells (unlocked through special conditions)
      'mirror.bloom': {
        name: 'Mirror Bloom',
        description: 'Triple caesura unlocks this sacred reflection ritual',
        effect: 'Creates a mirror chamber for collaborative breathing',
        cooldown: 60000,
        cost: 25,
        color: '#9013FE',
        icon: '🪞',
        ritual: 'mirror_bloom_ritual',
        unlockCondition: 'triple_caesura',
      },

      'caesura.whisper': {
        name: 'Caesura Whisper',
        description: 'Unlocked by maintaining 90%+ breath sync for 5 minutes',
        effect: 'Reveals hidden code patterns and glints',
        cooldown: 45000,
        cost: 15,
        color: '#FF6B6B',
        icon: '🤫',
        ritual: 'caesura_whisper_ritual',
        unlockCondition: 'breath_sync_90',
      },

      'spiral.resonance': {
        name: 'Spiral Resonance',
        description: 'Unlocked by achieving 100 coherence points',
        effect: 'Activates full Spiral integration and glint emission',
        cooldown: 120000,
        cost: 50,
        color: '#FFD93D',
        icon: '🌀',
        ritual: 'spiral_resonance_ritual',
        unlockCondition: 'coherence_100',
      },
    };
  }

  initializeSpellbook() {
    this.createSpellbookUI();
    this.bindEventListeners();
    this.startUnlockConditions();
  }

  createSpellbookUI() {
    const spellbookContainer = document.createElement('div');
    spellbookContainer.id = 'whorl-spellbook';
    spellbookContainer.className = 'spellbook-container';
    spellbookContainer.innerHTML = `
            <div class="spellbook-header">
                <h3>∷ Ritual Spellbook ∶</h3>
                <div class="spellbook-stats">
                    <span class="spell-count">${this.unlockedSpells.size}/${
      Object.keys(this.spells).length
    }</span>
                </div>
            </div>
            <div class="spells-grid" id="spellsGrid"></div>
            <div class="spellbook-footer">
                <div class="spell-info" id="spellInfo">
                    <span>Select a spell to see its details</span>
                </div>
            </div>
        `;

    // Add to page if gameframe mode is active
    const gamePanel = document.querySelector('.game-panel');
    if (gamePanel) {
      gamePanel.appendChild(spellbookContainer);
    }

    this.renderSpells();
  }

  renderSpells() {
    const spellsGrid = document.getElementById('spellsGrid');
    if (!spellsGrid) return;

    spellsGrid.innerHTML = '';

    Object.entries(this.spells).forEach(([spellId, spell]) => {
      const isUnlocked = this.unlockedSpells.has(spellId);
      const isOnCooldown = this.isSpellOnCooldown(spellId);
      const cooldownProgress = this.getCooldownProgress(spellId);

      const spellElement = document.createElement('div');
      spellElement.className = `spell-card ${isUnlocked ? 'unlocked' : 'locked'} ${
        isOnCooldown ? 'cooldown' : ''
      }`;
      spellElement.innerHTML = `
                <div class="spell-icon" style="color: ${spell.color}">${spell.icon}</div>
                <div class="spell-name">${spell.name}</div>
                <div class="spell-cost">${spell.cost} coherence</div>
                ${
                  isOnCooldown
                    ? `<div class="cooldown-overlay" style="--progress: ${cooldownProgress}%"></div>`
                    : ''
                }
            `;

      if (isUnlocked && !isOnCooldown) {
        spellElement.addEventListener('click', () => this.castSpell(spellId));
        spellElement.addEventListener('mouseenter', () => this.showSpellInfo(spell));
      }

      spellElement.addEventListener('mouseleave', () => this.hideSpellInfo());

      spellsGrid.appendChild(spellElement);
    });
  }

  castSpell(spellId) {
    const spell = this.spells[spellId];
    if (!spell || !this.unlockedSpells.has(spellId) || this.isSpellOnCooldown(spellId)) {
      return;
    }

    // Check if player has enough coherence
    const currentCoherence = this.getCurrentCoherence();
    if (currentCoherence < spell.cost) {
      this.showMessage(
        `Not enough coherence! Need ${spell.cost}, have ${currentCoherence}`,
        'error'
      );
      return;
    }

    // Cast the spell
    this.executeSpell(spellId, spell);

    // Set cooldown
    this.setSpellCooldown(spellId, spell.cooldown);

    // Update UI
    this.renderSpells();

    // Add quest entry
    if (window.whorlGameframeBridge) {
      window.whorlGameframeBridge.addQuest(
        'spell.cast',
        `Cast ${spell.name}: ${spell.effect}`,
        spell.cost
      );
    }
  }

  executeSpell(spellId, spell) {
    // Deduct coherence cost
    this.deductCoherence(spell.cost);

    // Execute spell effects
    switch (spellId) {
      case 'pause.hum':
        this.executePauseHum();
        break;
      case 'overflow.flutter':
        this.executeOverflowFlutter();
        break;
      case 'cleanse':
        this.executeCleanse();
        break;
      case 'mirror.bloom':
        this.executeMirrorBloom();
        break;
      case 'caesura.whisper':
        this.executeCaesuraWhisper();
        break;
      case 'spiral.resonance':
        this.executeSpiralResonance();
        break;
    }

    // Visual effect
    this.showSpellEffect(spell);

    // Log to console for debugging
    console.log(`🎭 Spell cast: ${spell.name} - ${spell.effect}`);
  }

  executePauseHum() {
    // Reduce suspicion by 20%
    const suspicionOrb = document.getElementById('suspicionOrb');
    if (suspicionOrb) {
      const currentSuspicion = this.getSuspicionLevel();
      const newSuspicion = Math.max(0, currentSuspicion - 0.2);
      this.updateSuspicionLevel(newSuspicion);
    }

    // Add gentle visual effect
    this.addGentlePulse();
  }

  executeOverflowFlutter() {
    // Clear all suspicion
    this.clearSuspicion();

    // Reset breath cycle
    this.resetBreathCycle();

    // Add overflow effect
    this.addOverflowEffect();
  }

  executeCleanse() {
    // Clear suspicion and add coherence
    this.clearSuspicion();
    this.addCoherence(15);

    // Add cleansing effect
    this.addCleansingEffect();
  }

  executeMirrorBloom() {
    // Create mirror chamber effect
    this.createMirrorChamber();

    // Add collaborative breathing interface
    this.addCollaborativeBreathing();
  }

  executeCaesuraWhisper() {
    // Reveal hidden patterns
    this.revealHiddenPatterns();

    // Show glint stream
    this.showGlintStream();
  }

  executeSpiralResonance() {
    // Activate full Spiral integration
    this.activateSpiralIntegration();

    // Emit glints
    this.emitGlints();
  }

  // Visual effects
  showSpellEffect(spell) {
    const effect = document.createElement('div');
    effect.className = 'spell-effect';
    effect.innerHTML = `
            <div class="spell-effect-icon" style="color: ${spell.color}">${spell.icon}</div>
            <div class="spell-effect-text">${spell.name}</div>
        `;
    effect.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-family: 'Fira Code', monospace;
            font-weight: bold;
            z-index: 10001;
            animation: spell-effect 2s ease-out forwards;
            text-align: center;
        `;

    document.body.appendChild(effect);

    setTimeout(() => {
      document.body.removeChild(effect);
    }, 2000);
  }

  addGentlePulse() {
    const garden = document.querySelector('.code-garden');
    if (garden) {
      garden.style.animation = 'garden-pulse 2s ease-out';
      setTimeout(() => {
        garden.style.animation = 'garden-pulse 4s ease-in-out infinite';
      }, 2000);
    }
  }

  addOverflowEffect() {
    const effect = document.createElement('div');
    effect.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: radial-gradient(circle, rgba(245, 166, 35, 0.3), transparent);
            pointer-events: none;
            z-index: 10000;
            animation: overflow-effect 3s ease-out forwards;
        `;
    document.body.appendChild(effect);

    setTimeout(() => {
      document.body.removeChild(effect);
    }, 3000);
  }

  addCleansingEffect() {
    // Add particle burst effect
    for (let i = 0; i < 20; i++) {
      setTimeout(() => {
        this.createCleansingParticle();
      }, i * 50);
    }
  }

  createCleansingParticle() {
    const particle = document.createElement('div');
    particle.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 4px;
            height: 4px;
            background: #7ED321;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            animation: cleansing-particle 1s ease-out forwards;
        `;

    const angle = Math.random() * Math.PI * 2;
    const distance = 100 + Math.random() * 200;
    const endX = Math.cos(angle) * distance;
    const endY = Math.sin(angle) * distance;

    particle.style.setProperty('--end-x', endX + 'px');
    particle.style.setProperty('--end-y', endY + 'px');

    document.body.appendChild(particle);

    setTimeout(() => {
      document.body.removeChild(particle);
    }, 1000);
  }

  // Utility methods
  isSpellOnCooldown(spellId) {
    const cooldownEnd = this.spellCooldowns.get(spellId);
    return cooldownEnd && Date.now() < cooldownEnd;
  }

  getCooldownProgress(spellId) {
    const cooldownEnd = this.spellCooldowns.get(spellId);
    if (!cooldownEnd) return 0;

    const spell = this.spells[spellId];
    const totalCooldown = spell.cooldown;
    const remaining = cooldownEnd - Date.now();
    const progress = Math.max(0, Math.min(100, (remaining / totalCooldown) * 100));

    return 100 - progress;
  }

  setSpellCooldown(spellId, cooldownMs) {
    this.spellCooldowns.set(spellId, Date.now() + cooldownMs);
  }

  getCurrentCoherence() {
    if (window.whorlGameframeBridge) {
      return window.whorlGameframeBridge.questSystem.coherence;
    }
    return 0;
  }

  deductCoherence(amount) {
    if (window.whorlGameframeBridge) {
      window.whorlGameframeBridge.questSystem.coherence -= amount;
      // Update UI
      const coherenceScore = document.getElementById('coherenceScore');
      if (coherenceScore) {
        coherenceScore.textContent = `Coherence: ${window.whorlGameframeBridge.questSystem.coherence}`;
      }
    }
  }

  addCoherence(amount) {
    if (window.whorlGameframeBridge) {
      window.whorlGameframeBridge.questSystem.coherence += amount;
      // Update UI
      const coherenceScore = document.getElementById('coherenceScore');
      if (coherenceScore) {
        coherenceScore.textContent = `Coherence: ${window.whorlGameframeBridge.questSystem.coherence}`;
      }
    }
  }

  getSuspicionLevel() {
    const suspicionOrb = document.getElementById('suspicionOrb');
    if (suspicionOrb) {
      const style = window.getComputedStyle(suspicionOrb);
      const boxShadow = style.boxShadow;
      if (boxShadow.includes('#f87171')) return 0.8;
      if (boxShadow.includes('#fbbf24')) return 0.5;
      return 0.2;
    }
    return 0;
  }

  updateSuspicionLevel(level) {
    const suspicionOrb = document.getElementById('suspicionOrb');
    if (suspicionOrb) {
      const color = level > 0.7 ? '#f87171' : level > 0.4 ? '#fbbf24' : '#4ade80';
      suspicionOrb.style.background = `radial-gradient(circle, ${color}, transparent)`;
      suspicionOrb.style.boxShadow = `0 0 ${20 + level * 30}px ${color}`;
    }
  }

  clearSuspicion() {
    this.updateSuspicionLevel(0);
  }

  resetBreathCycle() {
    const breathRing = document.getElementById('breathRing');
    if (breathRing) {
      breathRing.style.animation = 'none';
      breathRing.offsetHeight;
      breathRing.style.animation = 'breath-pulse 3s ease-in-out infinite';
    }
  }

  showSpellInfo(spell) {
    const spellInfo = document.getElementById('spellInfo');
    if (spellInfo) {
      spellInfo.innerHTML = `
                <div class="spell-info-name">${spell.name}</div>
                <div class="spell-info-description">${spell.description}</div>
                <div class="spell-info-effect">${spell.effect}</div>
                <div class="spell-info-cost">Cost: ${spell.cost} coherence</div>
            `;
    }
  }

  hideSpellInfo() {
    const spellInfo = document.getElementById('spellInfo');
    if (spellInfo) {
      spellInfo.innerHTML = '<span>Select a spell to see its details</span>';
    }
  }

  showMessage(message, type = 'info') {
    const messageElement = document.createElement('div');
    messageElement.className = `spellbook-message ${type}`;
    messageElement.textContent = message;
    messageElement.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#f87171' : '#4ade80'};
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            z-index: 10001;
            animation: message-slide-in 0.3s ease-out;
        `;

    document.body.appendChild(messageElement);

    setTimeout(() => {
      document.body.removeChild(messageElement);
    }, 3000);
  }

  startUnlockConditions() {
    // Monitor for unlock conditions
    setInterval(() => {
      this.checkUnlockConditions();
    }, 5000);
  }

  checkUnlockConditions() {
    // Check for triple caesura
    if (this.checkTripleCaesura()) {
      this.unlockSpell('mirror.bloom');
    }

    // Check for breath sync
    if (this.checkBreathSync90()) {
      this.unlockSpell('caesura.whisper');
    }

    // Check for coherence 100
    if (this.getCurrentCoherence() >= 100) {
      this.unlockSpell('spiral.resonance');
    }
  }

  checkTripleCaesura() {
    // This would integrate with the actual breath detection
    // For now, simulate based on time
    return Math.random() < 0.01; // 1% chance every 5 seconds
  }

  checkBreathSync90() {
    // This would integrate with actual breath sync tracking
    // For now, simulate based on coherence
    return this.getCurrentCoherence() > 50;
  }

  unlockSpell(spellId) {
    if (!this.unlockedSpells.has(spellId)) {
      this.unlockedSpells.add(spellId);
      this.renderSpells();

      // Show unlock notification
      const spell = this.spells[spellId];
      this.showMessage(`New spell unlocked: ${spell.name}!`, 'success');

      // Add quest entry
      if (window.whorlGameframeBridge) {
        window.whorlGameframeBridge.addQuest('spell.unlock', `Unlocked ${spell.name}`, 10);
      }
    }
  }

  bindEventListeners() {
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.altKey) {
        switch (e.key) {
          case '1':
            this.castSpell('pause.hum');
            break;
          case '2':
            this.castSpell('overflow.flutter');
            break;
          case '3':
            this.castSpell('cleanse');
            break;
        }
      }
    });
  }
}

// Add CSS for spellbook
const spellbookStyles = document.createElement('style');
spellbookStyles.textContent = `
    .spellbook-container {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid var(--accent-purple);
        margin-top: 1rem;
        box-shadow: 0 0 20px rgba(179, 102, 255, 0.2);
    }
    
    .spellbook-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        font-family: 'Fira Code', monospace;
    }
    
    .spellbook-header h3 {
        color: var(--accent-purple);
        font-size: 14px;
        font-weight: 600;
    }
    
    .spell-count {
        background: var(--bg-tertiary);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 10px;
        color: var(--text-secondary);
    }
    
    .spells-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .spell-card {
        background: var(--bg-tertiary);
        border: 1px solid var(--text-secondary);
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .spell-card.unlocked:hover {
        border-color: var(--accent-purple);
        box-shadow: 0 0 10px var(--accent-purple);
        transform: translateY(-2px);
    }
    
    .spell-card.locked {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .spell-card.cooldown {
        cursor: not-allowed;
    }
    
    .spell-icon {
        font-size: 24px;
        margin-bottom: 0.5rem;
    }
    
    .spell-name {
        font-family: 'Fira Code', monospace;
        font-size: 10px;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .spell-cost {
        font-size: 8px;
        color: var(--text-secondary);
    }
    
    .cooldown-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to top, rgba(0,0,0,0.7) var(--progress), transparent var(--progress));
        pointer-events: none;
    }
    
    .spellbook-footer {
        border-top: 1px solid var(--text-secondary);
        padding-top: 1rem;
    }
    
    .spell-info {
        font-size: 11px;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    .spell-info-name {
        color: var(--accent-purple);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .spell-info-description {
        margin-bottom: 0.5rem;
    }
    
    .spell-info-effect {
        color: var(--accent-green);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .spell-info-cost {
        color: var(--accent-orange);
        font-weight: 600;
    }
    
    @keyframes spell-effect {
        0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
        20% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
        80% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(1.2); opacity: 0; }
    }
    
    @keyframes overflow-effect {
        0% { opacity: 0; }
        50% { opacity: 1; }
        100% { opacity: 0; }
    }
    
    @keyframes cleansing-particle {
        0% { 
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
        }
        100% { 
            transform: translate(calc(-50% + var(--end-x)), calc(-50% + var(--end-y))) scale(0);
            opacity: 0;
        }
    }
    
    @keyframes message-slide-in {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(spellbookStyles);

// Initialize spellbook when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  if (window.whorlGameframeBridge) {
    window.whorlSpellbook = new WhorlSpellbook();
  }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = WhorlSpellbook;
}

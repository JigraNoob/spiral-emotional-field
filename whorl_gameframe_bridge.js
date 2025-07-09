/**
 * Whorl Gameframe Bridge
 * Detects gameframe mode and switches between sacred and gamified interfaces
 */

class WhorlGameframeBridge {
  constructor() {
    this.isGameframeMode = this.detectGameframeMode();
    this.sacredInterface = null;
    this.gameframeInterface = null;
    this.currentMode = this.isGameframeMode ? 'gameframe' : 'sacred';

    this.initializeInterface();
  }

  detectGameframeMode() {
    const urlParams = new URLSearchParams(window.location.search);
    return (
      urlParams.get('gameframe') === 'true' ||
      urlParams.get('mode') === 'game' ||
      localStorage.getItem('whorl_gameframe') === 'true'
    );
  }

  initializeInterface() {
    if (this.isGameframeMode) {
      this.loadGameframeInterface();
    } else {
      this.loadSacredInterface();
    }

    // Add mode toggle
    this.addModeToggle();
  }

  loadGameframeInterface() {
    // Load the gamified interface
    this.currentMode = 'gameframe';
    document.title = '∷ Code Garden: Mystic Dev Minigame ∶';

    // Add game-specific CSS
    this.addGameframeStyles();

    // Initialize game mechanics
    this.initializeGameMechanics();

    console.log('🎮 Gameframe mode activated - Sacred systems disguised as play');
  }

  loadSacredInterface() {
    // Load the sacred interface
    this.currentMode = 'sacred';
    document.title = '∷ Whorl: The IDE That Breathes ∶';

    // Remove game-specific elements
    this.removeGameframeElements();

    console.log('🌀 Sacred mode activated - Breath-aware development chamber');
  }

  addGameframeStyles() {
    const style = document.createElement('style');
    style.textContent = `
            /* Gameframe-specific styles */
            .gameframe-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: linear-gradient(45deg, rgba(0,0,0,0.1), rgba(74,158,255,0.05));
                pointer-events: none;
                z-index: 1000;
            }
            
            .gameframe-particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 999;
            }
            
            .gameframe-particle {
                position: absolute;
                width: 2px;
                height: 2px;
                background: #4a9eff;
                border-radius: 50%;
                animation: gameframe-float 6s infinite linear;
                opacity: 0.6;
            }
            
            @keyframes gameframe-float {
                0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
                10% { opacity: 0.6; }
                90% { opacity: 0.6; }
                100% { transform: translateY(-10px) rotate(360deg); opacity: 0; }
            }
        `;
    document.head.appendChild(style);
  }

  initializeGameMechanics() {
    // Initialize floating particles
    this.createParticles();

    // Add game-specific event listeners
    this.addGameframeEventListeners();

    // Initialize quest system
    this.initializeQuestSystem();
  }

  createParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'gameframe-particles';
    document.body.appendChild(particlesContainer);

    for (let i = 0; i < 15; i++) {
      const particle = document.createElement('div');
      particle.className = 'gameframe-particle';
      particle.style.left = Math.random() * 100 + '%';
      particle.style.animationDelay = Math.random() * 6 + 's';
      particle.style.animationDuration = Math.random() * 3 + 3 + 's';
      particlesContainer.appendChild(particle);
    }
  }

  addGameframeEventListeners() {
    // Add keyboard shortcuts for game mode
    document.addEventListener('keydown', (e) => {
      if (e.altKey && e.key === 'g') {
        this.toggleMode();
        e.preventDefault();
      }
    });

    // Add click effects for suspicion orb
    const suspicionOrb = document.getElementById('suspicionOrb');
    if (suspicionOrb) {
      suspicionOrb.addEventListener('click', () => {
        this.triggerBossBattle();
      });
    }
  }

  initializeQuestSystem() {
    // Initialize quest tracking
    this.questSystem = {
      quests: [],
      coherence: 0,
      achievements: new Set(),
    };

    // Add initial quest
    this.addQuest('game.start', 'Code Garden awakened - Mystic dev minigame activated', 10);
  }

  addQuest(type, message, reward) {
    const quest = {
      id: 'quest-' + Date.now(),
      type: type,
      message: message,
      reward: reward,
      timestamp: new Date(),
    };

    this.questSystem.quests.push(quest);
    this.questSystem.coherence += reward;

    // Update UI if quest container exists
    const questContainer = document.getElementById('questContainer');
    if (questContainer) {
      this.renderQuest(quest, questContainer);
    }

    // Check for achievements
    this.checkAchievements();

    return quest;
  }

  renderQuest(quest, container) {
    const questElement = document.createElement('div');
    questElement.className = 'quest-entry';
    questElement.innerHTML = `
            <div class="quest-header">
                <span class="quest-type">${quest.type}</span>
                <span>${quest.timestamp.toLocaleTimeString()}</span>
            </div>
            <div class="quest-message">${quest.message}</div>
            <div class="quest-reward">+${quest.reward} coherence</div>
        `;

    container.appendChild(questElement);
    container.scrollTop = container.scrollHeight;

    // Keep only last 10 quests
    if (container.children.length > 10) {
      container.removeChild(container.children[0]);
    }
  }

  checkAchievements() {
    const achievements = [
      {
        id: 'first_breath',
        condition: () => this.questSystem.coherence >= 10,
        name: 'First Breath',
      },
      {
        id: 'ritual_master',
        condition: () => this.questSystem.quests.filter((q) => q.type === 'spell.cast').length >= 3,
        name: 'Ritual Master',
      },
      {
        id: 'boss_slayer',
        condition: () =>
          this.questSystem.quests.filter((q) => q.type === 'boss.battle').length >= 1,
        name: 'Boss Slayer',
      },
      {
        id: 'coherence_100',
        condition: () => this.questSystem.coherence >= 100,
        name: 'Coherence Master',
      },
    ];

    achievements.forEach((achievement) => {
      if (!this.questSystem.achievements.has(achievement.id) && achievement.condition()) {
        this.questSystem.achievements.add(achievement.id);
        this.addQuest('achievement.unlocked', `Achievement Unlocked: ${achievement.name}`, 25);
        this.showAchievementNotification(achievement.name);
      }
    });
  }

  showAchievementNotification(achievementName) {
    const notification = document.createElement('div');
    notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(74, 158, 255, 0.9);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-family: 'Fira Code', monospace;
            font-weight: bold;
            z-index: 10001;
            animation: achievement-notification 3s ease-out forwards;
        `;
    notification.textContent = `🏆 ${achievementName} Unlocked!`;
    document.body.appendChild(notification);

    setTimeout(() => {
      document.body.removeChild(notification);
    }, 3000);
  }

  triggerBossBattle() {
    const suspicionLevel = this.getSuspicionLevel();
    if (suspicionLevel > 0.7) {
      this.addQuest('boss.battle', 'BOSS BATTLE: Ritual Overflow Detected!', 20);
      this.clearSuspicion();
      this.showBossBattleEffect();
    }
  }

  getSuspicionLevel() {
    // This would integrate with the actual suspicion meter
    const suspicionOrb = document.getElementById('suspicionOrb');
    if (suspicionOrb) {
      // Extract suspicion level from visual state
      const style = window.getComputedStyle(suspicionOrb);
      const boxShadow = style.boxShadow;
      if (boxShadow.includes('#f87171')) return 0.8;
      if (boxShadow.includes('#fbbf24')) return 0.5;
      return 0.2;
    }
    return 0;
  }

  clearSuspicion() {
    // Clear suspicion meter
    const suspicionOrb = document.getElementById('suspicionOrb');
    if (suspicionOrb) {
      suspicionOrb.style.background = 'radial-gradient(circle, #4ade80, transparent)';
      suspicionOrb.style.boxShadow = '0 0 20px #4ade80';
    }
  }

  showBossBattleEffect() {
    // Visual effect for boss battle
    const effect = document.createElement('div');
    effect.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: radial-gradient(circle, rgba(248, 113, 113, 0.3), transparent);
            pointer-events: none;
            z-index: 10000;
            animation: boss-battle-effect 2s ease-out forwards;
        `;
    document.body.appendChild(effect);

    setTimeout(() => {
      document.body.removeChild(effect);
    }, 2000);
  }

  addModeToggle() {
    const toggle = document.createElement('button');
    toggle.textContent = this.currentMode === 'gameframe' ? '🌀 Sacred' : '🎮 Game';
    toggle.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--bg-tertiary);
            border: 1px solid var(--accent-blue);
            color: var(--accent-blue);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.3s ease;
        `;

    toggle.addEventListener('click', () => {
      this.toggleMode();
    });

    toggle.addEventListener('mouseenter', () => {
      toggle.style.background = 'var(--accent-blue)';
      toggle.style.color = 'var(--bg-primary)';
    });

    toggle.addEventListener('mouseleave', () => {
      toggle.style.background = 'var(--bg-tertiary)';
      toggle.style.color = 'var(--accent-blue)';
    });

    document.body.appendChild(toggle);
  }

  toggleMode() {
    if (this.currentMode === 'gameframe') {
      this.loadSacredInterface();
    } else {
      this.loadGameframeInterface();
    }

    // Update localStorage
    localStorage.setItem('whorl_gameframe', this.currentMode === 'gameframe');

    // Update URL
    const url = new URL(window.location);
    if (this.currentMode === 'gameframe') {
      url.searchParams.set('gameframe', 'true');
    } else {
      url.searchParams.delete('gameframe');
    }
    window.history.replaceState({}, '', url);
  }

  removeGameframeElements() {
    // Remove game-specific elements
    const particles = document.querySelector('.gameframe-particles');
    if (particles) {
      document.body.removeChild(particles);
    }

    const overlay = document.querySelector('.gameframe-overlay');
    if (overlay) {
      document.body.removeChild(overlay);
    }
  }
}

// Initialize the bridge when the page loads
document.addEventListener('DOMContentLoaded', () => {
  window.whorlGameframeBridge = new WhorlGameframeBridge();
});

// Add CSS for animations
const gameframeAnimations = document.createElement('style');
gameframeAnimations.textContent = `
    @keyframes achievement-notification {
        0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
        20% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
        80% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
    }
    
    @keyframes boss-battle-effect {
        0% { opacity: 0; }
        50% { opacity: 1; }
        100% { opacity: 0; }
    }
`;
document.head.appendChild(gameframeAnimations);

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = WhorlGameframeBridge;
}

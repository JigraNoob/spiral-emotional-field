// Threshold Shimmer Transition System
class TransitionManager {
  constructor() {
    this.transitions = {
      'shimmerfold': this.shimmerfold.bind(this),
      'memoryRipple': this.memoryRipple.bind(this),
      'spiralTurn': this.spiralTurn.bind(this),
      'eyeCloseOpen': this.eyeCloseOpen.bind(this),
      'breathFade': this.breathFade.bind(this)
    };
    
    this.toneformMapping = {
      'joy': 'memoryRipple',
      'grief': 'eyeCloseOpen',
      'longing': 'shimmerfold',
      'trust': 'breathFade',
      'default': 'breathFade'
    };
    
    // Create transition overlay element
    this.transitionOverlay = document.createElement('div');
    this.transitionOverlay.className = 'transition-overlay';
    document.body.appendChild(this.transitionOverlay);
  }

  // Main transition function
  thresholdShimmer(currentState, nextState, toneform, options = {}) {
    const transitionType = this.toneformMapping[toneform] || this.toneformMapping['default'];
    return this.transitions[transitionType](currentState, nextState, options);
  }

  shimmerfold(currentState, nextState) {
    return new Promise((resolve) => {
      // Set fabric color based on toneform
      const fabricColor = currentState.toneform?.color || '#5e35b1';
      
      // Create fabric ripple elements
      const ripple1 = document.createElement('div');
      const ripple2 = document.createElement('div');
      
      ripple1.className = 'shimmer-ripple';
      ripple2.className = 'shimmer-ripple';
      
      ripple1.style.background = fabricColor;
      ripple2.style.background = fabricColor;
      
      this.transitionOverlay.innerHTML = '';
      this.transitionOverlay.appendChild(ripple1);
      this.transitionOverlay.appendChild(ripple2);
      
      // Animate ripples
      ripple1.animate([
        { transform: 'translateX(-100%) scaleX(1.5)', opacity: 0.8 },
        { transform: 'translateX(100%) scaleX(0.5)', opacity: 0 }
      ], {
        duration: 800,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
      });
      
      ripple2.animate([
        { transform: 'translateX(-100%) scaleX(1.2)', opacity: 0.6 },
        { transform: 'translateX(100%) scaleX(0.8)', opacity: 0 }
      ], {
        duration: 1000,
        delay: 100,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
      }).onfinish = () => {
        this.transitionOverlay.innerHTML = '';
        resolve(nextState);
      };
    });
  }

  memoryRipple(currentState, nextState, options = {}) {
    return new Promise((resolve) => {
      const ripple = document.createElement('div');
      ripple.className = 'memory-ripple';
      
      // Use provided origin or default to altar center
      if (options.origin) {
        ripple.style.left = `${options.origin.x}px`;
        ripple.style.top = `${options.origin.y}px`;
      } else {
        const altar = document.getElementById('altar-container');
        const rect = altar.getBoundingClientRect();
        ripple.style.left = `${rect.left + rect.width/2}px`;
        ripple.style.top = `${rect.top + rect.height/2}px`;
      }
      
      document.body.appendChild(ripple);
      
      const animation = ripple.animate([
        { transform: 'translate(-50%, -50%) scale(0)', opacity: 1 },
        { transform: 'translate(-50%, -50%) scale(3)', opacity: 0 }
      ], {
        duration: 1200,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
      });
      
      animation.onfinish = () => {
        ripple.remove();
        resolve(nextState);
      };
    });
  }

  eyeCloseOpen(currentState, nextState) {
    return new Promise((resolve) => {
      // Create eyelid elements
      const topLid = document.createElement('div');
      topLid.className = 'eyelid top';
      
      const bottomLid = document.createElement('div');
      bottomLid.className = 'eyelid bottom';
      
      document.body.appendChild(topLid);
      document.body.appendChild(bottomLid);
      
      // Animate eyelids closing then opening
      const closeDuration = 800;
      const holdDuration = 400;
      
      topLid.animate([
        { transform: 'translateY(-100%)' },
        { transform: 'translateY(0)' }
      ], { duration: closeDuration, easing: 'cubic-bezier(0.33, 1, 0.68, 1)' });
      
      bottomLid.animate([
        { transform: 'translateY(100%)' },
        { transform: 'translateY(0)' }
      ], { 
        duration: closeDuration, 
        easing: 'cubic-bezier(0.33, 1, 0.68, 1)',
        fill: 'forwards'
      }).onfinish = () => {
        // Pause briefly before opening
        setTimeout(() => {
          topLid.animate([
            { transform: 'translateY(0)' },
            { transform: 'translateY(-100%)' }
          ], { duration: closeDuration, easing: 'cubic-bezier(0.33, 1, 0.68, 1)' });
          
          bottomLid.animate([
            { transform: 'translateY(0)' },
            { transform: 'translateY(100%)' }
          ], { 
            duration: closeDuration, 
            easing: 'cubic-bezier(0.33, 1, 0.68, 1)',
            fill: 'forwards'
          }).onfinish = () => {
            topLid.remove();
            bottomLid.remove();
            resolve(nextState);
          };
        }, holdDuration);
      };
    });
  }

  breathFade(currentState, nextState) {
    return new Promise((resolve) => {
      // Find all shimmer elements
      const shimmerElements = document.querySelectorAll('.shimmer-effect, .murmur-shimmer, .bundle-glyph');
      
      // Create breath overlay
      const breathOverlay = document.createElement('div');
      breathOverlay.className = 'breath-fade';
      document.body.appendChild(breathOverlay);
      
      // Add sync class to shimmer elements
      shimmerElements.forEach(el => el.classList.add('breath-sync'));
      
      // Animate inhale/exhale cycle
      const animation = breathOverlay.animate([
        { opacity: 0, backgroundColor: 'rgba(230, 240, 255, 0)' },
        { opacity: 0.4, backgroundColor: 'rgba(200, 220, 240, 0.4)' },
        { opacity: 0, backgroundColor: 'rgba(230, 240, 255, 0)' }
      ], {
        duration: 1800,
        easing: 'cubic-bezier(0.33, 0, 0.67, 1)'
      });
      
      animation.onfinish = () => {
        // Remove sync class after animation
        shimmerElements.forEach(el => el.classList.remove('breath-sync'));
        breathOverlay.remove();
        resolve(nextState);
      };
    });
  }

  async triggerRuptureFlicker() {
    return new Promise((resolve) => {
      // Create flicker elements around altar edges
      const flickers = [];
      const altar = document.getElementById('altar-container');
      const rect = altar.getBoundingClientRect();
      
      // Create 4 flicker points (top, right, bottom, left)
      const positions = [
        { x: rect.left + rect.width/2, y: rect.top },
        { x: rect.right, y: rect.top + rect.height/2 },
        { x: rect.left + rect.width/2, y: rect.bottom },
        { x: rect.left, y: rect.top + rect.height/2 }
      ];
      
      positions.forEach(pos => {
        const flicker = document.createElement('div');
        flicker.className = 'rupture-flicker';
        flicker.style.left = `${pos.x}px`;
        flicker.style.top = `${pos.y}px`;
        document.body.appendChild(flicker);
        flickers.push(flicker);
      });
      
      // Animate flicker
      const animation = Promise.all(
        flickers.map(flicker => {
          return flicker.animate([
            { opacity: 0, transform: 'scale(1)' },
            { opacity: 0.8, transform: 'scale(1.2)' },
            { opacity: 0, transform: 'scale(1)' }
          ], {
            duration: 400,
            easing: 'cubic-bezier(0.5, 0, 0.75, 1)'
          }).finished;
        })
      );
      
      animation.then(() => {
        flickers.forEach(f => f.remove());
        resolve();
      });
    });
  }

  // Other transition methods would be implemented similarly
}

// Export singleton instance
export const transitionManager = new TransitionManager();

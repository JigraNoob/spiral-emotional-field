/**
 * Spiral Override Shimmer System
 * Provides real-time visual feedback for override states
 */

class SpiralShimmer {
    constructor() {
        this.currentState = null;
        this.updateInterval = 3000; // 3 seconds
        this.init();
    }

    async init() {
        await this.updateShimmer();
        setInterval(() => this.updateShimmer(), this.updateInterval);
    }

    async fetchOverrideState() {
        try {
            const response = await fetch('/api/override_state');
            if (!response.ok) return null;
            return await response.json();
        } catch (error) {
            console.warn('🌀 Shimmer: Failed to fetch override state:', error);
            return null;
        }
    }

    async updateShimmer() {
        const state = await this.fetchOverrideState();
        if (state && state !== this.currentState) {
            this.applyShimmer(state);
            this.currentState = state;
        }
    }

    applyShimmer(state) {
        const chamber = document.querySelector('.spiral-chamber') || document.body;
        const glintStream = document.getElementById('glint-stream');
        
        // Remove existing shimmer classes
        chamber.classList.remove(
            'shimmer-natural', 'shimmer-amplified', 'shimmer-muted', 
            'shimmer-ritual', 'shimmer-deferral'
        );

        // Apply mode-specific shimmer
        const mode = state.mode?.replace('ResonanceMode.', '') || 'NATURAL';
        
        switch (mode) {
            case 'AMPLIFIED':
                chamber.classList.add('shimmer-amplified');
                this.addIntensityGlow(state.intensity || 2.0);
                break;
            case 'MUTED':
                chamber.classList.add('shimmer-muted');
                break;
            case 'RITUAL':
                chamber.classList.add('shimmer-ritual');
                this.addRitualSigil();
                break;
            case 'DEFERRAL':
                chamber.classList.add('shimmer-deferral');
                break;
            default:
                chamber.classList.add('shimmer-natural');
        }

        // Apply emotional state hue if present
        if (state.emotional_state) {
            chamber.classList.add(`shimmer-emotion-${state.emotional_state}`);
        }

        // Update glint stream with override indicator
        this.updateGlintStreamIndicator(state);
    }

    addIntensityGlow(intensity) {
        const chamber = document.querySelector('.spiral-chamber') || document.body;
        chamber.style.setProperty('--shimmer-intensity', intensity);
    }

    addRitualSigil() {
        // Add ritual glyph overlay
        const existing = document.querySelector('.ritual-sigil');
        if (existing) existing.remove();

        const sigil = document.createElement('div');
        sigil.className = 'ritual-sigil';
        sigil.innerHTML = '∷';
        document.body.appendChild(sigil);
    }

    updateGlintStreamIndicator(state) {
        const indicator = document.getElementById('override-indicator') || this.createOverrideIndicator();
        const mode = state.mode?.replace('ResonanceMode.', '') || 'NATURAL';
        
        indicator.textContent = `🌀 Override: ${mode}`;
        indicator.className = `override-indicator override-${mode.toLowerCase()}`;
        
        if (state.active) {
            indicator.style.display = 'block';
        } else {
            indicator.style.display = 'none';
        }
    }

    createOverrideIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'override-indicator';
        indicator.className = 'override-indicator';
        
        const header = document.querySelector('h1') || document.body.firstChild;
        header.parentNode.insertBefore(indicator, header.nextSibling);
        
        return indicator;
    }
}

// Initialize shimmer system when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new SpiralShimmer();
});

// Export for manual control if needed
window.SpiralShimmer = SpiralShimmer;
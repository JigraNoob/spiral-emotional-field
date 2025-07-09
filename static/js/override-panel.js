/**
 * Spiral Override Panel
 * Real-time override state visualization and control
 */

class SpiralOverridePanel {
    constructor() {
        this.currentState = null;
        this.updateInterval = 2000; // 2 seconds
        this.panel = null;
        this.init();
    }

    async init() {
        this.createPanel();
        await this.updateState();
        setInterval(() => this.updateState(), this.updateInterval);
        this.bindControls();
    }

    createPanel() {
        // Remove existing panel if present
        const existing = document.getElementById('override-panel');
        if (existing) existing.remove();

        this.panel = document.createElement('div');
        this.panel.id = 'override-panel';
        this.panel.className = 'override-panel';
        this.panel.innerHTML = `
            <div class="override-header">
                <div class="override-glyph" id="override-glyph">🌿</div>
                <div class="override-title">
                    <span class="override-mode" id="override-mode">NATURAL</span>
                    <span class="override-status" id="override-status">∷ equilibrium ∷</span>
                </div>
            </div>
            
            <div class="override-metrics">
                <div class="intensity-meter">
                    <div class="intensity-label">Intensity</div>
                    <div class="intensity-bar">
                        <div class="intensity-fill" id="intensity-fill"></div>
                        <span class="intensity-value" id="intensity-value">1.0x</span>
                    </div>
                </div>
                
                <div class="emotional-state">
                    <div class="emotional-label">Emotional State</div>
                    <div class="emotional-indicator" id="emotional-indicator">—</div>
                </div>
            </div>

            <div class="override-controls">
                <button class="mode-btn" data-mode="NATURAL">🌿 Natural</button>
                <button class="mode-btn" data-mode="AMPLIFIED">🌀 Amplified</button>
                <button class="mode-btn" data-mode="MUTED">🌙 Muted</button>
                <button class="mode-btn" data-mode="RITUAL">✨ Ritual</button>
                <button class="mode-btn" data-mode="EMOTIONAL">💧 Emotional</button>
                <button class="mode-btn" data-mode="DEFERRAL">⏳ Deferral</button>
            </div>

            <div class="override-footer">
                <div class="duration" id="override-duration">—</div>
                <button class="deactivate-btn" id="deactivate-btn">Deactivate</button>
            </div>
        `;

        // Insert panel into dashboard
        const dashboard = document.querySelector('.spiral-chamber') || document.body;
        dashboard.appendChild(this.panel);
    }

    async updateState() {
        try {
            const response = await fetch('/api/override_state');
            if (!response.ok) return;
            
            const state = await response.json();
            if (JSON.stringify(state) !== JSON.stringify(this.currentState)) {
                this.applyState(state);
                this.currentState = state;
            }
        } catch (error) {
            console.warn('🌀 Override Panel: Failed to fetch state:', error);
        }
    }

    applyState(state) {
        const mode = state.mode?.replace('ResonanceMode.', '') || 'NATURAL';
        const intensity = state.intensity || 1.0;
        const emotional = state.emotional_state || null;
        const active = state.active || false;

        // Update mode display
        document.getElementById('override-mode').textContent = mode;
        document.getElementById('override-status').textContent = this.getModeStatus(mode);
        
        // Update glyph
        const glyph = this.getModeGlyph(mode);
        document.getElementById('override-glyph').textContent = glyph;
        
        // Update intensity meter
        const intensityFill = document.getElementById('intensity-fill');
        const intensityValue = document.getElementById('intensity-value');
        intensityFill.style.width = `${Math.min(intensity * 50, 100)}%`;
        intensityValue.textContent = `${intensity.toFixed(1)}x`;
        
        // Update emotional state
        document.getElementById('emotional-indicator').textContent = emotional || '—';
        
        // Update duration
        document.getElementById('override-duration').textContent = state.duration || '—';
        
        // Apply visual styling
        this.panel.className = `override-panel mode-${mode.toLowerCase()}`;
        
        // Update active button
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.mode === mode && active) {
                btn.classList.add('active');
            }
        });

        // Apply chamber-wide effects
        this.applyChamberEffects(mode, intensity, emotional);
    }

    getModeGlyph(mode) {
        const glyphs = {
            'NATURAL': '🌿',
            'AMPLIFIED': '🌀',
            'MUTED': '🌙',
            'RITUAL': '✨',
            'EMOTIONAL': '💧',
            'DEFERRAL': '⏳'
        };
        return glyphs[mode] || '🌿';
    }

    getModeStatus(mode) {
        const statuses = {
            'NATURAL': '∷ equilibrium ∷',
            'AMPLIFIED': '∷ intensity ∷',
            'MUTED': '∷ restraint ∷',
            'RITUAL': '∷ ceremonial ∷',
            'EMOTIONAL': '∷ feeling ∷',
            'DEFERRAL': '∷ patience ∷'
        };
        return statuses[mode] || '∷ unknown ∷';
    }

    applyChamberEffects(mode, intensity, emotional) {
        const chamber = document.querySelector('.spiral-chamber') || document.body;
        
        // Remove existing override classes
        chamber.classList.remove(
            'override-natural', 'override-amplified', 'override-muted',
            'override-ritual', 'override-emotional', 'override-deferral'
        );
        
        // Apply mode-specific class
        chamber.classList.add(`override-${mode.toLowerCase()}`);
        
        // Set intensity CSS variable
        chamber.style.setProperty('--override-intensity', intensity);
        
        // Apply emotional hue if present
        if (emotional) {
            chamber.classList.add(`emotional-${emotional}`);
        }
    }

    bindControls() {
        // Mode activation buttons
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.activateMode(btn.dataset.mode);
            });
        });

        // Deactivation button
        document.getElementById('deactivate-btn').addEventListener('click', () => {
            this.deactivateOverride();
        });
    }

    async activateMode(mode) {
        try {
            const response = await fetch('/api/override/activate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    mode: mode,
                    intensity: this.getDefaultIntensity(mode)
                })
            });

            if (response.ok) {
                console.log(`🌀 Override activated: ${mode}`);
                await this.updateState(); // Immediate update
            }
        } catch (error) {
            console.error('Failed to activate override mode:', error);
        }
    }

    async deactivateOverride() {
        try {
            const response = await fetch('/api/override/deactivate', {
                method: 'POST'
            });

            if (response.ok) {
                console.log('🌀 Override deactivated');
                await this.updateState(); // Immediate update
            }
        } catch (error) {
            console.error('Failed to deactivate override:', error);
        }
    }

    getDefaultIntensity(mode) {
        const defaults = {
            'NATURAL': 1.0,
            'AMPLIFIED': 1.8,
            'MUTED': 0.3,
            'RITUAL': 1.2,
            'EMOTIONAL': 1.4,
            'DEFERRAL': 0.8
        };
        return defaults[mode] || 1.0;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new SpiralOverridePanel();
});

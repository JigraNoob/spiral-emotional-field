
// Reflection Voice JS modal creation and integration
// (Full integration of toneform guidance, modal behavior, and application to Echo Shrine)

class ReflectionVoice {
    constructor() {
        this.isActive = false;
        this.currentReflection = null;
        this.createReflectionModal();
    }

    createReflectionModal() {
        const modalHTML = `
            <div id="reflectionModal" class="reflection-modal hidden">
                <div class="reflection-content">
                    <div class="reflection-header">
                        <span class="reflection-glyph" id="reflectionGlyph">🌀</span>
                        <h3 class="reflection-title">Reflection Voice</h3>
                        <button class="reflection-close" onclick="reflectionVoice.closeReflection()">×</button>
                    </div>
                    <div class="reflection-body">
                        <div class="divergence-context">
                            <span class="context-label">Divergence Detected:</span>
                            <span id="divergenceType" class="divergence-type"></span>
                        </div>
                        <div class="reflection-text" id="reflectionText"></div>
                        <div class="reflection-controls">
                            <div class="depth-selector">
                                <label>Reflection Depth:</label>
                                <div class="depth-options">
                                    <button class="depth-option" data-depth="gentle">🌱 Gentle</button>
                                    <button class="depth-option" data-depth="deep">🌊 Deep</button>
                                    <button class="depth-option" data-depth="ceremonial">🕯️ Ceremonial</button>
                                </div>
                            </div>
                            <div class="reflection-actions">
                                <button class="action-btn secondary" onclick="reflectionVoice.requestLineageReflection()">
                                    🌿 Reflect on Lineage
                                </button>
                                <button class="action-btn primary" onclick="reflectionVoice.requestToneformGuidance()">
                                    🎵 Get Toneform Guidance
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);

        document.querySelectorAll('.depth-option').forEach(option => {
            option.addEventListener('click', (e) => {
                document.querySelectorAll('.depth-option').forEach(opt => 
                    opt.classList.remove('selected'));
                e.target.classList.add('selected');

                if (this.currentReflection) {
                    this.requestReflection({
                        echo_id: this.currentReflection.echo_id,
                        divergence_type: this.currentReflection.divergence_type,
                        depth: e.target.dataset.depth
                    });
                }
            });
        });
    }

    async requestToneformGuidance() {
        const currentToneform = prompt("Current toneform:");
        const targetToneform = prompt("Desired toneform:");
        const content = prompt("Content to transform:");

        if (currentToneform && targetToneform && content) {
            const reflectionText = document.getElementById('reflectionText');
            reflectionText.innerHTML = '<div class="reflection-loading">🎵 Listening for toneform guidance...</div>';

            try {
                const response = await fetch('/api/reflect/toneform-guidance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        current_toneform: currentToneform,
                        target_toneform: targetToneform,
                        content: content
                    })
                });

                if (response.ok) {
                    const result = await response.json();
                    reflectionText.innerHTML = `
                        <div class="toneform-guidance">
                            <h4>🎵 Toneform Guidance</h4>
                            <div class="guidance-body">
                                ${this.formatReflectionText(result.guidance)}
                            </div>
                            <div class="guidance-metadata">
                                <span>From: ${result.transformation.from}</span>
                                <span>To: ${result.transformation.to}</span>
                            </div>
                        </div>
                    `;
                }
            } catch (error) {
                reflectionText.innerHTML = '<div class="reflection-error">🌫️ Unable to retrieve toneform guidance</div>';
            }
        }
    }

    async requestReflection(context = {}) {
        if (this.isActive) return;

        this.isActive = true;
        this.showModal();

        const reflectionText = document.getElementById('reflectionText');
        reflectionText.innerHTML = '<div class="reflection-loading">🌫️ The Spiral gathers its voice...</div>';

        try {
            const response = await fetch('/api/reflect/voice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(context)
            });

            if (response.ok) {
                const result = await response.json();
                this.displayReflection(result);
            } else {
                reflectionText.innerHTML = '<div class="reflection-error">🌫️ The Spiral's voice is distant...</div>';
            }

        } catch (error) {
            console.error('Error requesting reflection:', error);
            reflectionText.innerHTML = '<div class="reflection-error">🌫️ Unable to reach the Spiral's voice</div>';
        }
    }

    displayReflection(data) {
        this.currentReflection = data;
        const reflectionText = document.getElementById('reflectionText');
        const reflectionGlyph = document.getElementById('reflectionGlyph');
        const divergenceType = document.getElementById('divergenceType');
        const modalContent = document.querySelector('.reflection-content');

        reflectionGlyph.textContent = this.getToneformGlyph(data.inflected_with || 'unknown');
        divergenceType.textContent = this.formatDivergenceType(data.divergence_type || '');
        reflectionText.innerHTML = this.formatReflectionText(data.message);

        // Add shimmer effect
        modalContent.classList.add('shimmer');
        setTimeout(() => {
            modalContent.classList.remove('shimmer');
        }, 500);
    }

    closeReflection() {
        this.isActive = false;
        this.currentReflection = null;
        const modal = document.getElementById('reflectionModal');
        modal.classList.add('hidden');
    }

    getToneformGlyph(toneform) {
        const glyphMap = {
            'practical': '⟁',
            'emotional': '❦',
            'intellectual': '∿',
            'spiritual': '∞',
            'relational': '☍',
            'ceremonial': '🕯️',
            'unknown': '◯'
        };
        return glyphMap[toneform.toLowerCase()] || '◯';
    }

    formatDivergenceType(type) {
        const map = {
            'toneform_mismatch': 'Toneform Mismatch',
            'phase_drift': 'Phase Drift',
            'semantic_shift': 'Semantic Shift'
        };
        return map[type] || type;
    }

    formatReflectionText(text) {
        return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }

    showModal() {
        const modal = document.getElementById('reflectionModal');
        modal.classList.remove('hidden');
    }
}

// Initialize the Reflection Voice
const reflectionVoice = new ReflectionVoice();

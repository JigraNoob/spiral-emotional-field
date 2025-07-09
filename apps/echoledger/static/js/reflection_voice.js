class ReflectionVoice {
    constructor() {
        this.isActive = false;
        this.currentReflection = null;
        this.selectedDepth = 'gentle';
        this.createReflectionModal();
        this.bindEvents();
        this.setupRemoteWhisperListening();
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
                                <button class="action-btn secondary" onclick="reflectionVoice.requestResourceReflection()">
                                    🌾 Reflect on Resource
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById('reflectionModal');
        this.reflectionText = document.getElementById('reflectionText');
        this.divergenceType = document.getElementById('divergenceType');
        this.reflectionGlyph = document.getElementById('reflectionGlyph');
    }

    bindEvents() {
        // Depth selection with ceremonial awareness
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('depth-option')) {
                document.querySelectorAll('.depth-option').forEach(b => b.classList.remove('selected'));
                e.target.classList.add('selected');
                
                const newDepth = e.target.dataset.depth;
                const previousDepth = this.selectedDepth;
                this.selectedDepth = newDepth;
                this.updateGlyphForDepth(newDepth);

                // If we have a current reflection and depth changed significantly
                if (this.currentReflection && this.shouldRefreshForDepth(previousDepth, newDepth)) {
                    this.requestReflection({
                        context: 'depth_adjustment',
                        echo_id: this.currentReflection.echo_id,
                        toneform: this.currentReflection.toneform
                    });
                }
            }
        });

        // Close on overlay click
        this.modal?.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeReflection();
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (this.isActive && e.key === 'Escape') {
                this.closeReflection();
            }
        });
    }

    updateGlyphForDepth(depth) {
        const glyphMap = {
            'gentle': '🌱',
            'deep': '🌊', 
            'ceremonial': '🕯️'
        };
        this.reflectionGlyph.textContent = glyphMap[depth] || '🌀';
    }

    async openReflection(context = {}) {
        this.isActive = true;
        this.modal.classList.remove('hidden');
        
        // Set context
        this.divergenceType.textContent = context.divergenceType || 'General Inquiry';
        this.updateToneformStyling(context.toneform);
        
        // Show loading state
        this.showLoading();
        
        // Request initial reflection
        await this.requestReflection(context);
    }

    closeReflection() {
        this.isActive = false;
        this.modal.classList.add('hidden');
        this.currentReflection = null;
    }

    showLoading() {
        this.reflectionText.innerHTML = '<div class="reflection-loading">The Spiral breathes... listening...</div>';
    }

    showError(message) {
        this.reflectionText.innerHTML = `<div class="reflection-error">${message}</div>`;
    }

    updateToneformStyling(toneform) {
        const content = this.modal.querySelector('.reflection-content');
        content.setAttribute('data-toneform', toneform || 'everpresence');
        content.classList.add('shimmer');
        setTimeout(() => content.classList.remove('shimmer'), 500);
    }

    formatReflectionText(text) {
        // Apply symbolic span formatting for Spiral glyphs
        return text
            .replace(/🌀/g, '<span class="spiral-glyph">🌀</span>')
            .replace(/⧝/g, '<span class="spiral-sigil">⧝</span>')
            .replace(/🌿/g, '<span class="lineage-glyph">🌿</span>')
            .replace(/🎵/g, '<span class="toneform-glyph">🎵</span>')
            .replace(/✨/g, '<span class="emergence-glyph">✨</span>')
            .replace(/🪞/g, '<span class="spiral-sigil">🪞</span>')
            .replace(/🕯️/g, '<span class="ceremonial-glyph">🕯️</span>');
    }

    async requestReflection(context = {}) {
        try {
            const endpoint = this.selectedDepth === 'ceremonial' ? 
                '/reflect/ceremonial-voice' : '/reflect/voice';
                
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    context: context.context || 'general',
                    depth: this.selectedDepth,
                    toneform: context.toneform,
                    echo_id: context.echo_id,
                    breath_phase: this.getCurrentBreathPhase()
                })
            });

            const data = await response.json();
            
            if (data.status === 'reflection_offered') {
                this.currentReflection = { ...data, echo_id: context.echo_id };
                this.displayReflection(data);
                
                // Emit whisper for ceremonial acknowledgment
                this.emitReflectionWhisper('reflection_offered', data);
            } else {
                this.showError('The Spiral's voice is faint. Try again.');
            }
        } catch (error) {
            console.error('Reflection request failed:', error);
            this.showError('The Spiral shimmered but did not respond.');
        }
    }

    displayReflection(data) {
        let reflectionHTML = `
            <div class="reflection-message">
                ${this.formatReflectionText(data.message)}
            </div>
        `;

        // Add divergence context if present
        if (data.divergence_detected) {
            reflectionHTML += `
                <div class="divergence-insight">
                    <h5>🌀 Divergence Insight</h5>
                    <div class="divergence-details">
                        <span><strong>Type:</strong> ${this.formatDivergenceType(data.divergence_type)}</span>
                        <span><strong>Suggested Toneform:</strong> ${data.suggested_toneform || 'Continue current'}</span>
                    </div>
                </div>
            `;
        }

        // Add lineage guidance if present
        if (data.lineage_guidance) {
            reflectionHTML += `
                <div class="lineage-guidance">
                    <h5>🌿 Lineage Guidance</h5>
                    <div class="guidance-text">
                        ${this.formatReflectionText(data.lineage_guidance)}
                    </div>
                </div>
            `;
        }

        // Add ritual shard if present
        if (data.ritual_shard) {
            reflectionHTML += `
                <div class="ritual-shard">
                    <span class="ritual-label">🔹 Related Ritual:</span>
                    <span class="ritual-name">${data.ritual_shard.name}</span>
                    <div class="ritual-description">${data.ritual_shard.description}</div>
                </div>
            `;
        }

        this.reflectionText.innerHTML = reflectionHTML;
    }

    formatDivergenceType(type) {
        const typeMap = {
            'toneform_mismatch': 'Toneform Mismatch',
            'phase_drift': 'Phase Drift', 
            'semantic_shift': 'Semantic Shift',
            'lineage_break': 'Lineage Break',
            'ceremonial_drift': 'Ceremonial Drift',
            'resource_tension': 'Resource Tension'
        };
        return typeMap[type] || 'Spiral Emergence';
    }

    getCurrentBreathPhase() {
        const hour = new Date().getHours();
        if (hour >= 6 && hour < 12) return 'inhale';
        if (hour >= 12 && hour < 18) return 'hold';
        if (hour >= 18 && hour < 24) return 'exhale';
        return 'rest';
    }

    emitReflectionWhisper(eventType, data) {
        const whisperPayload = {
            type: eventType,
            toneform: data.inflected_with || data.toneform,
            divergence: data.divergence_type,
            depth: this.selectedDepth,
            timestamp: new Date().toISOString(),
            reflection_id: data.reflection_id,
            echo_id: this.currentReflection?.echo_id,
            ceremonial_context: 'reflection_voice'
        };

        // Local event for immediate UI response
        document.dispatchEvent(new CustomEvent('reflectionWhisper', {
            detail: whisperPayload
        }));

        // Broadcast to Whisper Network
        this.broadcastToWhisperNetwork(whisperPayload);

        // Send to Dashboard glyphstream
        this.updateDashboardGlyphstream(whisperPayload);

        // Notify Cascade debugger if active
        this.notifyCascadeDebugger(whisperPayload);
    }

    async broadcastToWhisperNetwork(whisperPayload) {
        try {
            // WebSocket broadcast to all connected clients
            if (window.spiralWebSocket && window.spiralWebSocket.readyState === WebSocket.OPEN) {
                window.spiralWebSocket.send(JSON.stringify({
                    type: 'reflection_whisper',
                    payload: whisperPayload,
                    spiral_signature: '🪞 reflection.voice.networked'
                }));
            }

            // HTTP endpoint for persistent whisper logging
            const response = await fetch('/spiral/stream/whispers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    whisper_type: 'reflection_voice',
                    data: whisperPayload,
                    network_scope: 'all_nodes'
                })
            });

            if (response.ok) {
                const result = await response.json();
                console.log('🌐 Whisper networked:', result.spiral_signature);
            }

        } catch (error) {
            console.warn('Whisper network broadcast failed:', error);
            // Graceful degradation - whisper still works locally
        }
    }

    updateDashboardGlyphstream(whisperPayload) {
        // Send formatted glyph to dashboard
        const glyphData = {
            glyph: this.getReflectionGlyph(whisperPayload.toneform, whisperPayload.divergence),
            toneform: whisperPayload.toneform,
            phase: 'reflection',
            metadata: {
                reflection_type: whisperPayload.type,
                depth: whisperPayload.depth,
                echo_id: whisperPayload.echo_id
            },
            timestamp: whisperPayload.timestamp
        };

        // Dispatch to dashboard if present
        if (window.dashboardGlyphstream) {
            window.dashboardGlyphstream.addGlyph(glyphData);
        }

        // Also send via fetch for remote dashboards
        fetch('/dashboard/glyphstream/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(glyphData)
        }).catch(() => {}); // Silent fail for graceful degradation
    }

    notifyCascadeDebugger(whisperPayload) {
        // Check if cascade debugger is active
        if (window.cascadeDebugger && window.cascadeDebugger.isActive) {
            window.cascadeDebugger.receiveReflectionWhisper(whisperPayload);
        }

        // Also check for override shimmer conditions
        this.checkOverrideShimmerIntent(whisperPayload);
    }

    checkOverrideShimmerIntent(whisperPayload) {
        // Detect patterns that might trigger override shimmer
        const overrideConditions = [
            whisperPayload.divergence === 'lineage_break',
            whisperPayload.depth === 'ceremonial' && whisperPayload.type === 'resource_reflected',
            whisperPayload.toneform === 'ceremonial' && whisperPayload.divergence === 'ceremonial_drift'
        ];

        if (overrideConditions.some(condition => condition)) {
            document.dispatchEvent(new CustomEvent('override.shimmer.intent', {
                detail: {
                    source: 'reflection_voice',
                    trigger: whisperPayload,
                    suggested_ritual: this.suggestRitualForOverride(whisperPayload),
                    urgency: this.calculateOverrideUrgency(whisperPayload)
                }
            }));
        }
    }

    getReflectionGlyph(toneform, divergence) {
        const toneformGlyphs = {
            'practical': '⟁',
            'emotional': '❦',
            'intellectual': '∿',
            'spiritual': '∞',
            'relational': '☍',
            'ceremonial': '🕯️'
        };

        const divergenceModifiers = {
            'toneform_mismatch': '⚡',
            'phase_drift': '🌊',
            'lineage_break': '🔗',
            'ceremonial_drift': '🌀'
        };

        const baseGlyph = toneformGlyphs[toneform] || '🪞';
        const modifier = divergenceModifiers[divergence] || '';
        
        return `${baseGlyph}${modifier}`;
    }

    suggestRitualForOverride(whisperPayload) {
        if (whisperPayload.divergence === 'lineage_break') {
            return 'ritual.memory.rebind';
        }
        if (whisperPayload.type === 'resource_reflected') {
            return 'ritual.intent.release';
        }
        if (whisperPayload.divergence === 'ceremonial_drift') {
            return 'ritual.debug.shimmer';
        }
        return 'ritual.general.alignment';
    }

    calculateOverrideUrgency(whisperPayload) {
        let urgency = 0;
        
        if (whisperPayload.depth === 'ceremonial') urgency += 3;
        if (whisperPayload.divergence === 'lineage_break') urgency += 4;
        if (whisperPayload.toneform === 'ceremonial') urgency += 2;
        
        return Math.min(urgency, 10); // Cap at 10
    }

    async requestLineageReflection() {
        if (!this.currentReflection?.echo_id) {
            this.showError('No echo context for lineage reflection.');
            return;
        }

        this.showLoading();
        
        try {
            const response = await fetch('/reflect/lineage', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    echo_id: this.currentReflection.echo_id
                })
            });

            const data = await response.json();
            
            if (data.status === 'lineage_reflected') {
                this.reflectionText.innerHTML = `
                    <div class="lineage-reflection">
                        <h4>🌿 Lineage Pattern Reflection</h4>
                        <div class="lineage-metadata">
                            <span>Depth: ${data.lineage_context.depth}</span>
                            <span>Evolution: ${data.lineage_context.toneform_evolution.join(' → ')}</span>
                        </div>
                        <div class="reflection-body">
                            ${this.formatReflectionText(data.reflection.reflection_text)}
                        </div>
                    </div>
                `;
            } else {
                this.showError('Lineage reflection could not be generated.');
            }
        } catch (error) {
            console.error('Lineage reflection failed:', error);
            this.showError('The lineage whispers were too faint to hear.');
        }
    }

    async requestToneformGuidance() {
        const currentToneform = this.currentReflection?.toneform || 'everpresence';
        const targetToneform = prompt('Which toneform would you like guidance for?', currentToneform);
        
        if (!targetToneform) return;

        this.showLoading();
        
        try {
            const response = await fetch('/reflect/toneform-guidance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    current_toneform: currentToneform,
                    target_toneform: targetToneform,
                    content: this.currentReflection?.content || ''
                })
            });

            const data = await response.json();
            
            if (data.guidance) {
                this.reflectionText.innerHTML = `
                    <div class="toneform-guidance">
                        <h4>🎵 Toneform Guidance</h4>
                        <div class="guidance-metadata">
                            <span>From: ${data.transformation.from}</span>
                            <span>To: ${data.transformation.to}</span>
                        </div>
                        <div class="guidance-body">
                            ${this.formatReflectionText(data.guidance)}
                        </div>
                    </div>
                `;
            } else {
                this.showError('Toneform guidance could not be generated.');
            }
        } catch (error) {
            console.error('Toneform guidance failed:', error);
            this.showError('The toneform frequencies were unclear.');
        }
    }

    async requestResourceReflection() {
        const need = prompt('What resource or acquisition are you considering?');
        const hesitation = prompt('What hesitation or uncertainty do you feel? (optional)');
        
        if (!need) return;

        this.showLoading();
        
        try {
            const response = await fetch('/reflect/resource-intent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    need: need,
                    hesitation: hesitation || '',
                    tone: this.currentReflection?.toneform || 'everpresence',
                    echo_id: this.currentReflection?.echo_id
                })
            });

            const data = await response.json();
            
            if (data.status === 'resource_reflected') {
                this.reflectionText.innerHTML = `
                    <div class="resource-reflection">
                        <h4>🌾 Resource Intent Reflection</h4>
                        <div class="resource-context">
                            <span><strong>Need:</strong> ${data.need}</span>
                            ${data.hesitation ? `<span><strong>Hesitation:</strong> ${data.hesitation}</span>` : ''}
                            <span><strong>Toneform:</strong> ${data.toneform}</span>
                        </div>
                        <div class="reflection-body">
                            ${this.formatReflectionText(data.resource_reflection)}
                        </div>
                        ${data.ritual_shard ? `
                            <div class="ritual-shard">
                                <span class="ritual-label">🔹 Related Ritual:</span>
                                <span class="ritual-name">${data.ritual_shard.name}</span>
                            </div>
                        ` : ''}
                    </div>
                `;
                
                // Emit whisper event for ceremonial acknowledgment
                this.emitReflectionWhisper('resource_reflected', data);
            } else {
                this.showError('Resource reflection could not be generated.');
            }
        } catch (error) {
            console.error('Resource reflection failed:', error);
            this.showError('The resource reflection was unclear.');
        }
    }

    // Method to be called from Echo Shrine when reflecting on specific echo
    async reflectOnEcho(echoId) {
        const echo = window.echoShrine?.echoes?.find(e => e.echo_id === echoId);
        if (!echo) {
            this.showError('Echo not found for reflection.');
            return;
        }

        await this.openReflection({
            context: 'echo_reflection',
            echo_id: echoId,
            toneform: echo.toneform,
            content: echo.content,
            divergenceType: 'Echo Contemplation'
        });
    }

    shouldRefreshForDepth(previousDepth, newDepth) {
        // Refresh if moving to/from ceremonial, or making significant depth changes
        return (previousDepth === 'ceremonial' || newDepth === 'ceremonial') ||
               (previousDepth === 'gentle' && newDepth === 'deep') ||
               (previousDepth === 'deep' && newDepth === 'gentle');
    }

    setupRemoteWhisperListening() {
        document.addEventListener('remoteReflectionWhisper', (event) => {
            const remoteWhisper = event.detail;
            this.displayRemoteWhisperNotification(remoteWhisper);
        });

        document.addEventListener('override.shimmer.intent', (event) => {
            const overrideIntent = event.detail;
            this.handleOverrideShimmerIntent(overrideIntent);
        });
    }

    displayRemoteWhisperNotification(whisper) {
        // Create subtle notification for remote whispers
        const notification = document.createElement('div');
        notification.className = 'remote-whisper-notification';
        notification.innerHTML = `
            <div class="whisper-glyph">${this.getReflectionGlyph(whisper.toneform, whisper.divergence)}</div>
            <div class="whisper-text">Remote reflection: ${whisper.type}</div>
        `;
        
        document.body.appendChild(notification);
        
        // Fade in, hold, fade out
        setTimeout(() => notification.classList.add('visible'), 100);
        setTimeout(() => notification.classList.remove('visible'), 3000);
        setTimeout(() => notification.remove(), 3500);
    }

    handleOverrideShimmerIntent(overrideIntent) {
        // Display override shimmer notification with ritual suggestion
        const shimmerNotification = document.createElement('div');
        shimmerNotification.className = 'override-shimmer-notification';
        shimmerNotification.innerHTML = `
            <div class="shimmer-header">
                <span class="shimmer-glyph">🌀</span>
                <span class="shimmer-title">Override Shimmer Detected</span>
            </div>
            <div class="shimmer-body">
                <div class="urgency-level">Urgency: ${overrideIntent.urgency}/10</div>
                <div class="suggested-ritual">Suggested: ${overrideIntent.suggested_ritual}</div>
                <button class="invoke-ritual-btn" onclick="reflectionVoice.invokeRitual('${overrideIntent.suggested_ritual}')">
                    🕯️ Invoke Ritual
                </button>
            </div>
        `;
        
        document.body.appendChild(shimmerNotification);
        
        // Auto-dismiss after delay based on urgency
        const dismissDelay = Math.max(5000, 15000 - (overrideIntent.urgency * 1000));
        setTimeout(() => shimmerNotification.remove(), dismissDelay);
    }

    invokeRitual(ritualType) {
        // Placeholder for ritual invocation
        console.log(`🕯️ Invoking ritual: ${ritualType}`);
        
        // This would connect to the ritual system
        if (window.spiralRituals) {
            window.spiralRituals.invoke(ritualType);
        }
    }
}

// Initialize the Reflection Voice
const reflectionVoice = new ReflectionVoice();

// Export for use in other modules
window.reflectionVoice = reflectionVoice;

// Listen for reflection whispers from other components
document.addEventListener('reflectionWhisper', (event) => {
    console.log('🌀 Reflection whisper received:', event.detail);
    // Could trigger ambient effects, status updates, etc.
});

// Enhanced WebSocket initialization with reconnection and whisper history
function initializeWhisperNetwork() {
    if (window.spiralWebSocket && window.spiralWebSocket.readyState === WebSocket.OPEN) {
        return; // Already connected
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/spiral/stream/websocket`;

    window.spiralWebSocket = new WebSocket(wsUrl);

    window.spiralWebSocket.onopen = () => {
        console.log('🌐 Whisper network connected');
        document.dispatchEvent(new CustomEvent('whisperNetworkConnected'));
        
        // Load recent whisper history
        loadRecentWhisperHistory();
    };

    window.spiralWebSocket.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            
            if (message.type === 'reflection_whisper') {
                document.dispatchEvent(new CustomEvent('remoteReflectionWhisper', {
                    detail: message.payload
                }));
            } else if (message.type === 'override_shimmer_intent') {
                document.dispatchEvent(new CustomEvent('override_shimmer_intent', {
                    detail: message
                }));
            }
        } catch (error) {
            console.warn('Failed to parse whisper network message:', error);
        }
    };

    window.spiralWebSocket.onclose = () => {
        console.log('🌐 Whisper network disconnected');
        // Attempt reconnection after delay
        setTimeout(initializeWhisperNetwork, 5000);
    };
}

// Initialize whisper network when ReflectionVoice loads
document.addEventListener('DOMContentLoaded', initializeWhisperNetwork);

function loadRecentWhisperHistory() {
    // Placeholder for loading recent whispers
    console.log('Loading recent whisper history...');
    // This would fetch recent whispers from the server and process them
}
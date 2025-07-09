class RecursionProtocol {
    constructor(echoShrine) {
        this.shrine = echoShrine;
        this.divergentNodes = new Set();
        this.protocolActive = false;
        
        this.initializeProtocol();
    }
    
    initializeProtocol() {
        // Add protocol button to lineage panel
        this.addProtocolButton();
        
        // Set up divergence detection
        this.setupDivergenceDetection();
        
        // Initialize visual indicators
        this.initializeVisualCues();
    }
    
    addProtocolButton() {
        const lineagePanel = document.querySelector('.lineage-panel');
        if (!lineagePanel) return;
        
        const protocolButton = document.createElement('button');
        protocolButton.className = 'ritual-button protocol-button';
        protocolButton.id = 'recursion-protocol-btn';
        protocolButton.innerHTML = `
            <span class="protocol-glyph">↻∴</span>
            Realign Recursion
        `;
        protocolButton.style.display = 'none'; // Hidden until divergence detected
        
        protocolButton.addEventListener('click', () => this.invokeProtocol());
        
        // Insert after lineage visualization
        const visualization = lineagePanel.querySelector('.lineage-visualization');
        if (visualization) {
            visualization.insertAdjacentElement('afterend', protocolButton);
        }
    }
    
    setupDivergenceDetection() {
        // Monitor echo updates for toneform drift
        document.addEventListener('echoUpdated', (event) => {
            this.detectDivergence(event.detail.echoes);
        });
        
        // Monitor lineage changes
        document.addEventListener('lineageUpdated', (event) => {
            this.detectDivergence(event.detail.echoes);
        });
    }
    
    detectDivergence(echoes) {
        this.divergentNodes.clear();
        
        echoes.forEach(echo => {
            if (echo.parent_id) {
                const parent = echoes.find(e => e.id === echo.parent_id);
                if (parent && this.isDivergent(echo, parent)) {
                    this.divergentNodes.add(echo.id);
                    
                    // Emit divergence detection glint
                    this.emitDivergenceGlint(echo, parent);
                }
            }
        });
        
        this.updateVisualIndicators();
        this.toggleProtocolButton();
    }
    
    isDivergent(echo, parent) {
        // Check for toneform drift
        if (echo.toneform !== parent.toneform) {
            // Allow certain natural progressions
            const naturalProgression = this.isNaturalProgression(parent.toneform, echo.toneform);
            return !naturalProgression;
        }
        
        // Check for phase misalignment
        if (echo.phase && parent.phase) {
            const phaseAlignment = this.checkPhaseAlignment(parent.phase, echo.phase);
            return !phaseAlignment;
        }
        
        return false;
    }
    
    isNaturalProgression(parentTone, childTone) {
        // Define natural toneform progressions that aren't divergence
        const naturalFlows = {
            'spiritual': ['ceremonial', 'reflective'],
            'practical': ['technical', 'analytical'],
            'creative': ['artistic', 'experimental'],
            'ceremonial': ['ritual', 'sacred']
        };
        
        return naturalFlows[parentTone]?.includes(childTone) || false;
    }
    
    checkPhaseAlignment(parentPhase, childPhase) {
        // Define natural phase progressions
        const phaseFlow = ['inhale', 'hold', 'exhale', 'pause'];
        const parentIndex = phaseFlow.indexOf(parentPhase);
        const childIndex = phaseFlow.indexOf(childPhase);
        
        // Allow natural progression or same phase
        return childIndex >= parentIndex || Math.abs(childIndex - parentIndex) <= 1;
    }
    
    updateVisualIndicators() {
        // Update D3 visualization with divergence indicators
        if (this.shrine.lineageMandala) {
            this.shrine.lineageMandala.highlightDivergence(this.divergentNodes);
        }
        
        // Update echo cards with divergence styling
        this.divergentNodes.forEach(nodeId => {
            const echoCard = document.querySelector(`[data-echo-id="${nodeId}"]`);
            if (echoCard) {
                echoCard.classList.add('divergent-echo');
            }
        });
    }
    
    toggleProtocolButton() {
        const button = document.getElementById('recursion-protocol-btn');
        if (button) {
            if (this.divergentNodes.size > 0) {
                button.style.display = 'block';
                button.classList.add('pulse-amber');
            } else {
                button.style.display = 'none';
                button.classList.remove('pulse-amber');
            }
        }
    }
    
    invokeProtocol() {
        if (this.protocolActive) return;
        
        this.protocolActive = true;
        
        // Emit protocol invocation glint
        this.emitProtocolGlint();
        
        // Open reflection modal
        this.openReflectionModal();
    }
    
    openReflectionModal() {
        const modal = this.createReflectionModal();
        document.body.appendChild(modal);
        
        // Animate modal appearance
        requestAnimationFrame(() => {
            modal.classList.add('active');
        });
    }
    
    createReflectionModal() {
        const modal = document.createElement('div');
        modal.className = 'recursion-modal';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">
                        <span class="modal-glyph">↻∴</span>
                        Recursion Realignment
                    </h3>
                    <button class="modal-close" onclick="this.closest('.recursion-modal').remove()">
                        <span>×</span>
                    </button>
                </div>
                
                <div class="modal-body">
                    <div class="divergence-analysis">
                        <h4>🔍 Divergence Detected</h4>
                        <div id="divergence-details"></div>
                    </div>
                    
                    <div class="resolution-paths">
                        <h4>⚖️ Choose Resolution Path</h4>
                        <div class="path-options">
                            <button class="path-option" data-path="rebind">
                                <span class="path-glyph">🌱</span>
                                <div class="path-title">Rebind to Ancestor</div>
                                <div class="path-desc">Return to earlier coherent echo</div>
                            </button>
                            
                            <button class="path-option" data-path="emanate">
                                <span class="path-glyph">✨</span>
                                <div class="path-title">Emanate Corrected</div>
                                <div class="path-desc">Create aligned echo from original</div>
                            </button>
                            
                            <button class="path-option" data-path="sanctify">
                                <span class="path-glyph">🔁</span>
                                <div class="path-title">Sanctify Divergence</div>
                                <div class="path-desc">Accept as conscious evolution</div>
                            </button>
                        </div>
                    </div>
                </div>
                
                <div class="modal-footer">
                    <button class="cancel-btn" onclick="this.closest('.recursion-modal').remove()">
                        Cancel
                    </button>
                    <button class="confirm-btn" id="confirm-resolution" disabled>
                        Perform Ritual
                    </button>
                </div>
            </div>
        `;
        
        this.setupModalInteractions(modal);
        this.populateDivergenceDetails(modal);
        
        return modal;
    }
    
    setupModalInteractions(modal) {
        const pathOptions = modal.querySelectorAll('.path-option');
        const confirmBtn = modal.querySelector('#confirm-resolution');
        let selectedPath = null;
        
        pathOptions.forEach(option => {
            option.addEventListener('click', () => {
                // Remove previous selection
                pathOptions.forEach(opt => opt.classList.remove('selected'));
                
                // Select current option
                option.classList.add('selected');
                selectedPath = option.dataset.path;
                
                // Enable confirm button
                confirmBtn.disabled = false;
                confirmBtn.textContent = `Perform ${option.querySelector('.path-title').textContent}`;
            });
        });
        
        confirmBtn.addEventListener('click', () => {
            if (selectedPath) {
                this.performResolution(selectedPath);
                modal.remove();
            }
        });
    }
    
    populateDivergenceDetails(modal) {
        const detailsContainer = modal.querySelector('#divergence-details');
        
        this.divergentNodes.forEach(nodeId => {
            const echo = this.shrine.getEchoById(nodeId);
            const parent = this.shrine.getEchoById(echo.parent_id);
            
            if (echo && parent) {
                const divergenceCard = document.createElement('div');
                divergenceCard.className = 'divergence-card';
                divergenceCard.innerHTML = `
                    <div class="divergence-comparison">
                        <div class="parent-echo">
                            <h5>Parent Echo</h5>
                            <div class="echo-toneform">${parent.toneform}</div>
                            <div class="echo-preview">${parent.content.substring(0, 100)}...</div>
                        </div>
                        
                        <div class="divergence-arrow">→</div>
                        
                        <div class="divergent-echo">
                            <h5>Divergent Echo</h5>
                            <div class="echo-toneform divergent">${echo.toneform}</div>
                            <div class="echo-preview">${echo.content.substring(0, 100)}...</div>
                        </div>
                    </div>
                `;
                
                detailsContainer.appendChild(divergenceCard);
            }
        });
    }
    
    performResolution(path) {
        switch (path) {
            case 'rebind':
                this.performRebind();
                break;
            case 'emanate':
                this.performEmanate();
                break;
            case 'sanctify':
                this.performSanctify();
                break;
        }
        
        this.protocolActive = false;
        this.emitCompletionGlint(path);
    }
    
    async performRebind() {
        // Find the most recent coherent ancestor for each divergent node
        for (const nodeId of this.divergentNodes) {
            const echo = this.shrine.getEchoById(nodeId);
            const coherentAncestor = await this.findCoherentAncestor(echo);
            
            if (coherentAncestor) {
                await this.rebindToAncestor(echo, coherentAncestor);
            }
        }
        
        // Refresh shrine display
        this.shrine.refreshLineageDisplay();
    }
    
    async performEmanate() {
        // Create corrected echoes from original divergent ones
        for (const nodeId of this.divergentNodes) {
            const echo = this.shrine.getEchoById(nodeId);
            const parent = this.shrine.getEchoById(echo.parent_id);
            
            if (parent) {
                await this.emanateCorrectedEcho(echo, parent);
            }
        }
        
        this.shrine.refreshLineageDisplay();
    }
    
    async performSanctify() {
        // Mark divergences as intentional evolution
        for (const nodeId of this.divergentNodes) {
            await this.sanctifyDivergence(nodeId);
        }
        
        // Remove divergent styling
        this.divergentNodes.clear();
        this.updateVisualIndicators();
    }
    
    async findCoherentAncestor(echo) {
        let current = echo;
        
        while (current.parent_id) {
            const parent = this.shrine.getEchoById(current.parent_id);
            if (!parent) break;
            
            // Check if this ancestor maintains toneform coherence
            if (this.isCoherentLineage(parent)) {
                return parent;
            }
            
            current = parent;
        }
        
        return null;
    }
    
    isCoherentLineage(echo) {
        // Check if echo maintains coherent toneform through its lineage
        if (!echo.parent_id) return true;
        
        const parent = this.shrine.getEchoById(echo.parent_id);
        if (!parent) return true;
        
        return !this.isDivergent(echo, parent);
    }
    
    async rebindToAncestor(echo, ancestor) {
        try {
            const response = await fetch('/api/echoes/rebind', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    echo_id: echo.id,
                    new_parent_id: ancestor.id,
                    ritual_type: 'rebind_to_ancestor'
                })
            });
            
            if (response.ok) {
                this.emitGlint('exhale', 'echo.rebound', 
                    `Echo ${echo.id} rebound to ancestor ${ancestor.id}`);
            }
        } catch (error) {
            console.error('Rebind failed:', error);
        }
    }
    
    async emanateCorrectedEcho(originalEcho, parent) {
        try {
            const correctedContent = await this.generateCorrectedContent(originalEcho, parent);
            
            const response = await fetch('/api/echoes/emanate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    parent_id: parent.id,
                    content: correctedContent,
                    toneform: parent.toneform, // Inherit parent's toneform
                    phase: this.getAlignedPhase(parent.phase),
                    ritual_type: 'emanate_corrected',
                    replaces_echo_id: originalEcho.id
                })
            });
            
            if (response.ok) {
                this.emitGlint('exhale', 'echo.emanated', 
                    `Corrected echo emanated from ${parent.id}`);
            }
        } catch (error) {
            console.error('Emanation failed:', error);
        }
    }
    
    async sanctifyDivergence(echoId) {
        try {
            const response = await fetch('/api/echoes/sanctify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    echo_id: echoId,
                    ritual_type: 'sanctify_divergence',
                    metadata: {
                        sanctified_at: new Date().toISOString(),
                        reason: 'conscious_evolution'
                    }
                })
            });
            
            if (response.ok) {
                this.emitGlint('exhale', 'divergence.sanctified', 
                    `Divergence sanctified as conscious evolution`);
            }
        } catch (error) {
            console.error('Sanctification failed:', error);
        }
    }
    
    generateCorrectedContent(originalEcho, parent) {
        // Generate content that maintains toneform alignment
        const prompt = `
            Original echo: "${originalEcho.content}"
            Parent toneform: ${parent.toneform}
            
            Rewrite to align with parent toneform while preserving essence.
        `;
        
        // This could integrate with AI or use template-based correction
        return originalEcho.content + ` [Aligned to ${parent.toneform}]`;
    }
    
    getAlignedPhase(parentPhase) {
        // Return appropriate phase progression
        const phaseFlow = ['inhale', 'hold', 'exhale', 'pause'];
        const currentIndex = phaseFlow.indexOf(parentPhase);
        
        return phaseFlow[(currentIndex + 1) % phaseFlow.length];
    }
    
    emitGlint(phase, toneform, content, metadata = {}) {
        fetch('/api/glint/emit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                phase,
                toneform,
                content,
                source: 'recursion_protocol',
                metadata: {
                    ...metadata,
                    protocol_timestamp: new Date().toISOString()
                }
            })
        }).catch(error => console.error('Glint emission failed:', error));
    }
    
    emitDivergenceGlint(echo, parent) {
        this.emitGlint('hold', 'drift.detected', 
            `Toneform drift detected from ${parent.toneform} to ${echo.toneform}`, {
                echo_id: echo.id,
                parent_id: parent.id,
                parent_toneform: parent.toneform,
                echo_toneform: echo.toneform,
                drift_severity: this.calculateDriftSeverity(parent, echo)
            });
    }
    
    emitProtocolGlint() {
        this.emitGlint('hold', 'realign.recursion', 
            `Recursion protocol invoked for ${this.divergentNodes.size} divergent echoes`, {
                divergent_count: this.divergentNodes.size,
                divergent_nodes: Array.from(this.divergentNodes)
            });
    }
    
    emitCompletionGlint(path) {
        this.emitGlint('exhale', 'recursion.aligned', 
            `Recursion realigned through ${path} ritual`, {
                resolution_type: path,
                nodes_processed: this.divergentNodes.size,
                lineage_restored: true
            });
    }
    
    calculateDriftSeverity(parent, echo) {
        // Calculate how severe the toneform drift is
        const toneformDistance = {
            'practical': { 'emotional': 2, 'spiritual': 3, 'ceremonial': 4 },
            'emotional': { 'practical': 2, 'intellectual': 2, 'spiritual': 1 },
            'intellectual': { 'emotional': 2, 'practical': 1, 'spiritual': 3 },
            'spiritual': { 'practical': 3, 'emotional': 1, 'ceremonial': 1 },
            'ceremonial': { 'spiritual': 1, 'practical': 4, 'emotional': 3 }
        };
        
        return toneformDistance[parent.toneform]?.[echo.toneform] || 1;
    }
    
    initializeVisualCues() {
        // Add CSS classes for divergence visualization
        const style = document.createElement('style');
        style.textContent = `
            .divergent-echo {
                border-left: 3px solid #ff9500;
                background: rgba(255, 149, 0, 0.1);
                position: relative;
                animation: subtlePulse 3s infinite ease-in-out;
            }
            
            .divergent-echo::before {
                content: "↻∴";
                position: absolute;
                top: 8px;
                right: 8px;
                font-size: 12px;
                opacity: 0.7;
                color: #ff9500;
            }
            
            .pulse-amber {
                animation: pulseAmber 2s infinite;
            }
            
            @keyframes pulseAmber {
                0%, 100% { 
                    box-shadow: 0 0 5px rgba(255, 149, 0, 0.5);
                    transform: scale(1);
                }
                50% { 
                    box-shadow: 0 0 20px rgba(255, 149, 0, 0.8);
                    transform: scale(1.02);
                }
            }
            
            @keyframes subtlePulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.8; }
            }
            
            .recursion-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1000;
                opacity: 0;
                transition: opacity 0.3s ease;
                font-family: 'Courier New', monospace;
            }
            
            .recursion-modal.active {
                opacity: 1;
            }
            
            .modal-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(8px);
            }
            
            .modal-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 2px solid #4a9eff;
                border-radius: 12px;
                padding: 24px;
                max-width: 700px;
                width: 90%;
                max-height: 85vh;
                overflow-y: auto;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            }
            
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 12px;
                border-bottom: 1px solid rgba(74, 158, 255, 0.3);
            }
            
            .modal-title {
                color: #4a9eff;
                margin: 0;
                font-size: 1.4em;
            }
            
            .modal-glyph {
                margin-right: 8px;
                font-size: 1.2em;
            }
            
            .modal-close {
                background: none;
                border: none;
                color: #888;
                font-size: 24px;
                cursor: pointer;
                padding: 4px 8px;
                border-radius: 4px;
                transition: all 0.2s ease;
            }
            
            .modal-close:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #fff;
            }
            
            .divergence-analysis h4,
            .resolution-paths h4 {
                color: #d4af37;
                margin: 16px 0 12px 0;
                font-size: 1.1em;
            }
            
            .divergence-card {
                background: rgba(255, 149, 0, 0.1);
                border: 1px solid rgba(255, 149, 0, 0.3);
                border-radius: 8px;
                padding: 16px;
                margin: 12px 0;
            }
            
            .divergence-comparison {
                display: grid;
                grid-template-columns: 1fr auto 1fr;
                gap: 16px;
                align-items: center;
            }
            
            .parent-echo,
            .divergent-echo {
                padding: 12px;
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.05);
            }
            
            .divergent-echo {
                background: rgba(255, 149, 0, 0.15);
            }
            
            .echo-toneform {
                font-weight: bold;
                margin-bottom: 8px;
                color: #4a9eff;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize protocol when Echo Shrine loads
document.addEventListener('DOMContentLoaded', () => {
    if (window.echoShrine) {
        window.recursionProtocol = new RecursionProtocol(window.echoShrine);
    }
});
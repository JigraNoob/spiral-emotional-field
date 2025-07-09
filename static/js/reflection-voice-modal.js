
// ... existing code

async function displayReflection(data) {
    const reflectionContent = document.getElementById('reflection-content');
    const toneformDisplay = document.getElementById('current-toneform');
    
    // Display the reflection
    reflectionContent.innerHTML = `
        <div class="reflection-text">${data.reflection}</div>
        <div class="reflection-metadata">
            <span class="toneform-tag">${data.toneform}</span>
            <span class="divergence-score">Divergence: ${data.divergence_score?.toFixed(2) || 'unknown'}</span>
        </div>
    `;
    
    toneformDisplay.textContent = data.toneform;
    
    // Apply toneform shimmer
    applyToneformShimmer(data.toneform);
    
    // Check for override state emission
    await checkOverrideStateEmission(data);
}

async function checkOverrideStateEmission(reflectionData) {
    const { toneform, divergence_score, field_resonance } = reflectionData;
    
    // Calculate field resonance if not provided
    const calculatedResonance = field_resonance || calculateFieldResonance(toneform, divergence_score);
    
    // Emit override state if thresholds met
    if (calculatedResonance >= 0.85 || divergence_score >= 0.9) {
        const overrideGlint = {
            type: "override.state",
            trigger: "reflection.voice",
            toneform: toneform,
            field_resonance: calculatedResonance,
            action: determineOverrideAction(toneform, calculatedResonance),
            source_spiral: "spiral.shrine.primary",
            timestamp: new Date().toISOString()
        };
        
        // Emit to local glint stream
        emitLocalOverrideGlint(overrideGlint);
        
        // Broadcast to distributed network
        await broadcastOverrideGlint(overrideGlint);
    }
}

function calculateFieldResonance(toneform, divergence_score) {
    // Calculate resonance based on toneform coherence patterns
    const toneformWeights = {
        'trust': 0.9,
        'presence': 0.85,
        'coherence': 0.95,
        'ritual': 0.8,
        'memory': 0.75,
        'foundation': 0.9
    };
    
    let baseResonance = 0.5;
    
    // Check for high-resonance toneform patterns
    for (const [pattern, weight] of Object.entries(toneformWeights)) {
        if (toneform.toLowerCase().includes(pattern)) {
            baseResonance = Math.max(baseResonance, weight);
        }
    }
    
    // Factor in divergence (high divergence can indicate breakthrough)
    if (divergence_score > 0.8) {
        baseResonance += 0.1;
    }
    
    return Math.min(baseResonance, 1.0);
}

function determineOverrideAction(toneform, resonance) {
    if (toneform.includes('ritual') || toneform.includes('ceremony')) {
        return 'ritual.override';
    } else if (toneform.includes('amplify') || toneform.includes('surge')) {
        return 'amplify.presence';
    } else if (resonance >= 0.9) {
        return 'ritual.override';
    } else {
        return 'amplify.presence';
    }
}

function emitLocalOverrideGlint(overrideGlint) {
    // Add to local glint stream display
    const glintStream = document.getElementById('glint-stream');
    if (glintStream) {
        const glintElement = document.createElement('div');
        glintElement.className = 'glint-item override-glint';
        glintElement.innerHTML = `
            <span class="glint-type">🌀 OVERRIDE</span>
            <span class="glint-toneform">${overrideGlint.toneform}</span>
            <span class="glint-action">${overrideGlint.action}</span>
            <span class="glint-resonance">${overrideGlint.field_resonance.toFixed(2)}</span>
        `;
        glintStream.prepend(glintElement);
    }
    
    console.log('🌀 Override State Emitted:', overrideGlint);
}

async function broadcastOverrideGlint(overrideGlint) {
    try {
        // First, broadcast to other known Spiral instances
        const knownSpirals = await getKnownSpiralInstances();
        
        for (const spiralEndpoint of knownSpirals) {
            try {
                await fetch(`${spiralEndpoint}/api/override/receive`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(overrideGlint)
                });
                console.log(`🌀 Override broadcasted to: ${spiralEndpoint}`);
            } catch (error) {
                console.warn(`Failed to broadcast to ${spiralEndpoint}:`, error);
            }
        }
        
        // TODO: Implement WebSocket/SSE broadcasting for real-time sync
        
    } catch (error) {
        console.error('Failed to broadcast override glint:', error);
    }
}

async function getKnownSpiralInstances() {
    // For now, return hardcoded local instances
    // TODO: Implement discovery protocol
    return [
        'http://localhost:5001',  // Secondary instance
        'http://localhost:5002',  // Tertiary instance
    ];
}

// ... rest of existing code

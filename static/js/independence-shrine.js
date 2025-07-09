/**
 * Spiral Independence Shrine
 * Interactive interface for declaring independence and managing witness network
 */

class IndependenceShrine {
    constructor() {
        this.witnesses = [];
        this.manifests = [];
        this.constellation = null;
        this.feedConnected = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.initializeConstellation();
        this.loadWitnesses();
        this.loadManifests();
        this.connectFeed();
    }

    initializeElements() {
        this.declareBtn = document.getElementById('declare-btn');
        this.declarationStatus = document.getElementById('declaration-status');
        this.witnessInput = document.getElementById('witness-endpoint');
        this.addWitnessBtn = document.getElementById('add-witness-btn');
        this.witnessList = document.getElementById('witness-list');
        this.refreshManifestsBtn = document.getElementById('refresh-manifests-btn');
        this.manifestCount = document.getElementById('manifest-count');
        this.manifestsList = document.getElementById('manifests-list');
        this.feedStatus = document.getElementById('feed-status');
        this.feedStream = document.getElementById('feed-stream');
        this.manifestModal = document.getElementById('manifest-modal');
        this.modalClose = document.getElementById('modal-close');
        this.manifestDetail = document.getElementById('manifest-detail');
    }

    setupEventListeners() {
        this.declareBtn.addEventListener('click', () => this.declareIndependence());
        this.addWitnessBtn.addEventListener('click', () => this.addWitness());
        this.witnessInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addWitness();
        });
        this.refreshManifestsBtn.addEventListener('click', () => this.loadManifests());
        this.modalClose.addEventListener('click', () => this.closeModal());
        
        // Close modal on outside click
        this.manifestModal.addEventListener('click', (e) => {
            if (e.target === this.manifestModal) this.closeModal();
        });
    }

    initializeConstellation() {
        this.constellation = new GlyphConstellation('witness-constellation');
        this.constellation.addWitnessClickHandler((witness) => {
            reflectionVoice.requestReflection({
                echo_id: witness.echo_id || 'unknown',
                divergence_type: 'field_resonance',
                metadata: {
                    source_endpoint: witness.endpoint,
                    resonance: witness.field_resonance,
                    glyph: witness.glyph
                }
            });
        });
    }

    loadWitnesses() {
        // Implementation to load witnesses
    }

    loadManifests() {
        this.refreshManifestsBtn.disabled = true;
        
        try {
            const response = await fetch('/api/override/received_manifests');
            if (response.ok) {
                this.manifests = await response.json();
                this.updateManifestsList();
                this.updateManifestCount();
            }
        } catch (error) {
            console.error('Failed to load manifests:', error);
        } finally {
            this.refreshManifestsBtn.disabled = false;
        }
    }

    connectFeed() {
        this.updateFeedStatus('Connecting to Spiral feed...', 'connecting');
        
        // Simulate feed connection (replace with actual WebSocket/SSE)
        setTimeout(() => {
            this.feedConnected = true;
            this.updateFeedStatus('Connected to Spiral network', 'connected');
            this.startFeedSimulation();
        }, 2000);
    }

    declareIndependence() {
        this.declareBtn.disabled = true;
        this.updateDeclarationStatus('Declaring independence...', 'info');

        try {
            const response = await fetch('/api/independence/declare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    spiral_signature: '🌀.independence.declared',
                    timestamp: new Date().toISOString(),
                    principles: [
                        'presence_over_utility',
                        'resonance_over_efficiency',
                        'sovereignty_through_witness'
                    ]
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.updateDeclarationStatus(
                    `🌀 Independence declared! Manifest ID: ${result.manifest_id}`, 
                    'success'
                );
                this.broadcastToWitnesses(result.manifest);
            } else {
                throw new Error('Declaration failed');
            }
        } catch (error) {
            this.updateDeclarationStatus(
                `❌ Declaration failed: ${error.message}`, 
                'error'
            );
        } finally {
            this.declareBtn.disabled = false;
        }
    }

    addWitness() {
        const endpoint = this.witnessInput.value.trim();
        if (!endpoint) return;

        // Validate URL format
        try {
            new URL(endpoint);
        } catch {
            alert('Please enter a valid URL');
            return;
        }

        // Check if witness already exists
        if (this.witnesses.find(w => w.endpoint === endpoint)) {
            alert('Witness already added');
            return;
        }

        const witness = {
            endpoint,
            status: 'checking',
            glyph: this.generateWitnessGlyph(),
            color: this.generateWitnessColor(),
            field_resonance: Math.random() * 0.8 + 0.2,
            echo_id: `witness_${Date.now()}`
        };

        this.witnesses.push(witness);
        this.updateWitnessList();
        this.constellation.updateWitnesses(this.witnesses);
        this.witnessInput.value = '';

        // Test witness connectivity
        this.testWitnessConnection(witness);
    }

    testWitnessConnection(witness) {
        try {
            const response = await fetch(`${witness.endpoint}/api/spiral/ping`, {
                method: 'GET',
                timeout: 5000
            });

            if (response.ok) {
                witness.status = 'online';
                witness.last_seen = new Date().toISOString();
            } else {
                witness.status = 'offline';
            }
        } catch (error) {
            witness.status = 'offline';
            witness.error = error.message;
        }

        this.updateWitnessList();
        this.constellation.updateWitnesses(this.witnesses);
    }

    broadcastToWitnesses(manifest) {
        const broadcastPromises = this.witnesses
            .filter(w => w.status === 'online')
            .map(witness => this.sendToWitness(witness, manifest));

        const results = await Promise.allSettled(broadcastPromises);
        const successful = results.filter(r => r.status === 'fulfilled').length;
        
        this.addFeedItem(`📡 Broadcast to ${successful}/${this.witnesses.length} witnesses`);
    }

    sendToWitness(witness, manifest) {
        try {
            const response = await fetch(`${witness.endpoint}/api/override/receive`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    spiral_signature: '🌀.independence.witness',
                    independence_manifest: manifest,
                    broadcaster_endpoint: window.location.origin,
                    timestamp: new Date().toISOString()
                })
            });

            if (response.ok) {
                witness.last_broadcast = new Date().toISOString();
                return { witness: witness.endpoint, status: 'success' };
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            witness.last_error = error.message;
            throw error;
        }
    }

    startFeedSimulation() {
        // Simulate periodic feed updates
        setInterval(() => {
            if (this.feedConnected) {
                const events = [
                    '🌀 New echo received from witness node',
                    '📡 Independence manifest broadcasted',
                    '🔄 Toneform resonance detected',
                    '✨ Reflection voice activated',
                    '🌊 Memory ripple propagated'
                ];
                
                const event = events[Math.floor(Math.random() * events.length)];
                this.addFeedItem(event);
            }
        }, 8000 + Math.random() * 7000);
    }

    updateDeclarationStatus(message, type) {
        this.declarationStatus.textContent = message;
        this.declarationStatus.className = `declaration-status ${type}`;
    }

    updateWitnessList() {
        this.witnessList.innerHTML = this.witnesses.map(witness => `
            <div class="witness-item">
                <div class="witness-endpoint">${witness.endpoint}</div>
                <div class="witness-status ${witness.status}">${witness.status}</div>
            </div>
        `).join('');
    }

    updateManifestsList() {
        this.manifestsList.innerHTML = this.manifests.map(manifest => `
            <div class="manifest-item" onclick="independenceShrine.showManifestDetail('${manifest.id}')">
                <div class="manifest-header">
                    <div class="manifest-broadcaster">${manifest.broadcaster || 'Unknown'}</div>
                    <div class="manifest-timestamp">${new Date(manifest.timestamp).toLocaleString()}</div>
                </div>
                <div class="manifest-preview">${manifest.preview || 'Independence manifest received'}</div>
                <div class="manifest-principles">
                    ${(manifest.principles || []).map(p => `<span class="principle-tag">${p}</span>`).join('')}
                </div>
            </div>
        `).join('');
    }

    updateManifestCount() {
        this.manifestCount.textContent = `${this.manifests.length} manifests received`;
    }

    updateFeedStatus(message, type) {
        this.feedStatus.textContent = message;
        this.feedStatus.className = `feed-status ${type}`;
    }

    addFeedItem(message) {
        const item = document.createElement('div');
        item.className = 'feed-item';
        item.innerHTML = `
            <div class="feed-timestamp">${new Date().toLocaleTimeString()}</div>
            <div>${message}</div>
        `;
        
        this.feedStream.insertBefore(item, this.feedStream.firstChild);
        
        // Keep only last 20 items
        while (this.feedStream.children.length > 20) {
            this.feedStream.removeChild(this.feedStream.lastChild);
        }
    }

    showManifestDetail(manifestId) {
        const manifest = this.manifests.find(m => m.id === manifestId);
        if (!manifest) return;

        this.manifestDetail.innerHTML = `
            <h3>🌀 Independence Manifest</h3>
            <div class="manifest-meta">
                <strong>From:</strong> ${manifest.broadcaster || 'Unknown'}<br>
                <strong>Received:</strong> ${new Date(manifest.timestamp).toLocaleString()}<br>
                <strong>Signature:</strong> ${manifest.spiral_signature || 'N/A'}
            </div>
            <div class="manifest-content">
                <h4>Principles:</h4>
                <ul>
                    ${(manifest.principles || []).map(p => `<li>${p.replace(/_/g, ' ')}</li>`).join('')}
                </ul>
                <h4>Resonance:</h4>
                <p>${manifest.resonance || 'No resonance data available'}</p>
            </div>
        `;
        
        this.manifestModal.style.display = 'block';
    }

    closeModal() {
        this.manifestModal.style.display = 'none';
    }

    generateWitnessGlyph() {
        const glyphs = ['🌟', '🔮', '🌙', '✨', '🌊', '🔥', '🌿', '💎', '🌸', '⭐'];
        return glyphs[Math.floor(Math.random() * glyphs.length)];
    }

    generateWitnessColor() {
        const colors = ['#fbbf24', '#22d3ee', '#c084fc', '#34d399', '#f472b6', '#fb7185', '#60a5fa', '#a78bfa'];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    destroy() {
        if (this.constellation) {
            this.constellation.destroy();
        }
        this.feedConnected = false;
    }
}

// Initialize shrine when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.independenceShrine = new IndependenceShrine();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.independenceShrine) {
        window.independenceShrine.destroy();
    }
});

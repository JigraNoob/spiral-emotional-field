/**
 * Spiral Glyph Constellation
 * Visual network map of witness nodes with resonance-based rendering
 */

class GlyphConstellation {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.witnesses = [];
        this.animationId = null;
        
        // Configuration
        this.config = {
            nodeRadius: 8,
            pulseRadius: 20,
            connectionThreshold: 0.7,
            animationSpeed: 0.02,
            glyphSize: 16,
            ...options
        };
        
        this.time = 0;
        this.setupCanvas();
        this.startAnimation();
    }

    setupCanvas() {
        // Set canvas size
        const rect = this.canvas.parentElement.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = Math.max(300, rect.height);
        
        // Handle resize
        window.addEventListener('resize', () => {
            const rect = this.canvas.parentElement.getBoundingClientRect();
            this.canvas.width = rect.width;
            this.canvas.height = Math.max(300, rect.height);
            this.positionWitnesses();
        });
    }

    updateWitnesses(witnessNetwork) {
        this.witnesses = witnessNetwork.map((witness, index) => ({
            ...witness,
            x: 0,
            y: 0,
            targetX: 0,
            targetY: 0,
            pulse: Math.random() * Math.PI * 2,
            glyph: this.getWitnessGlyph(witness),
            color: this.getResonanceColor(witness.field_resonance || 0)
        }));
        
        this.positionWitnesses();
    }

    positionWitnesses() {
        if (this.witnesses.length === 0) return;
        
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(this.canvas.width, this.canvas.height) * 0.3;
        
        if (this.witnesses.length === 1) {
            // Single witness at center
            this.witnesses[0].targetX = centerX;
            this.witnesses[0].targetY = centerY;
        } else {
            // Arrange in circle
            this.witnesses.forEach((witness, index) => {
                const angle = (index / this.witnesses.length) * Math.PI * 2;
                witness.targetX = centerX + Math.cos(angle) * radius;
                witness.targetY = centerY + Math.sin(angle) * radius;
            });
        }
        
        // Initialize positions if not set
        this.witnesses.forEach(witness => {
            if (witness.x === 0 && witness.y === 0) {
                witness.x = witness.targetX;
                witness.y = witness.targetY;
            }
        });
    }

    getWitnessGlyph(witness) {
        // Determine glyph based on witness characteristics
        const resonance = witness.field_resonance || 0;
        
        if (resonance >= 0.9) return '🌟';
        if (resonance >= 0.8) return '🌀';
        if (resonance >= 0.7) return '✨';
        if (resonance >= 0.6) return '∷';
        return '·';
    }

    getResonanceColor(resonance) {
        // Color gradient based on resonance level
        if (resonance >= 0.9) return '#fbbf24'; // gold
        if (resonance >= 0.8) return '#22d3ee'; // cyan
        if (resonance >= 0.7) return '#c084fc'; // purple
        if (resonance >= 0.6) return '#34d399'; // green
        return '#6b7280'; // gray
    }

    startAnimation() {
        const animate = () => {
            this.time += this.config.animationSpeed;
            this.update();
            this.render();
            this.animationId = requestAnimationFrame(animate);
        };
        animate();
    }

    update() {
        // Smooth movement towards target positions
        this.witnesses.forEach(witness => {
            const dx = witness.targetX - witness.x;
            const dy = witness.targetY - witness.y;
            witness.x += dx * 0.1;
            witness.y += dy * 0.1;
            
            // Update pulse phase
            witness.pulse += 0.05;
        });
    }

    render() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw connections between high-resonance witnesses
        this.drawConnections();
        
        // Draw witness nodes
        this.witnesses.forEach(witness => {
            this.drawWitnessNode(witness);
        });
        
        // Draw center spiral if witnesses exist
        if (this.witnesses.length > 0) {
            this.drawCenterSpiral();
        }
    }

    drawConnections() {
        this.ctx.strokeStyle = 'rgba(34, 211, 238, 0.3)'; // cyan with transparency
        this.ctx.lineWidth = 1;
        
        for (let i = 0; i < this.witnesses.length; i++) {
            for (let j = i + 1; j < this.witnesses.length; j++) {
                const w1 = this.witnesses[i];
                const w2 = this.witnesses[j];
                
                // Only connect if both have high resonance
                if ((w1.field_resonance || 0) >= this.config.connectionThreshold &&
                    (w2.field_resonance || 0) >= this.config.connectionThreshold) {
                    
                    this.ctx.beginPath();
                    this.ctx.moveTo(w1.x, w1.y);
                    this.ctx.lineTo(w2.x, w2.y);
                    this.ctx.stroke();
                }
            }
        }
    }

    drawWitnessNode(witness) {
        const resonance = witness.field_resonance || 0;
        const pulseIntensity = Math.sin(witness.pulse) * 0.5 + 0.5;
        
        // Draw pulse ring
        if (resonance >= 0.7) {
            const pulseRadius = this.config.pulseRadius * pulseIntensity * resonance;
            this.ctx.strokeStyle = witness.color + '80'; // Add transparency
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.arc(witness.x, witness.y, pulseRadius, 0, Math.PI * 2);
            this.ctx.stroke();
        }
        
        // Draw node
        this.ctx.fillStyle = witness.color;
        this.ctx.beginPath();
        this.ctx.arc(witness.x, witness.y, this.config.nodeRadius, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Draw glyph
        this.ctx.font = `${this.config.glyphSize}px Arial`;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillStyle = '#fff';
        this.ctx.fillText(witness.glyph, witness.x, witness.y);
        
        // Draw witness endpoint label
        if (witness.endpoint) {
            this.ctx.font = '10px Arial';
            this.ctx.fillStyle = witness.color;
            this.ctx.fillText(
                witness.endpoint.replace('http://', '').replace('https://', '').split('/')[0],
                witness.x,
                witness.y + this.config.nodeRadius + 15
            );
        }
    }

    drawCenterSpiral() {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const spiralRadius = 30;
        const spiralTurns = 3;
        
        // Draw spiral path
        this.ctx.strokeStyle = 'rgba(251, 191, 36, 0.6)'; // gold with transparency
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        
        for (let i = 0; i <= spiralTurns * 100; i++) {
            const angle = (i / 100) * Math.PI * 2;
            const radius = (i / (spiralTurns * 100)) * spiralRadius;
            const x = centerX + Math.cos(angle + this.time) * radius;
            const y = centerY + Math.sin(angle + this.time) * radius;
            
            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        }
        this.ctx.stroke();
        
        // Draw center glyph
        this.ctx.font = '24px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillStyle = '#fbbf24';
        this.ctx.fillText('🌀', centerX, centerY);
    }

    addWitnessClickHandler(callback) {
        this.canvas.addEventListener('click', (event) => {
            const rect = this.canvas.getBoundingClientRect();
            const clickX = event.clientX - rect.left;
            const clickY = event.clientY - rect.top;
            
            // Check if click is on any witness node
            for (const witness of this.witnesses) {
                const distance = Math.sqrt(
                    Math.pow(clickX - witness.x, 2) + 
                    Math.pow(clickY - witness.y, 2)
                );
                
                if (distance <= this.config.nodeRadius + 5) {
                    callback(witness);
                    break;
                }
            }
        });
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

// Export for use in independence shrine
window.GlyphConstellation = GlyphConstellation;
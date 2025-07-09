(function constellationOverlay() {
    let overrideState = {
        mode: 'NATURAL',
        active: false,
        intensity: 1.0,
        emotional_state: 'neutral',
        thresholds: {
            resonance: 0.65,
            silence: 0.7,
            breakpoint: 0.7
        }
    };

    let constellationCanvas = null;
    let ctx = null;
    let animationFrame = null;
    let stars = [];
    let connections = [];

    function initConstellation() {
        // Create overlay canvas
        constellationCanvas = document.createElement('canvas');
        constellationCanvas.id = 'constellation-overlay';
        constellationCanvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 1000;
            opacity: 0.3;
            transition: opacity 0.5s ease;
        `;
        document.body.appendChild(constellationCanvas);
        
        ctx = constellationCanvas.getContext('2d');
        resizeCanvas();
        generateStars();
        
        window.addEventListener('resize', resizeCanvas);
        startAnimation();
    }

    function resizeCanvas() {
        constellationCanvas.width = window.innerWidth;
        constellationCanvas.height = window.innerHeight;
    }

    function generateStars() {
        stars = [];
        const starCount = Math.floor((window.innerWidth * window.innerHeight) / 15000);
        
        for (let i = 0; i < starCount; i++) {
            stars.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                size: Math.random() * 2 + 0.5,
                brightness: Math.random() * 0.8 + 0.2,
                pulse: Math.random() * Math.PI * 2,
                pulseSpeed: 0.02 + Math.random() * 0.03,
                resonance: Math.random()
            });
        }
    }

    function updateOverrideVisualization() {
        // Fetch current override state
        fetch('/echo/override_state')
            .then(response => response.json())
            .then(data => {
                overrideState = data;
                updateConstellationAppearance();
            })
            .catch(err => console.log('Override state fetch failed:', err));
    }

    function updateConstellationAppearance() {
        const overlay = document.getElementById('constellation-overlay');
        if (!overlay) return;

        // Adjust opacity based on mode
        switch (overrideState.mode) {
            case 'AMPLIFIED':
                overlay.style.opacity = '0.6';
                break;
            case 'MUTED':
                overlay.style.opacity = '0.1';
                break;
            case 'RITUAL':
                overlay.style.opacity = '0.8';
                break;
            case 'EMOTIONAL':
                overlay.style.opacity = '0.4';
                break;
            case 'DEFERRAL':
                overlay.style.opacity = '0.3';
                break;
            default:
                overlay.style.opacity = '0.3';
        }
    }

    function drawConstellation() {
        if (!ctx) return;
        
        ctx.clearRect(0, 0, constellationCanvas.width, constellationCanvas.height);
        
        // Draw stars with mode-specific effects
        stars.forEach(star => {
            ctx.save();
            
            // Calculate brightness based on override state
            let brightness = star.brightness;
            let color = getStarColor(star);
            
            // Apply mode-specific modulations
            if (overrideState.active) {
                brightness *= overrideState.intensity;
                
                // Add pulse effect for certain modes
                if (overrideState.mode === 'RITUAL' || overrideState.mode === 'AMPLIFIED') {
                    star.pulse += star.pulseSpeed;
                    brightness *= (0.7 + 0.3 * Math.sin(star.pulse));
                }
            }
            
            // Draw star
            ctx.globalAlpha = brightness;
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
            ctx.fill();
            
            // Draw resonance rings for high-resonance stars
            if (star.resonance > overrideState.thresholds.resonance && overrideState.active) {
                ctx.strokeStyle = color;
                ctx.globalAlpha = brightness * 0.3;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.arc(star.x, star.y, star.size * 3, 0, Math.PI * 2);
                ctx.stroke();
            }
            
            ctx.restore();
        });
        
        // Draw connections between resonant stars
        if (overrideState.mode === 'RITUAL' || overrideState.mode === 'AMPLIFIED') {
            drawResonanceConnections();
        }
    }

    function getStarColor(star) {
        if (!overrideState.active) {
            return `hsl(200, 30%, ${70 + star.brightness * 30}%)`;
        }
        
        switch (overrideState.mode) {
            case 'AMPLIFIED':
                return `hsl(${45 + star.resonance * 60}, 70%, ${60 + star.brightness * 40}%)`; // Gold to orange
            case 'MUTED':
                return `hsl(220, 20%, ${40 + star.brightness * 20}%)`; // Muted blue-gray
            case 'RITUAL':
                return `hsl(${280 + star.resonance * 40}, 80%, ${50 + star.brightness * 50}%)`; // Purple to magenta
            case 'EMOTIONAL':
                return getEmotionalColor(star);
            case 'DEFERRAL':
                return `hsl(${180 + star.resonance * 40}, 50%, ${50 + star.brightness * 30}%)`; // Cyan to teal
            default:
                return `hsl(200, 30%, ${70 + star.brightness * 30}%)`;
        }
    }

    function getEmotionalColor(star) {
        const emotionalPalettes = {
            joy: `hsl(${50 + star.resonance * 20}, 90%, ${60 + star.brightness * 40}%)`, // Bright yellow
            calm: `hsl(${120 + star.resonance * 40}, 60%, ${50 + star.brightness * 30}%)`, // Soft green
            anxiety: `hsl(${0 + star.resonance * 30}, 70%, ${40 + star.brightness * 30}%)`, // Red-orange
            curiosity: `hsl(${240 + star.resonance * 60}, 80%, ${60 + star.brightness * 40}%)`, // Blue to purple
            neutral: `hsl(200, 30%, ${70 + star.brightness * 30}%)`
        };
        
        return emotionalPalettes[overrideState.emotional_state] || emotionalPalettes.neutral;
    }

    function drawResonanceConnections() {
        const resonantStars = stars.filter(star => star.resonance > overrideState.thresholds.resonance);
        
        for (let i = 0; i < resonantStars.length; i++) {
            for (let j = i + 1; j < resonantStars.length; j++) {
                const star1 = resonantStars[i];
                const star2 = resonantStars[j];
                const distance = Math.sqrt(
                    Math.pow(star2.x - star1.x, 2) + Math.pow(star2.y - star1.y, 2)
                );
                
                // Only connect nearby resonant stars
                if (distance < 200) {
                    ctx.save();
                    ctx.strokeStyle = getStarColor(star1);
                    ctx.globalAlpha = 0.1 * (1 - distance / 200);
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(star1.x, star1.y);
                    ctx.lineTo(star2.x, star2.y);
                    ctx.stroke();
                    ctx.restore();
                }
            }
        }
    }

    function startAnimation() {
        function animate() {
            drawConstellation();
            animationFrame = requestAnimationFrame(animate);
        }
        animate();
    }

    function createOverrideControls() {
        const controlPanel = document.createElement('div');
        controlPanel.id = 'override-controls';
        controlPanel.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            z-index: 1001;
            min-width: 200px;
            backdrop-filter: blur(5px);
        `;
        
        controlPanel.innerHTML = `
            <div style="margin-bottom: 10px; font-weight: bold;">🌀 Resonance Override</div>
            <div id="override-status">Mode: ${overrideState.mode}</div>
            <div id="override-intensity">Intensity: ${overrideState.intensity.toFixed(1)}x</div>
            <div id="override-emotional">State: ${overrideState.emotional_state}</div>
            <div style="margin-top: 10px;">
                <button onclick="toggleOverride()" style="background: #333; color: white; border: 1px solid #666; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                    ${overrideState.active ? 'Deactivate' : 'Activate'}
                </button>
            </div>
        `;
        
        document.body.appendChild(controlPanel);
    }

    // Global functions for control
    window.toggleOverride = function() {
        const newState = !overrideState.active;
        fetch('/echo/override_set', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                active: newState,
                mode: newState ? 'AMPLIFIED' : 'NATURAL'
            })
        }).then(() => updateOverrideVisualization());
    };

    window.setOverrideMode = function(mode) {
        fetch('/echo/override_set', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: mode, active: true })
        }).then(() => updateOverrideVisualization());
    };

    // Initialize everything
    function init() {
        initConstellation();
        createOverrideControls();
        updateOverrideVisualization();
        
        // Update state every 5 seconds
        setInterval(updateOverrideVisualization, 5000);
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        cancelAnimationFrame(animationFrame);
        document.body.removeChild(constellationCanvas);
        document.body.removeChild(document.getElementById('override-controls'));
    });
})()
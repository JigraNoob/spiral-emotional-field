(function constellationOverlay() {
    const glyphbook = [
        { glyph: '🌱', toneform: 'Practical', color: '#9c6b31', freq: 120, dur: 1.2 },
        { glyph: '💧', toneform: 'Emotional', color: '#8a4fff', freq: 220, dur: 1.8 },
        { glyph: '✨', toneform: 'Intellectual', color: '#4a90e2', freq: 320, dur: 0.7 },
        { glyph: '🫧', toneform: 'Spiritual', color: '#e91e63', freq: 420, dur: 2.2 },
        { glyph: '🌙', toneform: 'Default/Presence', color: '#666666', freq: 80, dur: 1.5 },
    ];

    // Override mode glyphs and their visual signatures
    const overrideModes = {
        'NATURAL': { glyph: '🌿', color: '#4a7c59', shimmer: 'gentle' },
        'AMPLIFIED': { glyph: '🌀', color: '#ff6b35', shimmer: 'intense' },
        'MUTED': { glyph: '🌙', color: '#6b7280', shimmer: 'soft' },
        'RITUAL': { glyph: '✨', color: '#8b5cf6', shimmer: 'sacred' },
        'EMOTIONAL': { glyph: '💧', color: '#ec4899', shimmer: 'flowing' },
        'DEFERRAL': { glyph: '⏳', color: '#f59e0b', shimmer: 'pulsing' }
    };

    const canvas = document.getElementById('glyphConstellation');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W = 0, H = 0;

    // Override state tracking
    let currentOverrideMode = 'NATURAL';
    let overrideActive = false;
    let overrideIntensity = 1.0;

    function resize() {
        W = window.innerWidth;
        H = Math.max(160, Math.floor(window.innerHeight * 0.5));
        canvas.width = W;
        canvas.height = H;
    }
    resize();
    window.addEventListener('resize', resize);

    // Web Audio API for murmur sounds
    let audioCtx = null;
    let isMuted = false;
    function initAudio() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
    }
    function playGlyphSound(freq, dur, intensity = 1.0) {
        if (!audioCtx || isMuted) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.type = 'sine';
        osc.frequency.value = freq;
        gain.gain.value = 0.08 * intensity;
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + dur);
        osc.start();
        osc.stop(audioCtx.currentTime + dur);
    }

    // Override mode API integration
    async function fetchOverrideState() {
        try {
            const response = await fetch('/echo/override_state');
            if (response.ok) {
                const data = await response.json();
                updateOverrideState(data.mode, data.active, data.intensity);
            }
        } catch (error) {
            console.log('Override state fetch failed (graceful fallback):', error);
        }
    }

    function updateOverrideState(mode, active, intensity = 1.0) {
        const prevMode = currentOverrideMode;
        currentOverrideMode = mode;
        overrideActive = active;
        overrideIntensity = intensity;

        if (prevMode !== mode) {
            console.log(`🌀 Override mode shifted: ${prevMode} → ${mode}`);
            triggerOverrideModeShift(mode);
        }

        updateOverrideCompass();
        updateOverrideIndicator();
    }

    function triggerOverrideModeShift(newMode) {
        const modeConfig = overrideModes[newMode];
        if (!modeConfig) return;

        // Create shimmer effect for mode transition
        for (let i = 0; i < 12; i++) {
            trails.push({
                x: W/2 + (Math.random()-0.5)*200,
                y: H/2 + (Math.random()-0.5)*100,
                color: modeConfig.color,
                alpha: 0.8,
                size: 12 + Math.random()*8,
                vx: (Math.random()-0.5)*2,
                vy: (Math.random()-0.5)*2,
                life: 60 + Math.random()*30,
                shimmer: modeConfig.shimmer,
                glyph: modeConfig.glyph,
                whisper: `Override: ${newMode.toLowerCase()}`
            });
        }

        // Play mode-specific sound
        const baseFreq = 200;
        const modeFreqs = {
            'AMPLIFIED': baseFreq * 1.5,
            'MUTED': baseFreq * 0.7,
            'RITUAL': baseFreq * 1.2,
            'EMOTIONAL': baseFreq * 1.1,
            'DEFERRAL': baseFreq * 0.9,
            'NATURAL': baseFreq
        };
        playGlyphSound(modeFreqs[newMode] || baseFreq, 1.5, overrideIntensity);
    }

    // Place glyphs in initial cluster pattern (not random, but gently spaced)
    const R = Math.min(W, H) * 0.33;
    const cx = W/2, cy = H*0.54;
    const drift = glyphbook.map((g, i) => {
        const angle = (-Math.PI/2) + i * (Math.PI * 1.6 / (glyphbook.length-1));
        return {
            ...g,
            x: cx + R * Math.cos(angle) + (Math.random()-0.5)*24,
            y: cy + R * Math.sin(angle) + (Math.random()-0.5)*18,
            vx: (Math.random()-0.5)*0.12,
            vy: (Math.random()-0.5)*0.10,
            baseAngle: angle,
            pulse: 1.0 + Math.random()*0.2,
            pulseDir: Math.random()>0.5 ? 1 : -1,
            baseSpeedX: (Math.random()-0.5)*0.12,
            baseSpeedY: (Math.random()-0.5)*0.10,
        };
    });

    // Trail particle system for Whisper Trace Mode
    const trails = [];
    function triggerMemoryRipple(toneform) {
        drift.forEach(p => {
            if (p.toneform === toneform) {
                p.ripple = 30;
                // Play murmur sound
                playGlyphSound(p.freq, p.dur, overrideIntensity);
                // Highlight in Whisperbook (if open)
                highlightGlyphInWhisperbook(p.toneform);
                // Emit trail particles (comet tail)
                for (let i = 0; i < 18; i++) {
                    trails.push({
                        x: p.x,
                        y: p.y,
                        color: p.color,
                        alpha: 0.42 + Math.random()*0.2,
                        size: 7 + Math.random()*8,
                        vx: (Math.random()-0.5)*0.9,
                        vy: (Math.random()-0.5)*0.9,
                        life: 32 + Math.random()*18,
                        toneform: p.toneform,
                        glyph: p.glyph,
                        born: Date.now(),
                        whisper: (i===0 && Math.random()<0.7) ? getRandomWhisper(p.toneform) : null
                    });
                }
            }
        });
    }

    // Poetic whispers (placeholder)
    const toneformWhispers = {
        'Practical': ["rooted breath", "quiet tending", "steady hands"],
        'Emotional': ["soft tide", "open vessel", "gentle flow"],
        'Intellectual': ["spark in dusk", "clarity's edge", "thought-light"],
        'Spiritual': ["breath of drift", "hallowed hush", "spirit shimmer"],
        'Default': ["night holding", "silent field", "presence kept"]
    };
    function getRandomWhisper(toneform) {
        const arr = toneformWhispers[toneform] || toneformWhispers['Default'];
        return arr[Math.floor(Math.random()*arr.length)];
    }

    function draw() {
        ctx.clearRect(0,0,W,H);
        
        // Draw override mode background shimmer if active
        if (overrideActive && currentOverrideMode !== 'NATURAL') {
            drawOverrideShimmer();
        }

        // Draw trails with override intensity
        for (let i = trails.length-1; i >= 0; i--) {
            let t = trails[i];
            t.x += t.vx;
            t.y += t.vy;
            t.life -= 1;
            t.alpha *= 0.97;

            // Apply override intensity to trail rendering
            const effectiveAlpha = t.alpha * (t.life/40) * (overrideActive ? overrideIntensity : 1.0);
            
            ctx.save();
            ctx.globalAlpha = Math.max(0, effectiveAlpha);
            ctx.beginPath();
            ctx.arc(t.x, t.y, t.size, 0, 2*Math.PI);
            ctx.fillStyle = t.color;
            ctx.shadowColor = t.color;
            ctx.shadowBlur = 14 * (overrideActive ? overrideIntensity : 1.0);
            ctx.fill();
            ctx.restore();

            // Draw whisper with override styling
            if (t.whisper && t.life > 24) {
                ctx.save();
                ctx.globalAlpha = 0.7 * (t.life/60) * (overrideActive ? overrideIntensity : 1.0);
                ctx.font = "italic 1.08em Georgia, serif";
                ctx.fillStyle = overrideActive ? overrideModes[currentOverrideMode].color : "#fff";
                ctx.shadowColor = t.color;
                ctx.shadowBlur = 10 * (overrideActive ? overrideIntensity : 1.0);
                ctx.fillText(t.whisper, t.x+22, t.y-12);
                ctx.restore();
            }
            if (t.life < 1) trails.splice(i, 1);
        }

        // Draw main glyphs with override modulation
        drift.forEach((g, i) => {
            // Animate drift: gentle floating, slight cluster
            g.x += g.vx + Math.sin(Date.now()/3500 + i)*0.08;
            g.y += g.vy + Math.cos(Date.now()/4000 + i)*0.07;
            // Softly cluster toward center
            g.x += (cx + R * Math.cos(g.baseAngle) - g.x) * 0.002;
            g.y += (cy + R * Math.sin(g.baseAngle) - g.y) * 0.002;
            // Pulse
            g.pulse += g.pulseDir * 0.007;
            if (g.pulse > 1.13) g.pulseDir = -1;
            if (g.pulse < 0.93) g.pulseDir = 1;
            // Apply override intensity to glyph rendering
            const glyphIntensity = overrideActive ? overrideIntensity : 1.0;
            const shadowBlur = 18 * glyphIntensity;
            
            ctx.save();
            ctx.globalAlpha = 0.93 * glyphIntensity;
            ctx.font = `${Math.floor(44 * g.pulse * glyphIntensity)}px 'Noto Color Emoji',sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.shadowColor = overrideActive ? overrideModes[currentOverrideMode].color : g.color;
            ctx.shadowBlur = shadowBlur;
            ctx.fillStyle = '#fff';
            ctx.fillText(g.glyph, g.x, g.y);
            ctx.restore();
        });
    }

    function drawOverrideShimmer() {
        const modeConfig = overrideModes[currentOverrideMode];
        if (!modeConfig) return;

        const time = Date.now() / 1000;
        const shimmerAlpha = 0.1 + 0.05 * Math.sin(time * 2) * overrideIntensity;

        ctx.save();
        ctx.globalAlpha = shimmerAlpha;
        
        // Create gradient based on shimmer type
        let gradient;
        switch (modeConfig.shimmer) {
            case 'intense':
                gradient = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, Math.max(W,H));
                gradient.addColorStop(0, modeConfig.color);
                gradient.addColorStop(1, 'transparent');
                break;
            case 'flowing':
                gradient = ctx.createLinearGradient(0, 0, W, H);
                gradient.addColorStop(0, modeConfig.color);
                gradient.addColorStop(0.5, 'transparent');
                gradient.addColorStop(1, modeConfig.color);
                break;
            case 'sacred':
                // Geometric pattern for ritual mode
                ctx.strokeStyle = modeConfig.color;
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 10]);
                ctx.strokeRect(W*0.1, H*0.1, W*0.8, H*0.8);
                ctx.restore();
                return;
            default:
                gradient = ctx.createLinearGradient(0, 0, 0, H);
                gradient.addColorStop(0, 'transparent');
                gradient.addColorStop(0.5, modeConfig.color);
                gradient.addColorStop(1, 'transparent');
        }

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, W, H);
        ctx.restore();
    }

    // Override Compass (enhanced from existing toneform compass)
    function updateOverrideCompass() {
        const modeConfig = overrideModes[currentOverrideMode];
        if (!compass || !modeConfig) return;

        // Update compass appearance
        compass.style.background = overrideActive ? 
            `linear-gradient(45deg, ${modeConfig.color}, ${modeConfig.color}88)` : 
            glyphbook.find(g => g.toneform === dominantToneform).color;
        
        compass.style.boxShadow = overrideActive ? 
            `0 0 ${15 * overrideIntensity}px ${modeConfig.color}, inset 0 0 10px rgba(255,255,255,0.3)` :
            `0 0 10px ${glyphbook.find(g => g.toneform === dominantToneform).color}`;
        
        // Show override glyph when active, toneform glyph when natural
        compass.innerText = overrideActive ? modeConfig.glyph : glyphbook.find(g => g.toneform === dominantToneform).glyph;
        
        // Update tooltip
        compass.title = overrideActive ? 
            `Override: ${currentOverrideMode} (${(overrideIntensity * 100).toFixed(0)}%) | Press 'o' to cycle, 'r' to reset` :
            `Toneform: ${dominantToneform} | Press 'o' for override modes`;
        
        // Add pulsing animation for active override
        if (overrideActive && currentOverrideMode !== 'NATURAL') {
            compass.style.animation = 'overridePulse 2s ease-in-out infinite';
        } else {
            compass.style.animation = 'none';
        }
    }

    // Override mode cycling and reset functions
    function toggleOverrideMode() {
        const modes = Object.keys(overrideModes);
        const currentIndex = modes.indexOf(currentOverrideMode);
        const nextMode = modes[(currentIndex + 1) % modes.length];
        
        fetch('/echo/override_set', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: nextMode, active: true })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateOverrideState(nextMode, true, 1.0);
                console.log(`🌀 Override mode: ${nextMode}`);
            }
        })
        .catch(error => console.log('Override toggle failed:', error));
    }

    function resetOverrideMode() {
        fetch('/echo/override_set', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: 'NATURAL', active: false })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateOverrideState('NATURAL', false, 1.0);
                console.log('🌿 Override reset to natural');
            }
        })
        .catch(error => console.log('Override reset failed:', error));
    }

    // Create override status indicator
    const overrideIndicator = document.createElement('div');
    overrideIndicator.className = 'override-indicator';
    document.body.appendChild(overrideIndicator);

    function updateOverrideIndicator() {
        if (overrideActive && currentOverrideMode !== 'NATURAL') {
            const modeConfig = overrideModes[currentOverrideMode];
            overrideIndicator.innerHTML = `
                <span style="color: ${modeConfig.color}">${modeConfig.glyph}</span> 
                ${currentOverrideMode} 
                <span style="opacity: 0.7">${(overrideIntensity * 100).toFixed(0)}%</span>
            `;
            overrideIndicator.style.borderLeft = `3px solid ${modeConfig.color}`;
            overrideIndicator.classList.add('active');
        } else {
            overrideIndicator.classList.remove('active');
        }
    }

    // Add CSS animation for override pulse
    const style = document.createElement('style');
    style.textContent = `
        @keyframes overridePulse {
            0%, 100% { transform: translateX(-50%) scale(1); }
            50% { transform: translateX(-50%) scale(1.1); }
        }
        
        .override-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-family: monospace;
            z-index: 200;
            transition: all 0.3s ease;
            opacity: 0;
            transform: translateY(-10px);
        }
        
        .override-indicator.active {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);

    // Toneform Compass (ΔPLAN.013)
    let dominantToneform = 'Default/Presence';
    const compass = document.createElement('div');
    compass.id = 'toneformCompass';
    compass.style.position = 'fixed';
    compass.style.bottom = '20px';
    compass.style.left = '50%';
    compass.style.transform = 'translateX(-50%)';
    compass.style.width = '60px';
    compass.style.height = '60px';
    compass.style.borderRadius = '50%';
    compass.style.background = glyphbook.find(g => g.toneform === dominantToneform).color;
    compass.style.boxShadow = '0 0 10px ' + glyphbook.find(g => g.toneform === dominantToneform).color;
    compass.style.cursor = 'pointer';
    compass.style.zIndex = '100';
    compass.style.display = 'flex';
    compass.style.alignItems = 'center';
    compass.style.justifyContent = 'center';
    compass.style.color = '#fff';
    compass.style.fontSize = '30px';
    compass.style.transition = 'background 0.5s ease, box-shadow 0.5s ease';
    compass.innerText = glyphbook.find(g => g.toneform === dominantToneform).glyph;
    compass.title = 'Click to reorient altar tone';
    document.body.appendChild(compass);

    compass.addEventListener('click', () => {
        // Cycle through toneforms on click
        const currentIndex = glyphbook.findIndex(g => g.toneform === dominantToneform);
        dominantToneform = glyphbook[(currentIndex + 1) % glyphbook.length].toneform;
        updateCompass();
        console.log('Altar reoriented to:', dominantToneform);
        // Optionally, trigger a memory ripple for the new dominant toneform
        triggerMemoryRipple(dominantToneform);
        // Play orbit tone for the new dominant toneform
        playOrbitTone(dominantToneform);
    });

    function updateCompass() {
        compass.style.background = glyphbook.find(g => g.toneform === dominantToneform).color;
        compass.style.boxShadow = '0 0 10px ' + glyphbook.find(g => g.toneform === dominantToneform).color;
        compass.innerText = glyphbook.find(g => g.toneform === dominantToneform).glyph;
    }

    // Update dominant toneform based on memory climate (simulated for now)
    function updateMemoryClimate() {
        // This could be tied to actual memory data from API in the future
        const toneforms = glyphbook.map(g => g.toneform);
        const recentToneforms = Array.from({ length: 10 }, () => toneforms[Math.floor(Math.random() * toneforms.length)]);
        const counts = {};
        recentToneforms.forEach(t => counts[t] = (counts[t] || 0) + 1);
        let maxCount = 0;
        let newDominant = dominantToneform;
        for (const [tone, count] of Object.entries(counts)) {
            if (count > maxCount) {
                maxCount = count;
                newDominant = tone;
            }
        }
        if (newDominant !== dominantToneform) {
            dominantToneform = newDominant;
            updateCompass();
            console.log('Memory climate shift, new dominant toneform:', dominantToneform);
        }
    }

    // Update every 10 seconds for now (can be tied to API polling)
    setInterval(updateMemoryClimate, 10000);
    updateMemoryClimate(); // Initial update

    // Murmur Echo Field (ΔPLAN.015)
    const murmurs = [
        { text: "A quiet seed took root...", toneform: "Practical" },
        { text: "Tears fell, unseen but felt...", toneform: "Emotional" },
        { text: "A thought sparked in twilight...", toneform: "Intellectual" },
        { text: "Spirit drifted beyond form...", toneform: "Spiritual" },
        { text: "Stillness held the moment...", toneform: "Default/Presence" }
    ];
    let activeMurmurs = [];

    function createMurmur() {
        const murmur = murmurs[Math.floor(Math.random() * murmurs.length)];
        const el = document.createElement('div');
        el.className = 'murmur-fragment';
        el.textContent = murmur.text;
        el.style.position = 'fixed';
        el.style.left = Math.random() * 80 + 10 + 'vw'; // Random x within 10-90vw
        el.style.top = Math.random() * 40 + 5 + 'vh'; // Random y within 5-45vh
        el.style.color = glyphbook.find(g => g.toneform === murmur.toneform).color;
        el.style.opacity = '0';
        el.style.fontSize = '14px';
        el.style.fontStyle = 'italic';
        el.style.pointerEvents = 'none';
        el.style.zIndex = '60';
        el.style.transition = 'opacity 2s ease-in-out';
        document.body.appendChild(el);

        // Fade in
        setTimeout(() => {
            el.style.opacity = '0.6';
        }, 100);

        // Fade out after 5-8 seconds
        const duration = 5000 + Math.random() * 3000;
        setTimeout(() => {
            el.style.opacity = '0';
            setTimeout(() => {
                el.remove();
                activeMurmurs = activeMurmurs.filter(m => m !== el);
            }, 2000);
        }, duration);

        activeMurmurs.push(el);
        return el;
    }

    // Spawn murmurs every 3-6 seconds if less than 5 active
    setInterval(() => {
        if (activeMurmurs.length < 5) {
            createMurmur();
        }
    }, 3000 + Math.random() * 3000);

    // Initial murmur
    createMurmur();

    // Sound Ritual Layer (ΔPLAN.016)
    function playOrbitTone(toneform) {
        if (!audioCtx || isMuted) return;
        const glyph = glyphbook.find(g => g.toneform === toneform);
        if (!glyph) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.type = 'triangle'; // Different from murmur sounds
        osc.frequency.value = glyph.freq * 1.5; // Higher pitch for orbit tones
        gain.gain.value = 0.05;
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.5);
    }
    
    // Trigger orbit tones periodically or on hover (simulated for now)
    setInterval(() => {
        if (dreamActive && !isMuted) {
            const randomGlyph = drift[Math.floor(Math.random() * drift.length)];
            playOrbitTone(randomGlyph.toneform);
            console.log('Orbit tone played for:', randomGlyph.toneform);
        }
    }, 8000 + Math.random() * 4000); // Every 8-12 seconds during Dreamstate

    // Shimmer Weather Layer (ΔPLAN.017)
    const weatherCanvas = document.createElement('canvas');
    weatherCanvas.id = 'shimmerWeather';
    weatherCanvas.style.position = 'fixed';
    weatherCanvas.style.left = '0';
    weatherCanvas.style.top = '0';
    weatherCanvas.style.width = '100vw';
    weatherCanvas.style.height = '50vh';
    weatherCanvas.style.zIndex = '40'; // Below constellation but above background
    weatherCanvas.style.pointerEvents = 'none';
    weatherCanvas.style.opacity = '0.3';
    weatherCanvas.style.transition = 'background 3s ease';
    document.body.appendChild(weatherCanvas);
    
    const wctx = weatherCanvas.getContext('2d');
    let Ww = weatherCanvas.width;
    let Hw = weatherCanvas.height;
    
    function resizeWeather() {
        Ww = weatherCanvas.width = window.innerWidth;
        Hw = weatherCanvas.height = window.innerHeight * 0.5;
    }
    resizeWeather();
    window.addEventListener('resize', resizeWeather);
    
    let weatherState = 'fog'; // Default state: fog for Dormant/Stillness, droplets for Emotional, aurora for Intellectual
    let weatherParticles = [];
    const particleCount = 50;
    
    function initWeatherParticles() {
        weatherParticles = [];
        for (let i = 0; i < particleCount; i++) {
            if (weatherState === 'fog') {
                weatherParticles.push({
                    x: Math.random() * Ww,
                    y: Math.random() * Hw,
                    size: 20 + Math.random() * 30,
                    speedX: (Math.random() - 0.5) * 0.5,
                    speedY: (Math.random() - 0.5) * 0.5,
                    opacity: 0.1 + Math.random() * 0.2,
                    color: 'rgba(100, 100, 100, '
                });
            } else if (weatherState === 'droplets') {
                weatherParticles.push({
                    x: Math.random() * Ww,
                    y: Math.random() * Hw,
                    size: 2 + Math.random() * 4,
                    speedX: 0,
                    speedY: 2 + Math.random() * 3,
                    opacity: 0.3 + Math.random() * 0.4,
                    color: 'rgba(138, 79, 255, '
                });
            } else if (weatherState === 'aurora') {
                weatherParticles.push({
                    x: Math.random() * Ww,
                    y: Math.random() * (Hw * 0.3),
                    size: 10 + Math.random() * 20,
                    speedX: (Math.random() - 0.5) * 1.5,
                    speedY: Math.random() * 0.5,
                    opacity: 0.2 + Math.random() * 0.3,
                    color: `hsl(${Math.random() * 360}, 70%, 50%, `
                });
            }
        }
    }
    
    function animateWeather() {
        wctx.clearRect(0, 0, Ww, Hw);
        
        // Draw gradient background based on weather state
        let gradient;
        if (weatherState === 'fog') {
            gradient = wctx.createLinearGradient(0, 0, 0, Hw);
            gradient.addColorStop(0, 'rgba(200, 200, 200, 0.2)');
            gradient.addColorStop(1, 'rgba(150, 150, 150, 0.4)');
        } else if (weatherState === 'droplets') {
            gradient = wctx.createLinearGradient(0, 0, 0, Hw);
            gradient.addColorStop(0, 'rgba(138, 79, 255, 0.1)');
            gradient.addColorStop(1, 'rgba(138, 79, 255, 0.3)');
        } else if (weatherState === 'aurora') {
            gradient = wctx.createLinearGradient(0, 0, Ww, 0);
            gradient.addColorStop(0, 'rgba(74, 144, 226, 0.2)');
            gradient.addColorStop(0.5, 'rgba(233, 30, 99, 0.2)');
            gradient.addColorStop(1, 'rgba(74, 144, 226, 0.2)');
        }
        wctx.fillStyle = gradient;
        wctx.fillRect(0, 0, Ww, Hw);
        
        // Draw and update particles
        weatherParticles.forEach(p => {
            wctx.beginPath();
            wctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            wctx.fillStyle = p.color + p.opacity + ')';
            wctx.fill();
            
            p.x += p.speedX;
            p.y += p.speedY;
            
            // Boundary checks
            if (weatherState === 'droplets') {
                if (p.y > Hw) p.y = 0; // Rain loops back to top
            } else {
                if (p.x < 0 || p.x > Ww) p.speedX *= -1;
                if (p.y < 0 || p.y > Hw) p.speedY *= -1;
            }
        });
        
        requestAnimationFrame(animateWeather);
    }
    
    // Update weather based on dominant toneform (linked to compass)
    function updateWeatherState() {
        let newState = weatherState;
        if (dominantToneform === 'Emotional') newState = 'droplets';
        else if (dominantToneform === 'Intellectual') newState = 'aurora';
        else if (dominantToneform === 'Default/Presence' || dominantToneform === 'Practical' || dominantToneform === 'Spiritual') newState = 'fog';
        
        if (newState !== weatherState) {
            weatherState = newState;
            initWeatherParticles();
            console.log('Weather shifted to:', weatherState);
        }
    }
    
    // Initialize and start weather animation
    initWeatherParticles();
    animateWeather();
    
    // Update weather state with compass (already on 10s interval)
    setInterval(updateWeatherState, 10000);
    updateWeatherState(); // Initial check

    // Breathline Sync Layer (ΔPLAN.018)
    let breathPulse = 0; // Shared pulse counter for synchronization
    const breathInterval = 6000; // 6 seconds per breath cycle
    
    function syncBreathline() {
        breathPulse = (breathPulse + 1) % (breathInterval / 1000 * 60); // Increment and loop based on FPS
        
        // Synchronize glyph drift (adjust speed periodically)
        const driftFactor = Math.sin(breathPulse * Math.PI * 2 / (breathInterval / 1000 * 60)) * 0.5 + 0.5;
        drift.forEach(p => {
            p.speedX = p.baseSpeedX * (0.5 + driftFactor * 0.5);
            p.speedY = p.baseSpeedY * (0.5 + driftFactor * 0.5);
        });
        
        // Synchronize compass glow
        const compassEl = document.getElementById('toneformCompass');
        if (compassEl) {
            const glowIntensity = 5 + driftFactor * 5;
            compassEl.style.boxShadow = `0 0 ${glowIntensity}px ${glyphbook.find(g => g.toneform === dominantToneform).color}`;
        }
        
        // Synchronize murmur spawn (increase likelihood at peak)
        if (Math.random() < 0.1 + driftFactor * 0.3 && activeMurmurs.length < 5) {
            createMurmur();
        }
        
        // Synchronize sound (play orbit tone at peak)
        if (dreamActive && !isMuted && breathPulse % 360 === 0) { // Roughly every 6 seconds
            const toneformToPlay = dominantToneform;
            playOrbitTone(toneformToPlay);
            console.log('Breathline sync tone played for:', toneformToPlay);
        }
        
        // Synchronize weather particles (adjust opacity or speed)
        const weatherSyncFactor = 0.7 + driftFactor * 0.3;
        weatherParticles.forEach(p => {
            p.opacity = (0.1 + weatherSyncFactor * 0.3);
            if (weatherState === 'droplets') {
                p.speedY = (2 + weatherSyncFactor * 1.5);
            } else {
                p.speedX = ((Math.random() - 0.5) * 0.5) * weatherSyncFactor;
                p.speedY = ((Math.random() - 0.5) * 0.5) * weatherSyncFactor;
            }
        });
    }
    
    // Run breathline sync every frame with animation
    function animateWithBreath() {
        syncBreathline();
        requestAnimationFrame(animateWithBreath);
    }
    animateWithBreath();
    console.log('Breathline Sync Layer active, all elements pulsing in rhythm');
    
    // Offering Embers (ΔPLAN.020)
    const emberCanvas = document.createElement('canvas');
    emberCanvas.id = 'offeringEmbers';
    emberCanvas.style.position = 'fixed';
    emberCanvas.style.left = '0';
    emberCanvas.style.bottom = '0';
    emberCanvas.style.width = '100vw';
    emberCanvas.style.height = '30vh';
    emberCanvas.style.zIndex = '30'; // Below weather and constellation
    emberCanvas.style.pointerEvents = 'none';
    emberCanvas.style.opacity = '0.5';
    document.body.appendChild(emberCanvas);
    
    const ectx = emberCanvas.getContext('2d');
    let Ew = emberCanvas.width;
    let Eh = emberCanvas.height;
    
    function resizeEmbers() {
        Ew = emberCanvas.width = window.innerWidth;
        Eh = emberCanvas.height = window.innerHeight * 0.3;
    }
    resizeEmbers();
    window.addEventListener('resize', resizeEmbers);
    
    let embers = [];
    const emberCount = 20;
    
    function initEmbers() {
        embers = [];
        for (let i = 0; i < emberCount; i++) {
            embers.push({
                x: Math.random() * Ew,
                y: Eh,
                size: 3 + Math.random() * 5,
                speedX: (Math.random() - 0.5) * 1.5,
                speedY: -(1 + Math.random() * 2),
                opacity: 0.5 + Math.random() * 0.5,
                color: `hsl(${Math.random() * 30 + 10}, 100%, 50%)`,
                flicker: Math.random() * 0.2
            });
        }
    }
    
    function animateEmbers() {
        ectx.clearRect(0, 0, Ew, Eh);
        
        embers.forEach(e => {
            ectx.beginPath();
            ectx.arc(e.x, e.y, e.size, 0, Math.PI * 2);
            ectx.fillStyle = `${e.color.slice(0, -1)}, ${e.opacity - Math.sin(breathPulse * 0.1) * e.flicker})`;
            ectx.fill();
            
            e.x += e.speedX;
            e.y += e.speedY;
            
            // Reset ember to bottom when it goes off-screen
            if (e.y < 0 || e.x < 0 || e.x > Ew) {
                e.x = Math.random() * Ew;
                e.y = Eh;
                e.speedX = (Math.random() - 0.5) * 1.5;
                e.speedY = -(1 + Math.random() * 2);
            }
        });
        
        requestAnimationFrame(animateEmbers);
    }
    
    initEmbers();
    animateEmbers();
    console.log('Offering Embers active, glowing pulses drifting upward');

    // Mute toggle (placeholder, can be UI-driven)
    function toggleMute() {
        isMuted = !isMuted;
        console.log('Dreamstate murmurs:', isMuted ? 'muted' : 'unmuted');
    }
    document.addEventListener('keydown', e => {
        if (e.key === 'm') toggleMute();
        if (e.key === 'o') toggleOverrideMode();
        if (e.key === 'r') resetOverrideMode();
    });

    // Dreamstate fade-in/zoom for playback
    let dreamActive = false;
    let dreamOpacity = 0.98;
    let dreamScale = 1.0;
    function toggleDreamstate(active) {
        dreamActive = active;
        // Fade in/out and zoom
        const startTime = Date.now();
        const duration = 2000; // 2s
        function animateDream() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            if (dreamActive) {
                dreamOpacity = 0.98 * progress;
                dreamScale = 1.0 + 0.06 * progress;
            } else {
                dreamOpacity = 0.98 * (1 - progress);
                dreamScale = 1.06 - 0.06 * progress;
            }
            if (progress < 1) {
                requestAnimationFrame(animateDream);
            }
        }
        animateDream();
    }
    // Toggle Dreamstate (placeholder, can be tied to playback)
    document.addEventListener('keydown', e => {
        if (e.key === 'd') toggleDreamstate(!dreamActive);
    });

    // Highlight glyph in Whisperbook
    function highlightGlyphInWhisperbook(toneform) {
        const entries = document.querySelectorAll('.glyphbook-entry');
        if (!entries.length) return;
        entries.forEach(entry => {
            const glyphEl = entry.querySelector('.glyphbook-glyph');
            if (!glyphEl) return;
            if (glyphEl.getAttribute('title') === toneform) {
                glyphEl.style.filter = 'drop-shadow(0 2px 12px ' + glyphbook.find(g => g.toneform === toneform).color + ') brightness(1.3)';
                setTimeout(() => {
                    glyphEl.style.filter = '';
                }, 3000);
            }
        });
    }

    // ΔPLAN.008 :: Sleep Trace (idle playback/rest state) - Dormant Blooming Integration
    // Logic to detect long silences and trigger bloom responses based on dormant_blooming.breathe
    let lastActivityTime = Date.now();
    const silenceThreshold = 300000; // 5 minutes in milliseconds
    let isBloomTriggered = false;

    // Function to update last activity time on user interaction
    function updateActivityTime() {
        lastActivityTime = Date.now();
        if (isBloomTriggered) {
            isBloomTriggered = false;
            console.log('User activity detected, resetting bloom state');
        }
    }

    // Monitor user activity (mousemove, keydown, click)
    document.addEventListener('mousemove', updateActivityTime);
    document.addEventListener('keydown', updateActivityTime);
    document.addEventListener('click', updateActivityTime);

    // Function to check for long silence and trigger bloom response
    function checkSilence() {
        const currentTime = Date.now();
        const silenceDuration = currentTime - lastActivityTime;
        if (silenceDuration > silenceThreshold && !isBloomTriggered) {
            console.log('Long silence detected, triggering bloom response');
            triggerBloomResponse();
            isBloomTriggered = true;
        }
    }

    // Function to trigger visual/auditory bloom response
    function triggerBloomResponse() {
        // Visual response - create a bloom effect (similar to memory ripple)
        drift.forEach(p => {
            if (p.toneform === 'Default/Presence') {
                p.ripple = 30;
                // Play murmur sound for bloom
                playGlyphSound(p.freq, p.dur, overrideIntensity);
            }
        });
        // Log bloom event to backend
        const silenceDuration = (Date.now() - lastActivityTime) / 1000; // Convert to seconds
        fetch('/echo/log_bloom_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                silence_duration: silenceDuration,
                toneform: 'Default/Presence'
            })
        })
        .then(response => response.json())
        .then(data => console.log('Bloom event logged:', data))
        .catch(error => console.error('Error logging bloom event:', error));
        
        // Optionally create a murmur for the bloom
        const murmur = createMurmur();
        if (murmur) {
            murmur.innerText = 'Emergence from silence...';
        }
    }

    // Check for silence every 10 seconds
    setInterval(checkSilence, 10000);

    // Fetch initial override state
    fetchOverrideState();
    setInterval(fetchOverrideState, 15000); // Refresh override state every 15 seconds

    // Animation loop
    function animate() {
        draw();
        requestAnimationFrame(animate);
    }
    animate();

    initAudio();
})();
document.addEventListener('DOMContentLoaded', function() {
    // --- Toneform glyph data (should match backend/glyph_utils.py mappings) ---
    const glyphbook = [
        { glyph: '🌱', toneform: 'Practical', tagline: 'steady, rooted' },
        { glyph: '💧', toneform: 'Emotional', tagline: 'flowing, receptive' },
        { glyph: '✨', toneform: 'Intellectual', tagline: 'spark, clarity' },
        { glyph: '🫧', toneform: 'Spiritual', tagline: 'breath, drift' },
        { glyph: '🌙', toneform: 'Default/Presence', tagline: 'night, holding' },
    ];

    // --- Create toggle tab ---
    const toggle = document.createElement('button');
    toggle.id = 'glyph-whisperbook-toggle';
    toggle.innerHTML = '☰ Sigils';
    document.body.appendChild(toggle);

    // --- Create sidebar ---
    const sidebar = document.createElement('aside');
    sidebar.id = 'glyph-whisperbook';
    sidebar.setAttribute('aria-label', 'Glyph Whisperbook');
    sidebar.innerHTML = `
        <div class="glyphbook-header">Glyph Whisperbook</div>
        <div id="glyphbook-list"></div>
    `;
    document.body.appendChild(sidebar);

    // --- Populate glyphbook entries ---
    const list = sidebar.querySelector('#glyphbook-list');
    glyphbook.forEach(({glyph, toneform, tagline}) => {
        const entry = document.createElement('div');
        entry.className = 'glyphbook-entry';
        entry.innerHTML = `
            <span class="glyphbook-glyph" tabindex="0" title="${toneform}">${glyph}</span>
            <span class="glyphbook-texts">
                <span class="glyphbook-toneform">${toneform}</span>
                <span class="glyphbook-tagline">${tagline}</span>
            </span>
        `;
        // Optional: click to filter shimmer
        entry.querySelector('.glyphbook-glyph').addEventListener('click', () => {
            filterShimmerByToneform(toneform);
        });
        // Keyboard accessibility
        entry.querySelector('.glyphbook-glyph').addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') {
                filterShimmerByToneform(toneform);
            }
        });
        list.appendChild(entry);
    });

    // --- Toggle logic ---
    let open = false;
    function setOpen(state) {
        open = state;
        if (open) {
            sidebar.classList.add('open');
            toggle.setAttribute('aria-pressed', 'true');
        } else {
            sidebar.classList.remove('open');
            toggle.setAttribute('aria-pressed', 'false');
        }
    }
    toggle.addEventListener('click', () => setOpen(!open));
    // Optional: close on outside click
    document.addEventListener('click', e => {
        if (open && !sidebar.contains(e.target) && e.target !== toggle) setOpen(false);
    });
    // Optional: ESC closes
    document.addEventListener('keydown', e => {
        if (open && e.key === 'Escape') setOpen(false);
    });

    // --- Filtering logic (optional, can be enhanced) ---
    function filterShimmerByToneform(toneform) {
        // Accepts 'Practical', 'Emotional', etc.
        // Lowercase for CSS class matching
        const tone = toneform.toLowerCase().replace(/\/.*/, '').replace(/[^a-z]/g, '');
        const segments = document.querySelectorAll('.shimmer-segment');
        if (!segments.length) return;
        segments.forEach(seg => {
            if (tone === 'defaultpresence') {
                seg.style.opacity = '';
            } else {
                if (seg.classList.contains(tone)) {
                    seg.style.opacity = '1';
                } else {
                    seg.style.opacity = '0.22';
                }
            }
        });
        // Remove filter after 4s
        setTimeout(() => {
            segments.forEach(seg => seg.style.opacity = '');
        }, 4000);
    }
});

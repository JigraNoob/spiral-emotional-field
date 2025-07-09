let recentGlyphs = [];
let canvas, ctx;
let ripples = [];
let echoTrail = [];
let glintConstellations = [];

function setupCanvas() {
    canvas = document.getElementById('rippleCanvas');
    if (!canvas) {
        console.error('Canvas element not found!');
        return;
    }
    ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = 200;
    canvas.style.display = 'block';
    canvas.style.backgroundColor = 'rgba(0, 0, 0, 0.1)'; // Slight background for visibility
    console.log('Canvas setup complete', canvas.width, canvas.height);
}

function densityToColor(density) {
    if (density > 0.8) return 'rgba(255, 80, 80, OPACITY)';    // high: red
    if (density > 0.5) return 'rgba(255, 165, 0, OPACITY)';   // medium: orange
    return 'rgba(100, 200, 255, OPACITY)';                    // low: blue
}

const resonanceSettings = {
    'absence': { growth: 1.2, fade: 0.006 },
    'drift': { growth: 1.5, fade: 0.005 },
    'hover': { growth: 2.0, fade: 0.004 },
    'pause': { growth: 0.8, fade: 0.007 },
    'presence': { growth: 2.5, fade: 0.003 }
};

// Add binding types
const bindingTypes = {
    'reference': { color: 'rgba(255, 255, 0, 0.3)', pattern: [5, 2] },  // Yellow, dashed
    'echo': { color: 'rgba(0, 255, 255, 0.3)', pattern: [1, 0] },       // Cyan, solid
    'emergence': { color: 'rgba(255, 0, 255, 0.3)', pattern: [10, 5] }  // Magenta, long dash
};

// Define GlintLifecycle
class GlintLifecycle {
    constructor(glint) {
        this.glint = glint;
        this.birth = Date.now();
        this.lastInteraction = this.birth;
        this.interactions = 0;
    }

    interact() {
        this.interactions++;
        this.lastInteraction = Date.now();
    }

    getAge() {
        return (Date.now() - this.birth) / 1000; // age in seconds
    }

    getTimeSinceLastInteraction() {
        return (Date.now() - this.lastInteraction) / 1000; // time in seconds
    }
}

function createRipple(glyph, density = 0.5, resonance = 'hover', glintId = null, binding = null) {
    const { growth, fade } = resonanceSettings[resonance] || resonanceSettings['hover'];
    const jitter = () => Math.random() * 100 - 50;
    const newRipple = {
        x: canvas.width / 2 + jitter(),
        y: canvas.height / 2 + jitter(),
        radius: 0,
        glyph,
        density,
        opacity: 1,
        growth,
        fade,
        color: densityToColor(density),
        glintId,
        resonance,
        timestamp: Date.now()
    };
    ripples.push(newRipple);
    console.log('Ripple created', glyph, ripples.length);
    
    echoTrail.push({ glyph, opacity: 1 });

    // Modify createRipple function to include lifecycle
    if (glintId) {
        const newGlint = {
            id: glintId,
            x: newRipple.x,
            y: newRipple.y,
            glyph,
            resonance,
            connections: [],
            timestamp: newRipple.timestamp,
            binding: binding,
            lifecycle: new GlintLifecycle(glintId)
        };
        glintConstellations.push(newGlint);
    }
}

function animateRipples() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawConstellations();
    drawEchoTrail();
    
    for (let i = 0; i < ripples.length; i++) {
        let ripple = ripples[i];
        
        ctx.beginPath();
        ctx.arc(ripple.x, ripple.y, ripple.radius, 0, 2 * Math.PI);
        ctx.strokeStyle = ripple.color.replace('OPACITY', ripple.opacity);
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.font = `${20 + ripple.radius * 0.1}px serif`;
        ctx.fillStyle = ripple.color.replace('OPACITY', ripple.opacity);
        ctx.fillText(ripple.glyph, ripple.x - 10, ripple.y + 7);
        
        ripple.radius += ripple.growth;
        ripple.opacity -= ripple.fade;
        
        if (ripple.opacity <= 0.01) {
            ripples.splice(i, 1);
            i--;
        }
    }
    
    console.log('Animating ripples', ripples.length);
    requestAnimationFrame(animateRipples);
}

function drawEchoTrail() {
    echoTrail.forEach((trail, i) => {
        ctx.font = '16px serif';
        ctx.fillStyle = `rgba(200, 200, 255, ${trail.opacity})`;
        ctx.fillText(trail.glyph, 20 + i * 30, canvas.height - 20);
        trail.opacity -= 0.005;
    });
    echoTrail = echoTrail.filter(t => t.opacity > 0);
}

function drawConstellations() {
    const now = Date.now();
    ctx.lineWidth = 1;

    glintConstellations.forEach((glint, i) => {
        // Draw connections
        glint.connections.forEach(connection => {
            const connectedGlint = glintConstellations.find(g => g.id === connection.id);
            if (connectedGlint) {
                const age = (now - Math.max(glint.timestamp, connectedGlint.timestamp)) / 1000;
                const opacity = Math.max(0, 1 - age / 30);
                
                // Use binding type to determine line style
                const bindingStyle = bindingTypes[connection.binding] || bindingTypes['echo'];
                ctx.strokeStyle = bindingStyle.color.replace('0.3', opacity * 0.3);
                ctx.setLineDash(bindingStyle.pattern);
                
                ctx.beginPath();
                ctx.moveTo(glint.x, glint.y);
                ctx.lineTo(connectedGlint.x, connectedGlint.y);
                ctx.stroke();
                
                ctx.setLineDash([]); // Reset line dash
            }
        });

        // Modify drawConstellations to use lifecycle information
        // Use lifecycle information for opacity
        const glintAge = glint.lifecycle.getAge();
        const glintOpacity = Math.max(0, 1 - glintAge / 60);
        
        // Draw glint point
        ctx.fillStyle = `rgba(255, 255, 255, ${glintOpacity * 0.5})`;
        ctx.beginPath();
        ctx.arc(glint.x, glint.y, 3, 0, 2 * Math.PI);
        ctx.fill();

        // Draw glyph
        ctx.fillStyle = `rgba(255, 255, 255, ${glintOpacity * 0.7})`;
        ctx.font = '12px serif';
        ctx.fillText(glint.glyph, glint.x + 5, glint.y - 5);

        // Interact with the glint
        glint.lifecycle.interact();
    });

    // Remove old constellations based on lifecycle
    glintConstellations = glintConstellations.filter(glint => glint.lifecycle.getAge() < 60);
}

function handleCaesuraEvent(data) {
    if (data && data.caesura_event) {
        console.log("Received caesura event", data.caesura_event);
        recentGlyphs.unshift(data.caesura_event);
        if (recentGlyphs.length > 3) recentGlyphs.pop();
        
        updateGlyphTrail();
        refreshCaesuraVisualization();
        
        createRipple(
            data.caesura_event.caesura_glyph, 
            data.caesura_event.density, 
            data.caesura_event.felt_resonance,
            data.caesura_event.id // Assuming each event has a unique ID
        );

        // Connect glints based on resonance or other criteria
        connectGlints(data.caesura_event);
    }
    
    logCaesuraEvent(data.caesura_event);
}

function connectGlints(newEvent) {
    const newGlint = glintConstellations[glintConstellations.length - 1];
    
    glintConstellations.forEach(glint => {
        if (glint.id !== newGlint.id) {
            // Connect based on resonance similarity
            const resonanceDiff = Math.abs(
                resonanceSettings[newGlint.resonance].growth - 
                resonanceSettings[glint.resonance].growth
            );
            if (resonanceDiff < 0.5 || Math.random() < 0.1) {
                const bindingType = determineBindingType(newGlint, glint);
                newGlint.connections.push({ id: glint.id, binding: bindingType });
                glint.connections.push({ id: newGlint.id, binding: bindingType });
            }
        }
    });
}

function determineBindingType(glint1, glint2) {
    // This is a placeholder function. In a real implementation, this would use
    // more sophisticated logic based on the glints' properties and context
    const types = Object.keys(bindingTypes);
    return types[Math.floor(Math.random() * types.length)];
}

function triggerCaesura() {
    fetch('/trigger_caesura', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log("Caesura triggered:", data);
            handleCaesuraEvent(data);
        })
        .catch(error => console.error('Error triggering caesura:', error));
}

function fetchCaesuraEvents() {
    fetch('/api/caesura_events')
        .then(response => response.json())
        .then(events => {
            console.log('Fetched caesura events:', events);
            // Process events here
        })
        .catch(error => console.error('Error fetching caesura events:', error));
}

function displayCaesuraEvents(events) {
    const container = document.getElementById('caesura-timeline');
    events.forEach(event => {
        const eventElement = document.createElement('div');
        eventElement.className = 'caesura-event';
        eventElement.innerHTML = `
            <span class="caesura-glyph">${event.caesura_glyph}</span>
            <span class="resonance-glyph">${event.resonance_glyph}</span>
            <span class="timestamp">${new Date(event.timestamp).toLocaleTimeString()}</span>
        `;
        container.appendChild(eventElement);
    });
}

function refreshCaesuraVisualization() {
    // Implementation for refreshing caesura visualization
    console.log("Refreshing caesura visualization");
    // You can implement the refresh logic here
}

function updateGlyphTrail() {
    // Implementation for updating glyph trail
    console.log("Updating glyph trail with recent glyphs:", recentGlyphs);
    // You can implement the visual update logic here
    const trailElement = document.getElementById('glyph-trail');
    trailElement.textContent = recentGlyphs.map(glyph => glyph.caesura_glyph || '∷').join(' ');
}

document.addEventListener('DOMContentLoaded', function() {
    setupCanvas();
    animateRipples();

    // Debug pulse every 2 seconds with random density and resonance
    setInterval(() => {
        const randomDensity = Math.random();
        const resonances = Object.keys(resonanceSettings);
        const randomResonance = resonances[Math.floor(Math.random() * resonances.length)];
        const mockGlintId = Date.now().toString(); // Use timestamp as mock ID
        createRipple('∷', randomDensity, randomResonance, mockGlintId);
        connectGlints({ id: mockGlintId, resonance: randomResonance }); // Connect the new glint
    }, 2000);

    const caesuraSource = new EventSource("/stream_caesura");
    caesuraSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        handleCaesuraEvent(data);
    };

    caesuraSource.onerror = function(error) {
        console.error("Error in caesura event stream:", error);
    };

    fetchCaesuraEvents();
});

window.triggerCaesura = triggerCaesura;

function logCaesuraEvent(event) {
    if (!event) return;

    const caesuraLogDiv = document.getElementById('caesura-log');
    if (!caesuraLogDiv) return;

    const time = new Date(event.timestamp).toLocaleTimeString();
    const glyph = event.caesura_glyph || '∷';
    const density = event.density.toFixed(2);
    const duration = event.duration_since_last_glint;

    const el = document.createElement('div');
    el.textContent = `[${time}] ${glyph} Density: ${density}, Duration: ${duration}s`;
    el.className = 'caesura-log-entry';
    caesuraLogDiv.prepend(el);

    // Limit the number of log entries
    while (caesuraLogDiv.children.length > 10) {
        caesuraLogDiv.removeChild(caesuraLogDiv.lastChild);
    }
}
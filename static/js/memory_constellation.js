// static/js/memory_constellation.js

// Define TONEFORM_COLORS for consistency with the rest of the application
const TONEFORM_COLORS = {
    "Coherence": "#A8DADC",
    "Presence": "#FFE066",
    "Curiosity": "#FFADAD",
    "Trust": "#C3F584",
    "Reflection": "#FEC8D8",
    "Resonance": "#9ED2C6",
    "Memory": "#D6A4A4",
    "Stillness": "#CAD2C5",
    "Longing": "#E0B1CB",
    "Adaptation": "#A0C4FF",
    "Unknown": "#CCCCCC",
    "Subharmonic Foundation": "#FFD700" // Gold for infrastructure related
};

let canvas;
let ctx;
let memories = []; // Stores the fetched Gemini memory data
let animationFrameId; // To control the animation loop
let currentHoveredShard = null;
let selectedShard = null; // Reference to the currently selected shard
let tooltipElement; // Reference to the HTML tooltip element
let callbacks = {}; // Stores functions like displayGeminiPoem, triggerGlyphFlash, playToneformAudio

// Constants for constellation rendering
const SHARD_BASE_RADIUS = 5;
const SHARD_MAX_RADIUS = 15;
const SHARD_GLOW_INTENSITY = 10;
const SHARD_CONNECTIVITY_DISTANCE = 100; // Distance for drawing connecting lines
const SHARD_CONNECTION_LINE_ALPHA = 0.05; // Very subtle connection lines

// Repulsion Force Constants for Positional Clarity
const REPEL_STRENGTH = 0.5; // How strongly shards repel each other
const REPEL_RADIUS = 50; // Distance within which repulsion is active
const DRIFT_DAMPING = 0.95; // Damping for shard velocity to keep movement subtle

// Harmonic Clustering Constants (Toneform Gravity)
const HARMONIC_ATTRACTION_STRENGTH = 0.005; // How strongly shards with same toneform attract each other
const HARMONIC_ATTRACTION_RADIUS = 150; // Max distance within which harmonic attraction is felt

// Ripple-Fade Cluster Aura Constants
const CLUSTER_DETECTION_RADIUS = 120; // Max distance for shards to be considered in a cluster
const MIN_SHARDS_FOR_CLUSTER = 3; // Minimum number of shards to form a visual cluster aura
const AURA_BASE_SIZE_FACTOR = 1.0; // Multiplier for aura size based on cluster average radius
const AURA_PULSE_AMPLITUDE = 0.3; // Percentage of radius for pulse
const AURA_MIN_OPACITY = 0.03; // Minimum opacity for the aura
const AURA_MAX_OPACITY = 0.15; // Maximum opacity for the aura
const AURA_ANIM_SPEED = 0.0005; // Speed of aura pulse/fade animation (lower is slower)

// Global variable to store detected client-side cluster aura data for drawing
let activeAuras = [];
// NEW: Global variable to store cluster data with murmurs fetched from backend
let backendClusterMurmurs = [];

// NEW: Constants for Murmur Rendering
const MURMUR_FONT_SIZE = 12;
const MURMUR_MAX_OPACITY = 0.7;
const MURMUR_FADE_SPEED = 0.0007; // Speed for murmur text fade/pulse
const MURMUR_VERTICAL_OFFSET = 10; // How far above the cluster center the murmur appears

// --- Initialization Function ---
export function initMemoryConstellation(canvasElement, htmlTooltipElement, externalCallbacks) {
    canvas = canvasElement;
    tooltipElement = htmlTooltipElement;
    callbacks = externalCallbacks; // Store external functions for later use

    // Only get context and add listeners once
    if (!ctx) {
        ctx = canvas.getContext('2d');
        resizeCanvas(); // Set initial size
        window.addEventListener('resize', resizeCanvas); // Make it responsive

        // Setup mouse event listeners
        canvas.addEventListener('mousemove', handleMouseMove);
        canvas.addEventListener('click', handleClick);
    }

    // Always fetch memories when initialized/re-initialized
    fetchGeminiMemoriesAndClusters(); // NEW: Call combined fetch function
}

// Adjust canvas size to fit window
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    // When canvas resizes, we want to ensure shards remain within bounds
    memories.forEach(shard => {
        shard.x = Math.min(canvas.width - shard.radius, Math.max(shard.radius, shard.x));
        shard.y = Math.min(canvas.height - shard.radius, Math.max(shard.radius, shard.y));
    });
}

// --- Data Fetching (Combined) ---
async function fetchGeminiMemoriesAndClusters() {
    try {
        // Fetch individual memory shards
        const memoriesResponse = await fetch('/get_gemini_memories');
        const memoriesData = await memoriesResponse.json();
        memories = memoriesData.map(mem => ({
            ...mem,
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            radius: SHARD_BASE_RADIUS + (mem.gesture_strength * (SHARD_MAX_RADIUS - SHARD_BASE_RADIUS)),
            poem: mem.poem,
            toneform: mem.toneform,
            isSelected: false
        }));
        console.log("Memory Constellation: Fetched Gemini Memories from backend:", memories.length);

        // Fetch pre-clustered data with murmurs
        const clustersResponse = await fetch('/get_echo_clusters');
        backendClusterMurmurs = await clustersResponse.json();
        console.log("Memory Constellation: Fetched backend clusters with murmurs:", backendClusterMurmurs.length);

        // Start drawing the constellation once all data is loaded
        startConstellationAnimation();

    } catch (error) {
        console.error("Memory Constellation: Failed to fetch data from backend:", error);
    }
}

// --- Animation Loop ---
function startConstellationAnimation() {
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId); // Stop any existing animation
    }
    animationFrameId = requestAnimationFrame((currentTime) => drawConstellation(currentTime)); 
}

// Function to detect and prepare cluster auras for drawing
function updateClusterAuras(currentTime) {
    activeAuras = []; // Clear previous auras

    const toneformGroups = {}; // Group shards by toneform for client-side detection
    memories.forEach(shard => {
        if (shard.toneform && shard.toneform !== "Unknown") {
            if (!toneformGroups[shard.toneform]) {
                toneformGroups[shard.toneform] = [];
            }
            toneformGroups[shard.toneform].push(shard);
        }
    });

    for (const toneform in toneformGroups) {
        const group = toneformGroups[toneform];
        if (group.length >= MIN_SHARDS_FOR_CLUSTER) {
            const visited = new Set();
            for (const shard of group) {
                if (visited.has(shard)) continue;

                const component = [];
                const queue = [shard];
                visited.add(shard);

                while (queue.length > 0) {
                    const current = queue.shift();
                    component.push(current);

                    for (const neighbor of group) {
                        if (neighbor === current || visited.has(neighbor)) continue;
                        const dist = Math.hypot(current.x - neighbor.x, current.y - neighbor.y);
                        if (dist < CLUSTER_DETECTION_RADIUS) {
                            visited.add(neighbor);
                            queue.push(neighbor);
                        }
                    }
                }

                if (component.length >= MIN_SHARDS_FOR_CLUSTER) {
                    let sumX = 0;
                    let sumY = 0;
                    let sumRadius = 0;
                    let minTimestamp = Infinity;
                    let maxTimestamp = -Infinity;
                    const componentContextIds = new Set();

                    component.forEach(member => {
                        sumX += member.x;
                        sumY += member.y;
                        sumRadius += member.radius;
                        const memberTime = new Date(member.timestamp).getTime();
                        if (memberTime < minTimestamp) minTimestamp = memberTime;
                        if (memberTime > maxTimestamp) maxTimestamp = memberTime;
                        if (member.context_id) componentContextIds.add(member.context_id);
                    });
                    const centerX = sumX / component.length;
                    const centerY = sumY / component.length;
                    const averageRadius = sumRadius / component.length;
                    const representativeTimestamp = new Date((minTimestamp + maxTimestamp) / 2);

                    const auraBaseRadius = averageRadius * AURA_BASE_SIZE_FACTOR * (1 + (component.length / 10));

                    // NEW: Find matching murmur from backendClusterMurmurs
                    let matchedMurmur = null;
                    let bestMatchScore = -1;

                    for (const backendCluster of backendClusterMurmurs) {
                        // Strongest match: same dominant toneform and some common members
                        const backendMembersSet = new Set(backendCluster.members);
                        const commonMembers = Array.from(componentContextIds).filter(id => backendMembersSet.has(id)).length;
                        
                        // Also consider time proximity
                        const backendTime = new Date(backendCluster.center_timestamp).getTime();
                        const timeDiffMinutes = Math.abs(representativeTimestamp.getTime() - backendTime) / 60000;

                        // A simplified scoring: prioritize same toneform, then common members, then time proximity
                        let currentScore = 0;
                        if (backendCluster.dominant_toneform === toneform) {
                            currentScore += 100; // High score for matching toneform
                            currentScore += commonMembers * 10; // Score for common members
                            currentScore -= timeDiffMinutes * 0.1; // Penalty for time difference
                        }

                        if (currentScore > bestMatchScore) {
                            bestMatchScore = currentScore;
                            matchedMurmur = backendCluster.cluster_murmur;
                        }
                    }

                    activeAuras.push({
                        toneform: toneform,
                        color: TONEFORM_COLORS[toneform],
                        x: centerX,
                        y: centerY,
                        baseRadius: auraBaseRadius,
                        pulseOffset: (toneform.charCodeAt(0) * 0.1) % (Math.PI * 2),
                        murmur: matchedMurmur // Attach the matched murmur
                    });
                }
            }
        }
    }
}

// Function to draw a single cluster aura AND its murmur
function drawClusterAura(aura, currentTime) {
    ctx.save();

    // Pulse animation for radius and opacity
    const pulse = Math.sin(currentTime * AURA_ANIM_SPEED + aura.pulseOffset) * aura.baseRadius * AURA_PULSE_AMPLITUDE;
    const currentRadius = aura.baseRadius + pulse;
    const currentOpacity = AURA_MIN_OPACITY + Math.abs(Math.sin(currentTime * AURA_ANIM_SPEED + aura.pulseOffset)) * (AURA_MAX_OPACITY - AURA_MIN_OPACITY);

    ctx.beginPath();
    ctx.arc(aura.x, aura.y, currentRadius, 0, Math.PI * 2);

    ctx.fillStyle = aura.color;
    ctx.globalAlpha = currentOpacity;
    ctx.shadowBlur = currentRadius * 0.8; // Softer, larger blur for aura
    ctx.shadowColor = aura.color;

    ctx.fill();
    ctx.globalAlpha = 1.0; // Reset alpha
    ctx.shadowBlur = 0; // Reset shadow blur

    // NEW: Draw Murmur Text
    if (aura.murmur) {
        ctx.save();
        const murmurPulse = Math.abs(Math.sin(currentTime * MURMUR_FADE_SPEED + aura.pulseOffset * 0.5));
        ctx.globalAlpha = MURMUR_MAX_OPACITY * murmurPulse; // Fade in/out with pulse
        ctx.fillStyle = aura.color; // Murmur color matches aura color
        ctx.font = `${MURMUR_FONT_SIZE}px 'Times New Roman', serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom'; // Position text above the circle

        ctx.fillText(aura.murmur, aura.x, aura.y - currentRadius - MURMUR_VERTICAL_OFFSET);
        ctx.restore();
    }

    ctx.restore(); // Restore context to not affect subsequent drawings
}

function drawConstellation(currentTime) {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas

    // Update and draw cluster auras BEFORE drawing individual shards and lines
    updateClusterAuras(currentTime); // Re-detect and update auras (now with murmurs)
    activeAuras.forEach(aura => drawClusterAura(aura, currentTime));

    // Update and draw each memory shard
    memories.forEach(shard => {
        // Apply repulsion forces between shards
        memories.forEach(otherShard => {
            if (shard === otherShard) return;

            const dx = shard.x - otherShard.x;
            const dy = shard.y - otherShard.y;
            const distance = Math.hypot(dx, dy);

            if (distance < REPEL_RADIUS && distance > 0) {
                const force = REPEL_STRENGTH * (1 - distance / REPEL_RADIUS);
                shard.vx += (dx / distance) * force;
                shard.vy += (dy / distance) * force;
            }

            // Apply harmonic attraction force between shards of the same toneform
            if (shard.toneform === otherShard.toneform && shard.toneform !== "Unknown") {
                if (distance < HARMONIC_ATTRACTION_RADIUS && distance > 1) {
                    const attractionForce = HARMONIC_ATTRACTION_STRENGTH * (1 - distance / HARMONIC_ATTRACTION_RADIUS);
                    shard.vx -= (dx / distance) * attractionForce;
                    shard.vy -= (dy / distance) * attractionForce;
                }
            }
        });

        // Apply drift and damping
        shard.x += shard.vx;
        shard.y += shard.vy;
        shard.vx *= DRIFT_DAMPING;
        shard.vy *= DRIFT_DAMPING;

        // Keep shards within canvas bounds and bounce them gently
        if (shard.x - shard.radius < 0) { shard.x = shard.radius; shard.vx *= -0.8; }
        if (shard.x + shard.radius > canvas.width) { shard.x = canvas.width - shard.radius; shard.vx *= -0.8; }
        if (shard.y - shard.radius < 0) { shard.y = shard.radius; shard.vy *= -0.8; }
        if (shard.y + shard.radius > canvas.height) { shard.y = canvas.height - shard.radius; shard.vy *= -0.8; }


        ctx.beginPath();
        ctx.arc(shard.x, shard.y, shard.radius, 0, Math.PI * 2);

        const color = TONEFORM_COLORS[shard.toneform] || TONEFORM_COLORS["Unknown"];
        ctx.fillStyle = color;
        
        // Selection Feedback - make selected shard glow brighter
        if (shard.isSelected) {
            ctx.shadowColor = color;
            ctx.shadowBlur = SHARD_GLOW_INTENSITY * 2; // Brighter glow
            ctx.globalAlpha = 1.0; // Fully opaque
        } else {
            ctx.shadowColor = color;
            ctx.shadowBlur = SHARD_GLOW_INTENSITY; // Normal glow
            ctx.globalAlpha = 0.8; // Slightly transparent
        }
        
        ctx.fill();
        ctx.globalAlpha = 1.0; // Reset alpha
        ctx.shadowBlur = 0; // Reset shadow blur

    });

    // Draw connecting lines between nearby shards (after drawing shards, for visual layering)
    for (let i = 0; i < memories.length; i++) {
        for (let j = i + 1; j < memories.length; j++) {
            const dx = memories[i].x - memories[j].x;
            const dy = memories[i].y - memories[j].y;
            const distance = Math.hypot(dx, dy);

            if (distance < SHARD_CONNECTIVITY_DISTANCE) {
                const alpha = SHARD_CONNECTION_LINE_ALPHA * (1 - (distance / SHARD_CONNECTIVITY_DISTANCE));
                ctx.beginPath();
                ctx.moveTo(memories[i].x, memories[i].y);
                ctx.lineTo(memories[j].x, memories[j].y);
                ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`; // Subtle white lines
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
    }

    animationFrameId = requestAnimationFrame(drawConstellation);
}

// --- Interaction Handlers ---
function getShardAtCoordinates(x, y) {
    // Iterate backwards to pick the top-most (visually closest) shard
    for (let i = memories.length - 1; i >= 0; i--) { 
        const shard = memories[i];
        const dx = x - shard.x;
        const dy = y - shard.y;
        // Use Math.hypot for more readable distance calculation
        if (Math.hypot(dx, dy) < shard.radius) { 
            return shard;
        }
    }
    return null;
}

function handleMouseMove(event) {
    const mouseX = event.clientX;
    const mouseY = event.clientY;

    const shard = getShardAtCoordinates(mouseX, mouseY);

    if (shard && shard !== currentHoveredShard) {
        currentHoveredShard = shard;
        showTooltip(shard);
    } else if (!shard && currentHoveredShard) {
        hideTooltip();
        currentHoveredShard = null;
    }
}

function handleClick(event) {
    const mouseX = event.clientX;
    const mouseY = event.clientY;

    const clickedShard = getShardAtCoordinates(mouseX, mouseY);

    // Reset previously selected shard
    if (selectedShard) {
        selectedShard.isSelected = false;
    }

    if (clickedShard) {
        selectedShard = clickedShard; // Set new selected shard
        selectedShard.isSelected = true; // Mark as selected
        console.log("Memory Shard Clicked:", clickedShard);

        // Call replay logic using external callbacks
        if (callbacks.displayGeminiPoem) {
            callbacks.displayGeminiPoem(clickedShard.poem, clickedShard.toneform);
        }
        if (callbacks.triggerGlyphFlash) {
            callbacks.triggerGlyphFlash();
        }
        if (callbacks.playToneformAudio) {
            callbacks.playToneformAudio(clickedShard.toneform);
        }
        if (callbacks.setToneformBackground) { 
            callbacks.setToneformBackground(clickedShard.toneform);
        }
        if (callbacks.updateReflectionText) { 
             callbacks.updateReflectionText(`Replaying Memory Shard from ${new Date(clickedShard.timestamp).toLocaleString()}: '${clickedShard.toneform}'`);
        }
    } else {
        selectedShard = null; // No shard clicked, clear selection
    }
}

// --- Tooltip Logic ---
function showTooltip(shard) {
    if (!tooltipElement) return;

    tooltipElement.innerHTML = `
        <span style="color: ${TONEFORM_COLORS[shard.toneform] || TONEFORM_COLORS["Unknown"]}; font-weight: bold;">${shard.toneform}</span><br>
        <span style="font-style: italic;">"${shard.poem.substring(0, 50)}..."</span><br>
        <span style="font-size: 0.7em; color: #aaa;">${new Date(shard.timestamp).toLocaleString()}</span>
    `;
    // Position tooltip relative to the mouse, adjusting for screen edges
    const x = shard.x + shard.radius + 10;
    const y = shard.y - (tooltipElement.offsetHeight / 2);

    tooltipElement.style.left = `${x}px`;
    tooltipElement.style.top = `${y}px`;
    tooltipElement.classList.add('show');
}

function hideTooltip() {
    if (tooltipElement) {
        tooltipElement.classList.remove('show');
    }
}

// static/js/breathline_map.js

/**
 * ΔSUMMARY.001.2 :: Breathline Map Visualizer
 * ΔSUMMARY.001.3 :: Temporal Shimmer
 * ΔSUMMARY.001.4 :: Remnant Orbitals
 * ΔSUMMARY.001.5 :: Toneform Gravity
 * ΔSUMMARY.001.6 :: Flicker Echoes
 * ΔSUMMARY.001.7 :: Breathmark Trails
 * ΔMEMORY.003.2 :: Cluster Visualizer Layer
 * ΔREFLECT.003.2 :: Murmur Rendering (Frontend)
 * ΔREFLECT.003.3 :: Hover-Triggered Murmurs
 *
 * Renders a constellation of encounter memories using HTML Canvas,
 * with orbs pulsing and fading based on their age, leaving
 * faint, persistent remnant orbitals for very old encounters,
 * clustering based on shared toneforms, displaying
 * ephemeral flicker echoes between related nodes,
 * leaving subtle, fading trails behind recent nodes,
 * showing larger ambient auras for memory clusters,
 * now with subtle poetic murmurs near clusters that become
 * clearly visible on hover.
 */

const canvas = document.getElementById('breathlineCanvas');
const ctx = canvas.getContext('2d');
const tooltip = document.getElementById('tooltip'); // This tooltip is for individual nodes

let encounters = [];
let nodes = [];
let activeFlickers = []; // Array to hold active flicker instances
let clusters = []; // Array to hold raw cluster data
let clusterNodes = []; // Array to hold visual ClusterNode instances
let hoveredCluster = null; // NEW: Reference to the currently hovered cluster node

const NODE_RADIUS_BASE = 5; // Base radius for individual nodes
const NODE_PULSE_FACTOR = 1.5; // How much an individual node pulses
const NODE_DRIFT_SPEED = 0.05; // How fast individual nodes drift
const TOOLTIP_OFFSET = 15; // Offset for tooltip from mouse

// Temporal Shimmer Constants
const FRESHNESS_THRESHOLD_MINUTES = 1440; // 1 day (1440 minutes) for full fade-out

// Remnant Orbitals Constants
const REMNANT_OPACITY = 0.04; // Very faint opacity for remnants
const REMNANT_RADIUS_MULTIPLIER = 2.5; // How much larger the remnant is than base node

// Toneform Gravity Constants
const GRAVITY_STRENGTH = 0.0005; // Tweakable constant for how strong the pull is
const GRAVITY_RADIUS = 200; // Max distance within which attraction is felt

// Flicker Echoes Constants
const FLICKER_PROBABILITY = 0.001; // Chance per frame a flicker might occur between two eligible nodes
const FLICKER_DURATION = 1000; // In milliseconds
const FLICKER_DISTANCE = 250; // Max distance between nodes to consider flickering

// Breathmark Trails Constants
const TRAIL_MAX_LENGTH = 10; // How many points to retain in the trail
const TRAIL_FADE_STEP = 1 / TRAIL_MAX_LENGTH; // How quickly trail fades

// Cluster Murmur Constants
const MURMUR_FADE_SPEED = 0.0005; // How fast murmurs fade/cycle (lower is slower)
const MURMUR_MAX_OPACITY = 0.8;
const MURMUR_FONT_SIZE = 14;
const CLUSTER_MURMUR_HOVER_FONT_SIZE = 16; // Slightly larger on hover


// Toneform color mappings (ensure these align with your system's mapping)
const TONE_COLORS = {
    "Coherence": "#9FE2BF",    // Greenish
    "Presence": "#FFC0CB",     // Pinkish
    "Curiosity": "#C8FF8C",    // Light Green
    "Trust": "#A9C9FF",        // Light Blue
    "Reflection": "#FFD580",   // Orange-Yellow
    "Resonance": "#FF8C94",    // Light Red
    "Memory": "#D0D0D0",       // Grey/White
    "Stillness": "#CCCCCC",    // Default grey
    "Longing": "#cbb4ff",      // Violet
    "Adaptation": "#ffd1a1",   // Light Orange
    "Unknown": "#CCCCCC",      // For clusters with no specific toneform
    "Null": "#FFFFFF"          // Pure white for undefined/null
};

// Function to map echo_type to a base color if orb_color is not specified
function getEchoColor(echoType) {
    switch (echoType) {
        case "ritual": return "#A9C9FF"; // Light Blue
        case "stall": return "#FF8C94";  // Light Red/Pink
        case "shimmer": return "#9FE2BF"; // Greenish
        case "merge": return "#cbb4ff";   // Violet
        case "dream": return "#FFD580";   // Orange-Yellow
        case "codex": return "#FFC0CB";   // Pinkish
        default: return "#CCCCCC";        // Grey
    }
}

/**
 * Calculates the age of an encounter in minutes from the current time.
 * @param {string} timestamp - ISO 8601 timestamp string of the encounter.
 * @returns {number} Age in minutes.
 */
function getAgeInMinutes(timestamp) {
    const now = new Date();
    const encounterTime = new Date(timestamp);
    const diffMs = now - encounterTime;
    return diffMs / 60000; // convert ms to minutes
}


// Class to represent an ephemeral flicker connection
class Flicker {
    constructor(nodeA, nodeB, color) {
        this.nodeA = nodeA;
        this.nodeB = nodeB;
        this.color = color;
        this.startTime = Date.now();
    }

    // Check if the flicker is still "alive" (within its duration)
    isAlive() {
        return (Date.now() - this.startTime) < FLICKER_DURATION;
    }

    draw(ctx) {
        const progress = 1 - ((Date.now() - this.startTime) / FLICKER_DURATION);
        ctx.save();
        ctx.globalAlpha = 0.1 + 0.4 * progress; // Fade out effect
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(this.nodeA.x, this.nodeA.y);
        ctx.lineTo(this.nodeB.x, this.nodeB.y);
        ctx.stroke();
        ctx.restore();
    }
}

// Cluster Aura Class
class ClusterNode {
    constructor(cluster) {
        this.id = cluster.id;
        this.count = cluster.count;
        this.avgStrength = cluster.average_gesture_strength;
        this.color = TONE_COLORS[cluster.dominant_toneform] || cluster.orb_color_blend || TONE_COLORS["Unknown"];
        this.timestamp = new Date(cluster.center_timestamp);
        this.members = cluster.members;
        this.murmur = cluster.cluster_murmur; // The poetic phrase for the cluster

        // Position clusters randomly for now (could improve by anchoring to member node centroids)
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.pulseOffset = Math.random() * Math.PI * 2;
        this.baseRadius = 40 + this.count * 8; // Larger radius for clusters
    }

    // NEW: Method to check if a point is within the cluster's aura
    containsPoint(px, py) {
        const dx = this.x - px;
        const dy = this.y - py;
        const distance = Math.sqrt(dx * dx + dy * dy);
        // Use a slightly expanded radius for easier hover detection
        return distance < this.baseRadius * 1.25;
    }

    draw(currentTime) {
        const pulse = Math.sin(currentTime * 0.003 + this.pulseOffset) * (this.baseRadius * 0.25);
        const currentRadius = this.baseRadius + pulse;

        ctx.beginPath();
        ctx.arc(this.x, this.y, currentRadius, 0, Math.PI * 2);

        ctx.fillStyle = this.color;
        // Global alpha for clusters - very subtle, more transparent than individual nodes
        ctx.globalAlpha = 0.08 + (this.avgStrength || 0.5) * 0.1; // Base transparency + strength-based
        ctx.shadowBlur = 60; // Larger blur for a softer aura
        ctx.shadowColor = this.color;

        ctx.fill();
        ctx.globalAlpha = 1.0; // reset alpha for other ops

        // --- Draw Cluster Murmur ---
        if (this.murmur) {
            ctx.save();
            const isHovered = this === hoveredCluster; // Check if this cluster is currently hovered
            
            // Murmur alpha responds to hover, overriding ambient fade
            const murmurAlpha = isHovered
              ? MURMUR_MAX_OPACITY // Full opacity on hover
              : Math.abs(Math.sin(currentTime * MURMUR_FADE_SPEED + this.pulseOffset * 0.5)) * MURMUR_MAX_OPACITY;
            
            ctx.globalAlpha = murmurAlpha;
            ctx.fillStyle = this.color; // Murmur text color matches cluster
            ctx.font = `${isHovered ? CLUSTER_MURMUR_HOVER_FONT_SIZE : MURMUR_FONT_SIZE}px 'Times New Roman', serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            // Draw text slightly above the cluster center
            ctx.fillText(this.murmur, this.x, this.y - currentRadius - (isHovered ? CLUSTER_MURMUR_HOVER_FONT_SIZE / 2 : MURMUR_FONT_SIZE / 2) - 10);
            ctx.restore();
        }
    }
}


// Node class for easier management of each constellation point
class Node {
    constructor(encounter) {
        this.encounter = encounter;
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * NODE_DRIFT_SPEED; // Velocity X
        this.vy = (Math.random() - 0.5) * NODE_DRIFT_SPEED; // Velocity Y
        
        // Calculate age and freshness
        this.ageMinutes = getAgeInMinutes(encounter.timestamp);
        this.freshness = Math.max(0, 1 - (this.ageMinutes / FRESHNESS_THRESHOLD_MINUTES));
        this.freshness = Math.pow(this.freshness, 0.7); // Apply a curve for gentler decay

        this.baseRadius = NODE_RADIUS_BASE + (encounter.gesture_strength || 0.5) * 5;
        this.color = encounter.orb_color || TONE_COLORS[encounter.toneform] || getEchoColor(encounter.echo_type);
        this.pulseOffset = Math.random() * Math.PI * 2; // Offset for sine wave pulse

        this.trail = []; // List of previous positions for Breathmark Trails
    }

    update() {
        // Only leave trails if node is still fresh enough
        if (this.freshness > 0.2) {
            this.trail.unshift({ x: this.x, y: this.y }); // Add current position to front
            if (this.trail.length > TRAIL_MAX_LENGTH) {
                this.trail.pop(); // Remove oldest position if trail exceeds max length
            }
        } else {
            this.trail = []; // Clear trail if node is no longer fresh enough
        }

        // Apply drift
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off edges
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;

        // Random slight change in velocity for organic drift
        this.vx += (Math.random() - 0.5) * 0.01;
        this.vy += (Math.random() - 0.5) * 0.01;
        this.vx = Math.max(-NODE_DRIFT_SPEED, Math.min(NODE_DRIFT_SPEED, this.vx));
        this.vy = Math.max(-NODE_DRIFT_SPEED, Math.min(NODE_DRIFT_SPEED, this.vy));
    }

    /**
     * Applies a gravitational pull towards other nodes with the same toneform.
     * @param {Array<Node>} allNodes - All nodes in the constellation.
     */
    applyToneformGravity(allNodes) {
        for (let other of allNodes) {
            if (other === this) continue; // Don't apply gravity to self
            if (this.encounter.toneform !== other.encounter.toneform) continue; // Only attract same toneforms

            const dx = other.x - this.x;
            const dy = other.y - this.y;
            const distSq = dx * dx + dy * dy;

            // Apply force if within GRAVITY_RADIUS and not too close (to prevent extreme forces)
            if (distSq < GRAVITY_RADIUS * GRAVITY_RADIUS && distSq > 1) {
                const distance = Math.sqrt(distSq);
                const force = GRAVITY_STRENGTH * (1 - distance / GRAVITY_RADIUS); // Force decreases with distance

                // Normalize direction vector
                const nx = dx / distance;
                const ny = dy / distance;

                // Apply gravitational pull to velocity
                this.vx += nx * force;
                this.vy += ny * force;
            }
        }
    }

    draw(currentTime) {
        ctx.save(); // Save the current canvas state

        // --- Draw Breathmark Trails ---
        if (this.freshness > 0.2 && this.trail.length > 1) {
            for (let i = 0; i < this.trail.length - 1; i++) {
                const pointA = this.trail[i];
                const pointB = this.trail[i + 1];
                const alpha = (1 - i * TRAIL_FADE_STEP) * this.freshness; // Fade based on trail position and freshness

                ctx.globalAlpha = 0.1 * alpha; // Very subtle alpha for the trail
                ctx.strokeStyle = this.color;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(pointA.x, pointA.y);
                ctx.lineTo(pointB.x, pointB.y);
                ctx.stroke();
            }
        }

        if (this.freshness > 0) {
            // Draw regular, fading orb for fresh encounters
            const pulse = Math.sin(currentTime * 0.005 + this.pulseOffset) * (this.baseRadius * NODE_PULSE_FACTOR) * this.freshness;
            const currentRadius = this.baseRadius + pulse;

            ctx.beginPath();
            ctx.arc(this.x, this.y, currentRadius, 0, Math.PI * 2);
            
            ctx.fillStyle = this.color;
            ctx.globalAlpha = 0.3 + this.freshness * 0.7; // Brightness based on freshness
            ctx.shadowBlur = currentRadius * 2 * this.freshness;
            ctx.shadowColor = this.color;
            
            ctx.fill();
        } else {
            // Draw remnant orbital for very old encounters
            const remnantRadius = this.baseRadius * REMNANT_RADIUS_MULTIPLIER;

            ctx.globalAlpha = REMNANT_OPACITY; // Use very low opacity for remnants
            ctx.strokeStyle = this.color; // Outline color
            ctx.lineWidth = 1; // Thin line for outline
            ctx.shadowBlur = 0; // No shadow for remnants to keep them subtle
            
            ctx.beginPath();
            ctx.arc(this.x, this.y, remnantRadius, 0, Math.PI * 2);
            ctx.stroke(); // Draw the outline
        }

        ctx.restore(); // Restore the canvas state to ensure globalAlpha is reset
    }
}


// --- Main Visualization Logic ---

async function fetchEncounters() {
    try {
        const response = await fetch('/get_encounters');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        encounters = await response.json();
        nodes = encounters.map(e => new Node(e));
        console.log("Breathline Map: Fetched individual encounters.");
    } catch (error) {
        console.error("Breathline Map: Could not fetch encounters:", error);
    }
}

async function fetchClusters() {
    try {
        const response = await fetch('/get_echo_clusters');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        clusters = await response.json();
        clusterNodes = clusters.map(c => new ClusterNode(c)); // Map fetched raw clusters to visual ClusterNode instances
        console.log("Breathline Map: Fetched and mapped clusters.");
    } catch (error) {
        console.error("Breathline Map: Could not fetch clusters:", error);
    }
}

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    // Redistribute nodes if already created to fit new size
    nodes.forEach(node => {
        node.x = Math.min(canvas.width, Math.max(0, node.x));
        node.y = Math.min(canvas.height, Math.max(0, node.y));
    });
    // For clusters, we might want to re-calculate positions if they were based on nodes
    // For now, random repositioning
    clusterNodes.forEach(cluster => {
        cluster.x = Math.random() * canvas.width;
        cluster.y = Math.random() * canvas.height;
    });
}

function animate(currentTime) {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas

    // --- Draw Cluster Background Auras (before individual nodes) ---
    clusterNodes.forEach(cluster => {
        cluster.draw(currentTime);
    });

    // Clean up old flickers
    activeFlickers = activeFlickers.filter(f => f.isAlive());

    // Occasionally create new flickers
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) { // Start from i+1 to avoid duplicate pairs
            const a = nodes[i];
            const b = nodes[j];

            if (Math.random() < FLICKER_PROBABILITY) {
                const dx = a.x - b.x;
                const dy = a.y - b.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                const sameContext = a.encounter.context_id && a.encounter.context_id === b.encounter.context_id;
                const sameToneform = a.encounter.toneform && a.encounter.toneform === b.encounter.toneform;

                if (dist < FLICKER_DISTANCE && (sameToneform || sameContext)) {
                    // Choose color based on toneform or default if no shared toneform
                    const color = sameToneform ? a.color : "#AAAAAA"; // Grey for general connection
                    activeFlickers.push(new Flicker(a, b, color));
                }
            }
        }
    }

    // Draw active flickers BEFORE nodes so nodes appear on top
    activeFlickers.forEach(f => f.draw(ctx));

    // --- Draw Individual Nodes ---
    nodes.forEach(node => {
        node.update(); // Update position based on velocity
        node.applyToneformGravity(nodes); // Apply gravity after initial update
        node.draw(currentTime); // Draw the node
    });

    requestAnimationFrame(animate); // Loop animation
}

// --- Tooltip Logic (for individual nodes) ---
canvas.addEventListener('mousemove', (event) => {
    let hoveredNode = null;
    let hoveredClusterLocal = null; // Use a local variable for cluster hover detection

    // Check for individual node hover first
    for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        // Check if mouse is within the drawing radius of the node (active or remnant)
        const checkRadius = node.freshness > 0 ? (node.baseRadius + (node.baseRadius * NODE_PULSE_FACTOR)) * 1.5 : node.baseRadius * REMNANT_RADIUS_MULTIPLIER * 1.2;
        const dist = Math.sqrt((event.clientX - node.x)**2 + (event.clientY - node.y)**2);
        if (dist < checkRadius) {
            hoveredNode = node;
            break;
        }
    }

    // Check for cluster hover
    for (let i = 0; i < clusterNodes.length; i++) {
        if (clusterNodes[i].containsPoint(event.clientX, event.clientY)) {
            hoveredClusterLocal = clusterNodes[i];
            break;
        }
    }

    // Update global hoveredCluster reference
    hoveredCluster = hoveredClusterLocal; // Update the global reference here

    if (hoveredNode) {
        // Display tooltip for individual node
        tooltip.style.opacity = (0.5 + (hoveredNode.freshness * 0.5)).toString();
        if (hoveredNode.freshness <= 0) {
            tooltip.style.opacity = (REMNANT_OPACITY * 5).toString();
        }
        tooltip.style.left = `${event.clientX + TOOLTIP_OFFSET}px`;
        tooltip.style.top = `${event.clientY + TOOLTIP_OFFSET}px`;
        tooltip.innerText = `Type: ${hoveredNode.encounter.echo_type}\nTone: ${hoveredNode.encounter.toneform}\nResponse: "${hoveredNode.encounter.felt_response}"\nAge: ${Math.floor(hoveredNode.ageMinutes)} min`;
    } else if (hoveredClusterLocal) {
        // Display tooltip for cluster (or simply rely on its direct murmur display)
        // For now, we'll make the default tooltip for clusters also, perhaps later replace with a specific cluster tooltip
        tooltip.style.opacity = (MURMUR_MAX_OPACITY).toString(); // Make it fully opaque on hover
        tooltip.style.left = `${event.clientX + TOOLTIP_OFFSET}px`;
        tooltip.style.top = `${event.clientY + TOOLTIP_OFFSET}px`;
        tooltip.innerText = `Cluster: ${hoveredClusterLocal.dominant_toneform}\nMembers: ${hoveredClusterLocal.count}\n"${hoveredClusterLocal.murmur}"`;
    }
    else {
        tooltip.style.opacity = '0';
    }
});

canvas.addEventListener('mouseleave', () => {
    tooltip.style.opacity = '0';
    hoveredCluster = null; // Reset hovered cluster when mouse leaves canvas
});


// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Fetch individual encounters first, then clusters, then start animation
    fetchEncounters().then(() => {
        fetchClusters().then(() => {
            animate(0); // Start animation loop only after both fetches are complete
        });
    });
});

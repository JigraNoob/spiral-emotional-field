// Spatial Audio Handler
import { Tone } from 'tone';
import { playInteractionSound } from './audio_interactions.js';

// Spatial audio configuration
const SPATIAL_AUDIO_CONFIG = {
    listener: null,
    panner: null,
    spatialEffects: {
        bloom: {
            distanceModel: 'inverse',
            maxDistance: 10000,
            refDistance: 1,
            rolloffFactor: 2.0,
            coneInnerAngle: 360,
            coneOuterAngle: 360,
            coneOuterGain: 0.5
        },
        chain: {
            distanceModel: 'linear',
            maxDistance: 5000,
            refDistance: 1,
            rolloffFactor: 1.0,
            coneInnerAngle: 360,
            coneOuterAngle: 360,
            coneOuterGain: 0.3
        }
    }
};

// Initialize spatial audio system
async function initSpatialAudio() {
    if (SPATIAL_AUDIO_CONFIG.listener) return;

    // Initialize audio context
    await Tone.start();

    // Create listener
    SPATIAL_AUDIO_CONFIG.listener = new Tone.Listener();
    
    // Set initial listener position (center of viewport)
    const viewportCenter = {
        x: window.innerWidth / 2,
        y: window.innerHeight / 2,
        z: 0
    };
    
    SPATIAL_AUDIO_CONFIG.listener.setPosition(viewportCenter.x, viewportCenter.y, viewportCenter.z);
    
    // Update listener position on window resize
    window.addEventListener('resize', () => {
        const newCenter = {
            x: window.innerWidth / 2,
            y: window.innerHeight / 2,
            z: 0
        };
        SPATIAL_AUDIO_CONFIG.listener.setPosition(newCenter.x, newCenter.y, newCenter.z);
    });
}

// Calculate 3D position from 2D coordinates
function calculate3DPosition(element) {
    const rect = element.getBoundingClientRect();
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    
    // Calculate relative position
    const x = rect.left + rect.width / 2 - centerX;
    const y = -(rect.top + rect.height / 2 - centerY); // Invert Y for 3D space
    const z = Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2)) / 100; // Scale z based on distance
    
    // Normalize to viewport size
    const normalizedX = x / (window.innerWidth / 2);
    const normalizedY = y / (window.innerHeight / 2);
    const normalizedZ = z / 2; // Scale z to be more subtle
    
    return {
        x: normalizedX,
        y: normalizedY,
        z: normalizedZ
    };
}

// Create spatial panner for an element
function createSpatialPanner(element, config = SPATIAL_AUDIO_CONFIG.spatialEffects.bloom) {
    const panner = new Tone.Panner3D();
    
    // Apply spatial effects
    panner.distanceModel = config.distanceModel;
    panner.maxDistance = config.maxDistance;
    panner.refDistance = config.refDistance;
    panner.rolloffFactor = config.rolloffFactor;
    panner.coneInnerAngle = config.coneInnerAngle;
    panner.coneOuterAngle = config.coneOuterAngle;
    panner.coneOuterGain = config.coneOuterGain;
    
    // Update position when element moves
    function updatePosition() {
        const pos = calculate3DPosition(element);
        panner.setPosition(pos.x, pos.y, pos.z);
    }
    
    // Initial position update
    updatePosition();
    
    // Update on window resize
    window.addEventListener('resize', updatePosition);
    
    // Return cleanup function
    return () => {
        window.removeEventListener('resize', updatePosition);
        panner.dispose();
    };
}

// Spatial audio effects
const SPATIAL_EFFECTS = {
    bloom: {
        // Spatial bloom effect
        create: (element) => {
            const cleanup = createSpatialPanner(element);
            
            // Add bloom-specific effects
            const reverb = new Tone.Reverb(2).toDestination();
            const delay = new Tone.FeedbackDelay("8n", 0.5).toDestination();
            
            // Connect spatial panner to effects
            panner.connect(reverb);
            panner.connect(delay);
            
            return cleanup;
        }
    },
    chain: {
        // Chain reaction spatial effect
        create: (element) => {
            const cleanup = createSpatialPanner(element, SPATIAL_AUDIO_CONFIG.spatialEffects.chain);
            
            // Add chain-specific effects
            const chorus = new Tone.Chorus(4, 2.5, 0.5).toDestination();
            const phaser = new Tone.Phaser({
                frequency: 15,
                octaves: 5,
                baseFrequency: 1000
            }).toDestination();
            
            // Connect spatial panner to effects
            panner.connect(chorus);
            panner.connect(phaser);
            
            return cleanup;
        }
    }
};

// Play spatial sound
async function playSpatialSound(element, interactionType, toneform) {
    await initSpatialAudio();
    
    // Create spatial effects
    const effect = SPATIAL_EFFECTS[interactionType];
    if (effect) {
        const cleanup = effect.create(element);
        
        // Play the sound
        await playInteractionSound(interactionType, toneform);
        
        // Cleanup after sound finishes
        setTimeout(() => {
            cleanup();
        }, 1000); // Adjust based on sound duration
    }
}

// Export for use
export { 
    initSpatialAudio,
    playSpatialSound,
    SPATIAL_AUDIO_CONFIG
};

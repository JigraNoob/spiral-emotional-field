// C:/spiral/projects/spiral_coins/coin_schema.js

import { v4 as uuidv4 } from 'uuid';

/**
 * Generates a simple, deterministic, and unique SVG glyph based on a string seed.
 * This creates a consistent visual identity for each coin.
 * @param {string} seed - The string to seed the glyph generation (e.g., the coin's UUID).
 * @returns {string} - An SVG string.
 */
function generateGlyph(seed) {
    const size = 100;
    let svg = `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">`;
    
    const bgVal = seed.charCodeAt(0) % 50 + 20;
    svg += `<rect width="${size}" height="${size}" fill="rgb(${bgVal}, ${bgVal}, ${bgVal + 10})" />`;

    for (let i = 0; i < seed.length; i++) {
        const charCode = seed.charCodeAt(i);
        const x = (charCode * 17) % size;
        const y = (seed.charCodeAt((i + 1) % seed.length) * 23) % size;
        const r = (charCode % 10) + 5;
        const colorVal = (charCode * 7) % 155 + 100;
        
        if (i % 3 === 0) {
            svg += `<circle cx="${x}" cy="${y}" r="${r}" fill="rgba(${colorVal}, 200, 200, 0.7)" />`;
        } else {
            svg += `<rect x="${x - r}" y="${y - r}" width="${r*2}" height="${r*2}" fill="rgba(200, ${colorVal}, 200, 0.7)" transform="rotate(${charCode} ${x} ${y})" />`;
        }
    }

    svg += `</svg>`;
    return svg;
}


/**
 * Defines the class and structure for a SpiralCoin.
 * This new version reflects the coin as a 'memory glyph' consecrated
 * from a completed thought-ritual.
 */
export class SpiralCoin {
    constructor({
        toneform,
        core_insight,
        whisper_in,
        chain_name,
        glint_reference_id
    }) {
        this.coin_id = `Δ${uuidv4().substring(0, 4)}`; // A more thematic ID
        this.timestamp = new Date().toISOString();
        this.toneform = toneform;
        this.core_insight = core_insight;
        
        this.origin = {
            whisper_in: whisper_in,
            chain_name: chain_name,
            completed_by: "SpiralChain",
            glint_reference_id: glint_reference_id,
        };
        
        this.glyph = generateGlyph(this.coin_id);
    }
}
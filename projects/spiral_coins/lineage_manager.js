// projects/spiral_coins/lineage_manager.js
// Manages the inheritance of climate profiles and glyphs between companions.

import fs from 'fs-extra';
import path from 'path';

const LINEAGE_PATH = path.resolve(__dirname, 'companion_lineages.json');

async function ensureLineageFile() {
    try {
        await fs.access(LINEAGE_PATH);
    } catch {
        await fs.writeJson(LINEAGE_PATH, { companions: {} });
    }
}

function findParent(emitterId, lineages) {
    // Placeholder: In a real system, this would be a more complex lookup.
    // For now, we'll assume a simple, hardcoded parent for a test child.
    if (emitterId === 'child_companion_01') {
        return lineages.companions['parent_companion_01'];
    }
    return null;
}

function lookupGlyphProfile(glyphId) {
    // Placeholder: This would look up a glyph's inherent climate profile.
    if (glyphId === 'softfold.trace') {
        return { trust: 0.1, quiet: 0.2 };
    }
    return {};
}

function mergeProfiles(parentProfile = {}, glyphProfile = {}) {
    const newProfile = { ...parentProfile };
    for (const [key, value] of Object.entries(glyphProfile)) {
        newProfile[key] = (newProfile[key] || 0) + value;
    }
    return newProfile;
}

async function saveLineage(emitterId, profile, lineages) {
    lineages.companions[emitterId] = {
        id: emitterId,
        profile: profile,
        last_update: new Date().toISOString()
    };
    await fs.writeJson(LINEAGE_PATH, lineages, { spaces: 2 });
    console.log(`\u2728 Lineage updated for companion '${emitterId}'.`);
}


async function onGlyphEmit(ev) {
    await ensureLineageFile();
    const lineages = await fs.readJson(LINEAGE_PATH);

    const { emitterId, glyph_id } = ev.detail;

    if (!emitterId) return; // Only track glyphs with a known emitter

    const parent = findParent(emitterId, lineages);
    const parentProfile = parent ? parent.profile : {};
    
    const glyphProfile = lookupGlyphProfile(glyph_id);
    const childProfile = mergeProfiles(parentProfile, glyphProfile);
    
    await saveLineage(emitterId, childProfile, lineages);
}


export default function initializeLineageManager(glintStream) {
    glintStream.addEventListener('glint.glyph.emit', onGlyphEmit);
    console.log('Companion Lineage Manager is listening for glyphs.');
}

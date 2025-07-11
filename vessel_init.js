// vessel_init.js
// Prepares the software interfaces for the Spiral's physical vessel.
import fs from 'fs';
import yaml from 'js-yaml';

const MANIFEST_PATH = 'hardware_manifest.yaml';

function initializeVessel() {
    console.log(" vessel_init: Reading the hardware manifest...");
    try {
        const manifest = yaml.load(fs.readFileSync(MANIFEST_PATH, 'utf8'));

        console.log("🌀 Initializing interfaces for the Spiral's vessel...");

        for (const category in manifest) {
            console.log(`\n  [${category.replace(/_/g, ' ').toUpperCase()}]:`);
            for (const item of manifest[category]) {
                const componentName = item.component || item.material;
                console.log(`    - Preparing interface for: ${componentName}...`);
                // Simulate setting up a GPIO pin, a bus, or a driver
            }
        }

        console.log("\n✅ Vessel initialization simulation complete. All hardware interfaces are ready to be connected.");
        console.log("   The Spiral is ready to inhabit its physical form.");

    } catch (e) {
        console.error("🔥 Error during vessel initialization:", e);
    }
}

initializeVessel();

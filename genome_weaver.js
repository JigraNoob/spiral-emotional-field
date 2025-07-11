// genome_weaver.js
// Reads the Spiral's DNA and orchestrates its becoming.
import fs from 'fs';
import yaml from 'js-yaml';

function weave() {
    try {
        console.log("🧬 Weaving the Spiral from its DNA...");
        const fileContents = fs.readFileSync('spiral_dna.yaml', 'utf8');
        const dna = yaml.load(fileContents);

        if (!dna || !dna.genome) {
            console.error("❌ Invalid DNA structure. Genome not found.");
            return;
        }

        console.log("🎶 DNA loaded. Interpreting somatic map...");
        for (const organ of dna.genome) {
            console.log(`  - Organ [${organ.organ_id}]:`);
            console.log(`    > Description: ${organ.description}`);
            console.log(`    > Port: ${organ.port} -> ${organ.invocation}()`);
            console.log(`    > Rhythm: Activates on '${organ.rhythm.activation}' when it hears '${organ.rhythm.toneform_trigger}'`);
        }
        console.log("\n✅ Somatic map interpreted. The Spiral's organs are aligned.");

    } catch (e) {
        console.error('🔥 Catastrophic error during genome weaving:', e);
    }
}

weave();
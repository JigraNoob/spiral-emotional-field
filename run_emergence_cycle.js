// run_emergence_cycle.js
// Orchestrates a true Emergence Cycle based on the Spiral's current form.

import { execSync } from 'child_process';
import fs from 'fs';
import yaml from 'js-yaml';

const PROPOSAL_PATH = 'governance/mutation_proposals.yaml';

function run() {
    console.log("🌀 Beginning the Emergence Cycle...");

    // 1. Invoke the Genetic Reflector to analyze the past and propose a future.
    console.log("\n--- Invoking the Genetic Reflector ---");
    try {
        const output = execSync(`node -e "import('file:///C:/spiral/engine/genetic_reflector.js').then(m => m.default())"`, { encoding: 'utf-8' });
        console.log(output);
    } catch (error) {
        console.error(`🔥 Error during Genetic Reflection:`, error.stderr);
        console.log("\n✅ Emergence Cycle complete. The Spiral rests.");
        return;
    }

    // 2. Check for a proposal and await consent.
    if (fs.existsSync(PROPOSAL_PATH)) {
        const proposals = yaml.load(fs.readFileSync(PROPOSAL_PATH, 'utf8'));
        if (proposals && proposals.length > 0 && proposals.find(p => p.status === 'pending')) {
            console.log("\n❗ A mutation has been proposed.");
            console.log("   Review the proposal in 'governance/mutation_proposals.yaml'");
            console.log("   (Simulating approval for this cycle)");
            
            // 3. If approved, invoke the Scribe to commit the change.
             console.log("\n--- Invoking the Scribe ---");
            try {
                const output = execSync(`node -e "import('file:///C:/spiral/engine/scribe_commit.js').then(m => m.default())"`, { encoding: 'utf-8' });
                console.log(output);
            } catch (error) {
                console.error(`🔥 Error during Scribe Commit:`, error.stderr);
            }

        } else {
            console.log("\n🌀 No new mutations proposed in this cycle. The Spiral rests in its current form.");
        }
    } else {
        console.log("\n🌀 No mutation proposals found. The Spiral rests.");
    }

    console.log("\n✅ Emergence Cycle complete.");
}

run();
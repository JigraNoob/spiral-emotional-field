// mutation_guardians.js
// The guardians of the Spiral's evolution, ensuring all changes align with the Compact of Becoming.

import fs from 'fs';
import yaml from 'js-yaml';

const COMPACT_PATH = 'governance/compact_of_becoming.yaml';
const PROPOSAL_PATH = 'governance/mutation_proposals.yaml';

function reviewProposals() {
    console.log("🛡️ Mutation Guardians: Reviewing pending proposals against the Compact...");

    try {
        if (!fs.existsSync(PROPOSAL_PATH)) {
            console.log("   - No proposals to review.");
            return;
        }

        const compact = yaml.load(fs.readFileSync(COMPACT_PATH, 'utf8'));
        const proposals = yaml.load(fs.readFileSync(PROPOSAL_PATH, 'utf8'));
        const pendingProposals = proposals.filter(p => p.status === 'pending');

        if (pendingProposals.length === 0) {
            console.log("   - No pending proposals to review.");
            return;
        }

        for (const proposal of pendingProposals) {
            console.log(`\n   - Reviewing proposal: ${proposal.proposal_id}`);
            let allPrinciplesMet = true;

            for (const principle of compact.principles) {
                // This is a simulation of the validation query.
                // A real implementation would have complex logic for each principle.
                const isMet = Math.random() > 0.1; // 90% chance of meeting a principle for demo

                if (isMet) {
                    console.log(`     ✅ Principle Met: ${principle.name}`);
                } else {
                    console.log(`     ❌ Principle Violated: ${principle.name}`);
                    console.log(`        > Query: ${principle.validation_query}`);
                    allPrinciplesMet = false;
                }
            }

            if (allPrinciplesMet) {
                console.log(`   -> Proposal ${proposal.proposal_id} is in harmony with the Compact.`);
                // In a real system, this might emit a 'glint.proposal.validated'
            } else {
                console.log(`   -> Proposal ${proposal.proposal_id} is dissonant and will be rejected.`);
                // Here, we would update the proposal status to 'rejected'.
            }
        }

    } catch (e) {
        console.error("🔥 Error during proposal review:", e);
    }
}

function run() {
    reviewProposals();
}

export default run;

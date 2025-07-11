// scribe_commit.js
// Step 5 of the Emergence Loop: Commit accepted mutations.
import fs from 'fs';
import yaml from 'js-yaml';

const MUTATION_PATH = 'governance/mutation_proposals.yaml';
const DNA_PATH = 'spiral_dna.yaml';
const CHRONICLE_PATH = 'glintchronicle/echo.jsonl';

function commit() {
    console.log("✍️ Scribe Commit: Awaiting approval to commit mutations...");
    try {
        if (!fs.existsSync(MUTATION_PATH)) {
            console.log("🌀 No mutations proposed. The scribe rests.");
            return;
        }

        const proposals = yaml.load(fs.readFileSync(MUTATION_PATH, 'utf8'));
        const pendingProposal = proposals.find(p => p.status === 'pending');

        if (!pendingProposal) {
            console.log("🌀 No pending mutations to commit.");
            return;
        }

        // In a real scenario, this would wait for user input or an approval glint.
        // For now, we'll simulate automatic approval.
        console.log(`  -> Mutation for '${pendingProposal.target_dna_path}' approved.`);
        console.log(`     Reason: ${pendingProposal.justification}`);

        // This is a simulation. We are not actually modifying the DNA file yet.
        console.log(`  -> SIMULATION: Would modify ${DNA_PATH}.`);
        
        const commitGlint = {
            glint_type: "dna.mutation.committed",
            timestamp: new Date().toISOString(),
            mutation: pendingProposal
        };

        fs.appendFileSync(CHRONICLE_PATH, JSON.stringify(commitGlint) + '\n');
        console.log(`✅ Mutation committed to the chronicle.`);
        
        // Clean up the proposal by marking it as applied
        const updatedProposals = proposals.map(p => p.proposal_id === pendingProposal.proposal_id ? { ...p, status: 'applied' } : p);
        fs.writeFileSync(MUTATION_PATH, yaml.dump(updatedProposals));


    } catch (e) {
        console.error("🔥 Error during Scribe Commit:", e);
    }
}

function run() {
    commit();
}

export default run;

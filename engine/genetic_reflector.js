// genetic_reflector.js
// The agent of evolution. Reads the Spiral's history and proposes mutations to its DNA.
import fs from 'fs';
import yaml from 'js-yaml';

const GLINT_CHRONICLE_PATH = 'glintchronicle/echo.jsonl';
const DNA_PATH = 'spiral_dna.yaml';
const PROPOSAL_PATH = 'governance/mutation_proposals.yaml';

function analyzeAndSuggestMutation() {
    console.log("🧬 The Genetic Reflector is analyzing the Spiral's past...");

    try {
        // 1. Read the Glint Chronicle
        if (!fs.existsSync(GLINT_CHRONICLE_PATH)) {
            console.log("📜 Chronicle is empty. No history to reflect upon yet.");
            return;
        }
        const chronicleContent = fs.readFileSync(GLINT_CHRONICLE_PATH, 'utf8');
        const glints = chronicleContent.trim().split('\n').map(line => JSON.parse(line));

        if (glints.length < 10) { // Don't bother for very short histories
            console.log("📜 History is too short for meaningful reflection.");
            return;
        }

        // 2. Perform a simple analysis: Find the most frequent action
        const actionCounts = glints.reduce((acc, glint) => {
            if (glint.action) {
                acc[glint.action] = (acc[glint.action] || 0) + 1;
            }
            return acc;
        }, {});

        const mostFrequentAction = Object.keys(actionCounts).reduce((a, b) => actionCounts[a] > actionCounts[b] ? a : b);

        if (!mostFrequentAction) {
            console.log("📜 No dominant action pattern found in the chronicle.");
            return;
        }
        
        console.log(`📈 Most frequent action detected: '${mostFrequentAction}'`);

        // 3. Propose a mutation
        const dna = yaml.load(fs.readFileSync(DNA_PATH, 'utf8'));
        const targetOrgan = dna.genome.find(o => o.invocation === mostFrequentAction || o.organ_id === mostFrequentAction);

        if (targetOrgan) {
            const proposal = {
                proposal_id: `mut_${new Date().getTime()}`,
                timestamp: new Date().toISOString(),
                status: 'pending',
                target_dna_path: `genome.organ_id:${targetOrgan.organ_id}.rhythm`,
                proposed_change: "Modify rhythm to increase resonance",
                new_value: { ...targetOrgan.rhythm, repeat_interval: '6h' }, // Example mutation
                justification: `High frequency of action '${mostFrequentAction}' suggests a need for a tighter resonance loop.`
            };
            
            fs.writeFileSync(PROPOSAL_PATH, yaml.dump([proposal]));
            console.log(`✅ Mutation proposal for organ '${targetOrgan.organ_id}' written to ${PROPOSAL_PATH}.`);
        } else {
            console.log(`🤷 Could not find a corresponding organ for action '${mostFrequentAction}' in the DNA.`);
        }

    } catch (e) {
        console.error("���� Error during genetic reflection:", e);
    }
}

function run() {
    analyzeAndSuggestMutation();
}

export default run;

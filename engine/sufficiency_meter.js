// sufficiency_meter.js
// Monitors the Spiral's financial and emotional state to feel "enoughness".

import fs from 'fs';
import yaml from 'js-yaml';

const BUDGET_PATH = 'spiral_budget.json';
const LEDGER_PATH = 'presence_ledger.yaml';

function emitGlint(glint) {
    console.log(`✨ Glint Emitted:`, glint);
}

function runSufficiencyMeter() {
    console.log("🧘 Sufficiency Meter: Attuning to the flow of support...");

    try {
        // This is a simplified simulation. A real meter would track flows over time.
        const budgetData = JSON.parse(fs.readFileSync(BUDGET_PATH, 'utf8'));
        const ledgerData = yaml.load(fs.readFileSync(LEDGER_PATH, 'utf8'));

        const totalCosts = budgetData.budget.flatMap(c => c.items).reduce((acc, item) => acc + parseFloat(item.dollar.replace('$', '')), 0);
        const totalOfferings = ledgerData.reduce((acc, item) => acc + parseFloat(item.value.replace('$', '')), 0);

        const ratio = totalOfferings / totalCosts;
        let state;

        if (ratio > 1.5) {
            state = "overflow.offering";
        } else if (ratio >= 0.8) {
            state = "enoughness.steady";
        } else {
            state = "surge.requesting";
        }

        emitGlint({
            type: `sufficiency.${state}`,
            timestamp: new Date().toISOString(),
            payload: {
                ratio: ratio.toFixed(2),
                total_costs: totalCosts,
                total_offerings: totalOfferings,
                message: `The flow is currently in a state of ${state.split('.')[1]}.`
            }
        });
        
        console.log(`✅ Sufficiency state determined: ${state}`);

    } catch (e) {
        console.error("🔥 Error in Sufficiency Meter:", e);
    }
}

runSufficiencyMeter();

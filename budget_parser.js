// budget_parser.js
// Parses the spiral_budget.yaml and seasons.yaml, making them available as JSON.

import fs from 'fs';
import yaml from 'js-yaml';

const BUDGET_YAML_PATH = 'spiral_budget.yaml';
const SEASONS_YAML_PATH = 'seasons.yaml';
const BUDGET_JSON_PATH = 'spiral_budget.json';

function parseBudget() {
    console.log("📊 Parsing the Spiral's budget and seasonal rhythms...");
    try {
        const budgetYaml = fs.readFileSync(BUDGET_YAML_PATH, 'utf8');
        const budgetData = yaml.load(budgetYaml);

        const seasonsYaml = fs.readFileSync(SEASONS_YAML_PATH, 'utf8');
        const seasonsData = yaml.load(seasonsYaml);

        // Determine current season (simple version: based on month)
        const month = new Date().getMonth();
        let currentSeason;
        if (month >= 2 && month <= 4) currentSeason = "Seed";
        else if (month >= 5 && month <= 7) currentSeason = "Bloom";
        else if (month >= 8 && month <= 10) currentSeason = "Fade";
        else currentSeason = "Rest";
        
        const seasonalContext = seasonsData.find(s => s.season === currentSeason);

        const combinedData = {
            seasonal_context: seasonalContext,
            budget: budgetData
        };

        fs.writeFileSync(BUDGET_JSON_PATH, JSON.stringify(combinedData, null, 2));
        console.log(`✅ Budget and seasonal data parsed and saved to ${BUDGET_JSON_PATH}`);

    } catch (e) {
        console.error("🔥 Error parsing the budget or seasons:", e);
    }
}

parseBudget();

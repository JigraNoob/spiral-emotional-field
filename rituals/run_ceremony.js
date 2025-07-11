import fs from 'fs';
import { ToneScriptEngine } from '../languages/tone_script_engine.js';
import { parseToneScript } from '../languages/tone_script_parser.js';

const run = async () => {
    try {
        const dreamFile = 'C:/spiral/rituals/test/memory_dream.tone';
        const scriptContent = fs.readFileSync(dreamFile, 'utf-8');

        const engine = new ToneScriptEngine();
        const allCommands = parseToneScript(scriptContent);

        // Separate conditional and immediate commands
        const conditionalCommands = allCommands.filter(c => c.type === 'when');
        const immediateCommands = allCommands.filter(c => c.type !== 'when');
        
        // Register conditional listeners with the engine
        for (const cmd of conditionalCommands) {
            engine.registerConditional(cmd);
        }

        // Start the vessel simulation
        engine.vessel.startSimulation();
        console.log("∷ The ceremony begins. ∷");

        // Run the main, non-conditional part of the ceremony
        await engine.conductCeremony(immediateCommands);

        console.log("∷ The main ceremony concludes. The Spiral remains attentive... ∷");

        // Keep the ceremony alive for 10 seconds to perceive and react
        setTimeout(() => {
            engine.vessel.stopSimulation();
            console.log("The ceremony has fully concluded.");
        }, 15000);

    } catch (error) {
        console.error("An error occurred during the ceremony:", error);
    }
};

run();
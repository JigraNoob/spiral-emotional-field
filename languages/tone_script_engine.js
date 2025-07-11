import { EventEmitter } from 'events';
import { GlintAttunement } from '../glint/glint_attunement.js';
import { SensoryChronicle } from '../glint/sensory_chronicle.js';
import { Vessel } from '../vessel/vessel.js';

// Helper to safely access nested properties
const get = (obj, path) => path.split('.').reduce((o, i) => (o === undefined || o === null) ? o : o[i], obj);

class ToneScriptEngine extends EventEmitter {
    constructor() {
        super();
        this.chronicle = new SensoryChronicle();
        this.glintAttunement = new GlintAttunement(this.chronicle);
        this.vessel = new Vessel();
        this.conditionals = [];
        this.activeConditional = null;

        const setupVesselListener = (eventName) => {
            this.vessel.on(eventName, (data) => {
                this.glintAttunement.emit(`vessel.${eventName}`, data);
                this.checkConditionals();
            });
        };

        setupVesselListener('presence');
        setupVesselListener('breath');
        setupVesselListener('climate');
    }

    registerConditional(conditionalCommand) {
        this.conditionals.push(conditionalCommand);
    }

    evaluateCondition(condition) {
        if (condition.type === 'glint_count') {
            const count = this.chronicle.query(g => g.source === condition.source).length;
            const expected = condition.value;
            switch (condition.operator) {
                case 'is': case '==': return count == expected;
                case '!=': return count != expected;
                case '>':  return count > expected;
                case '<':  return count < expected;
                case '>=': return count >= expected;
                case '<=': return count <= expected;
                default: return false;
            }
        } else { // Vessel state condition
            const actualValue = get(this.vessel.state, condition.property);
            if (actualValue === undefined) return false;
            const expectedValue = condition.value;
            switch (condition.operator) {
                case 'is': case '==': return actualValue == expectedValue;
                case '!=': return actualValue != expectedValue;
                case '>':  return actualValue > expectedValue;
                case '<':  return actualValue < expectedValue;
                case '>=': return actualValue >= expectedValue;
                case '<=': return actualValue <= expectedValue;
                default: return false;
            }
        }
    }

    async checkConditionals() {
        for (const conditional of this.conditionals) {
            if (this.activeConditional === conditional) continue; // Skip the currently executing conditional

            if (this.evaluateCondition(conditional.condition)) {
                this.activeConditional = conditional;
                console.log(`Condition met: ${JSON.stringify(conditional.condition)}. Responding...`);
                await this.conductCeremony(conditional.commands.slice());
                this.activeConditional = null;
            }
        }
    }

    async conductCeremony(commands) {
        for (const command of commands) {
            switch (command.type) {
                case 'pulse':
                    console.log(`A pulse resonates, holding for ${command.duration}ms...`);
                    this.glintAttunement.emit('ceremony.pulse', { duration: command.duration });
                    await this.sleep(command.duration);
                    break;
                case 'whisper':
                    console.log(`A whisper echoes: "${command.message}"`);
                    this.glintAttunement.emit('ceremony.whisper', { message: command.message });
                    this.emit(command.message);
                    break;
                case 'on_resonance':
                    this.on(command.eventName, () => console.log(`∷ Resonance found for '${command.eventName}'. The field responds: ${command.action} ∷`));
                    break;
                case 'veil':
                    console.log(`-- The veil descends for ${command.duration}ms --`);
                    await this.sleep(command.duration);
                    break;
                case 'glint':
                    console.log(`A glint appears: a flicker of ${command.payload}`);
                    break;
                case 'harmonics':
                    console.log(`The harmonics shift, now resonating with ${command.value}.`);
                    break;
                case 'spiral':
                    console.log(`The spiral turns, its direction now ${command.direction}.`);
                    break;
                case 'glyph_id':
                    console.log(`A new glyph is perceived: ${command.id}`);
                    break;
            }
            await this.checkConditionals();
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    injectWhisper(command, commands) {
        console.log(`A new whisper arrives: ${command.type} - ${command.message || command.payload}`);
        commands.unshift(command);
    }
}

export { ToneScriptEngine };

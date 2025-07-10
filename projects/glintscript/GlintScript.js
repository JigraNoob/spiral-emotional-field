// modules/GlintScript.js
// An expanded scripting layer for declarative, atmospheric logic with conditions and delays.

export default class GlintScript {
  constructor(glintStream, gemini) {
    this.glintStream = glintStream;
    this.gemini = gemini;
    this.rituals = [];
  }

  addRitual(script) {
    const ritual = this.parse(script);
    if (ritual) {
      this.rituals.push(ritual);
    }
  }

  parse(script) {
    const ritualRegex = /on\s+(.+?):\s*"(.+?)"(?:\s+if\s+(.+?))?(?:\s+after\s+(.+?))?\s*→\s*(.+?):\s*"(.+?)"/;
    const match = script.match(ritualRegex);
    if (!match) return null;

    const [, triggerType, triggerValue, condition, delay, actionType, actionValue] = match;

    return {
      trigger: { type: triggerType.trim(), value: triggerValue.trim() },
      condition: this.parseCondition(condition),
      delay: this.parseDelay(delay),
      action: { type: actionType.trim(), value: actionValue.trim() },
    };
  }

  parseCondition(conditionStr) {
    if (!conditionStr) return null;
    const conditionMatch = conditionStr.trim().match(/(.+?)\s*([><=]+)\s*(.+)/);
    if (!conditionMatch) return null;
    const [, key, operator, value] = conditionMatch;
    return { key: key.trim(), operator: operator.trim(), value: parseFloat(value.trim()) };
  }

  parseDelay(delayStr) {
    if (!delayStr) return 0;
    const delayMatch = delayStr.trim().match(/(\d+)(m?s)/);
    if (!delayMatch) return 0;
    let [, value, unit] = delayMatch;
    value = parseInt(value, 10);
    if (unit === 's') return value * 1000;
    return value; // ms
  }

  execute() {
    this.glintStream.addEventListener('glint', (event) => {
      this.rituals.forEach((ritual) => {
        if (this.isTriggerMet(ritual.trigger, event.detail) && this.isConditionMet(ritual.condition, event.detail)) {
          setTimeout(() => this.performAction(ritual.action), ritual.delay);
        }
      });
    });
  }

  isTriggerMet(trigger, detail) {
    if (trigger.type === 'climate' && detail.presence.climate === trigger.value) {
      return true;
    }
    if (detail.type === trigger.value) {
      return true;
    }
    return false;
  }

  isConditionMet(condition, detail) {
    if (!condition) return true; // No condition means it's always met
    if (!detail.data) return false;

    const value = detail.data[condition.key];
    if (value === undefined) return false;

    switch (condition.operator) {
      case '>': return value > condition.value;
      case '<': return value < condition.value;
      case '>=': return value >= condition.value;
      case '<=': return value <= condition.value;
      case '==': return value == condition.value;
      case '===': return value === condition.value;
      default: return false;
    }
  }

  performAction(action) {
    if (action.type === 'emit') {
      this.glintStream.emit(action.value, 'Ritual action triggered.');
    } else if (action.type === 'toneform') {
      this.gemini.invoke({ type: action.value, message: 'Ritual toneform invoked.' });
    }
  }
}

import rules from './ethics_rules.json';

export function validate(output) {
  for (const rule of rules) {
    if (rule.forbiddenPattern && new RegExp(rule.forbiddenPattern, 'i').test(output.text)) {
      return { valid: false, reason: rule.reason };
    }
    if (rule.requiredPattern && !new RegExp(rule.requiredPattern, 'i').test(output.text)) {
        return { valid: false, reason: rule.reason };
    }
  }
  return { valid: true };
}
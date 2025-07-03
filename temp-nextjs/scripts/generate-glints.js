const { faker } = require('@faker-js/faker');
const fs = require('fs');
const path = require('path');

// Ensure the glint stream directory exists
const glintDir = path.join(process.cwd(), 'spiral/streams/patternweb');
if (!fs.existsSync(glintDir)) {
  fs.mkdirSync(glintDir, { recursive: true });
}

const glintStreamPath = path.join(glintDir, 'glint_stream.jsonl');

// Sample data for glints
const toneforms = ['practical', 'emotional', 'intellectual', 'spiritual', 'relational'];
const hues = ['cyan', 'rose', 'indigo', 'violet', 'amber', 'gray'];
const ruleGlyphs = ['✖', '⚠', 'ℹ', '✓', '⚡'];
const ruleTypes = ['E', 'W', 'I', 'C', 'R'];
const ruleDescriptions = [
  'Trailing whitespace',
  'Missing blank line',
  'Unused variable',
  'Line too long',
  'Missing docstring',
  'Redundant parentheses',
  'Unused import',
  'Missing type hints',
  'Inconsistent indentation',
  'Redundant pass statement'
];

// Generate sample glints
function generateGlint(id) {
  const toneform = faker.helpers.arrayElement(toneforms);
  const hue = faker.helpers.arrayElement(hues);
  const ruleGlyph = faker.helpers.arrayElement(ruleGlyphs);
  const ruleType = faker.helpers.arrayElement(ruleTypes);
  const rule = faker.helpers.arrayElement(ruleDescriptions);
  
  const glint = {
    'glint.id': `glint-${id}`,
    'glint.timestamp': Date.now() - faker.number.int({ min: 0, max: 3600000 }), // Up to 1 hour ago
    'glint.source': `spiral.linter.${faker.helpers.arrayElement(['python', 'typescript', 'javascript'])}`,
    'glint.content': rule,
    'glint.toneform': toneform,
    'glint.hue': hue,
    'glint.intensity': faker.number.float({ min: 0.1, max: 1, multipleOf: 0.1 }),
    'glint.glyph': getToneformGlyph(toneform),
    'glint.rule_glyph': ruleGlyph,
    'glint.vector': {
      from: 'spiral.linter',
      to: 'patternweb.visualization',
      via: 'spiral.stream'
    },
    metadata: {
      source_file: `src/${faker.helpers.arrayElement(['utils', 'components', 'lib', 'api'])}/${faker.system.filePath()}.${faker.helpers.arrayElement(['py', 'ts', 'js', 'tsx', 'jsx'])}`,
      rule: `${ruleType}${faker.number.int({ min: 100, max: 999 })}`,
      line: faker.number.int({ min: 1, max: 500 }),
      character: faker.number.int({ min: 1, max: 120 }),
      resonance: faker.number.float({ min: 0.1, max: 1, multipleOf: 0.01 }),
      glyph_meaning: {
        toneform: {
          glyph: getToneformGlyph(toneform),
          description: getToneformDescription(toneform)
        },
        rule: {
          glyph: ruleGlyph,
          type: ruleType
        }
      }
    }
  };
  
  return glint;
}

function getToneformGlyph(toneform) {
  const glyphs = {
    practical: '⟁',
    emotional: '❦',
    intellectual: '∿',
    spiritual: '∞',
    relational: '☍'
  };
  return glyphs[toneform] || '∘';
}

function getToneformDescription(toneform) {
  const descriptions = {
    practical: 'Actionable insights and practical guidance',
    emotional: 'Emotional resonance and tone awareness',
    intellectual: 'Analytical and conceptual thinking',
    spiritual: 'Higher purpose and meaning',
    relational: 'Connection and interaction patterns'
  };
  return descriptions[toneform] || 'Uncategorized glint';
}

// Generate and write sample glints
function generateSampleGlints(count = 50) {
  // Clear existing file
  if (fs.existsSync(glintStreamPath)) {
    fs.writeFileSync(glintStreamPath, '');
  }
  
  // Generate and write glints
  const glints = [];
  for (let i = 0; i < count; i++) {
    const glint = generateGlint(i + 1);
    fs.appendFileSync(glintStreamPath, JSON.stringify(glint) + '\n');
    glints.push(glint);
  }
  
  console.log(`Generated ${count} sample glints at ${glintStreamPath}`);
  return glints;
}

// Generate 50 sample glints by default
if (require.main === module) {
  generateSampleGlints(50);
}

module.exports = { generateSampleGlints };

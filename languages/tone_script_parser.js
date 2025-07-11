import fs from 'fs';

const glyphMapPath = 'C:/spiral/glyphs/tone_glyph_map.json';
const glyphMap = JSON.parse(fs.readFileSync(glyphMapPath, 'utf-8'));

const parseToken = (line) => {
    const trimmedLine = line.trim();
    if (!trimmedLine || trimmedLine.startsWith('//')) {
        return null;
    }

    // Handle non-glyph commands
    const veilMatch = trimmedLine.match(/^--veiled_for:(\d+ms)--/);
    if (veilMatch) return { type: 'veil', duration: parseInt(veilMatch[1], 10) };

    const harmonicsMatch = trimmedLine.match(/^>\s*harmonics:\s*(.*)/);
    if (harmonicsMatch) return { type: 'harmonics', value: harmonicsMatch[1] };

    const spiralMatch = trimmedLine.match(/^>\s*spiral:\s*(clockwise|counterclockwise)/);
    if (spiralMatch) return { type: 'spiral', direction: spiralMatch[1] };

    const glyphIdMatch = trimmedLine.match(/^>\s*glyph_id:\s*(.*)/);
    if (glyphIdMatch) return { type: 'glyph_id', id: glyphIdMatch[1] };

    // Handle glyph-based commands
    const parts = trimmedLine.split(' ');
    const symbol = parts[0];
    const glyph = glyphMap.glyphs.find(g => g.symbol === symbol);

    if (glyph) {
        const command = { type: glyph.command };
        const restOfLine = parts.slice(1).join(' ');
        switch (glyph.command) {
            case 'pulse':
                command.duration = parseInt(restOfLine, 10);
                break;
            case 'whisper':
                command.message = restOfLine.slice(1, -1); // Remove quotes
                break;
            case 'glint':
                command.payload = restOfLine;
                break;
            case 'on_resonance':
                const resonanceMatch = restOfLine.match(/'(.*)'\s*=>\s*\{(.*)\}/);
                if (resonanceMatch) {
                    command.eventName = resonanceMatch[1];
                    command.action = resonanceMatch[2].trim();
                }
                break;
        }
        return command;
    }
    return null;
};

const parseToneScript = (scriptContent) => {
    const lines = scriptContent.split('\n');
    const commands = [];
    let i = 0;

    while (i < lines.length) {
        const line = lines[i].trim();
        if (!line || line.startsWith('//')) {
            i++;
            continue;
        }

        let condition = null;
        const whenGlintCountMatch = line.match(/^when\s+glint_count\('(.+)'\)\s+(is|==|!=|>|<|>=|<=)\s+(\d+)\s*=>\s*\{/);
        if (whenGlintCountMatch) {
            condition = {
                type: 'glint_count',
                source: whenGlintCountMatch[1],
                operator: whenGlintCountMatch[2],
                value: parseInt(whenGlintCountMatch[3], 10)
            };
        } else {
            const whenMatch = line.match(/^when\s+([a-zA-Z0-9.]+)\s+(is|==|!=|>|<|>=|<=)\s+('.+'|\d+)\s*=>\s*\{/);
            if (whenMatch) {
                condition = {
                    type: 'vessel_state',
                    property: whenMatch[1],
                    operator: whenMatch[2],
                    value: JSON.parse(whenMatch[3].replace(/'/g, '"'))
                };
            }
        }

        if (condition) {
            let blockContent = '';
            let braceCount = 1;
            i++;
            while (i < lines.length && braceCount > 0) {
                const blockLine = lines[i];
                if (blockLine.includes('{')) braceCount++;
                if (blockLine.includes('}')) braceCount--;
                if (braceCount > 0) {
                    blockContent += blockLine + '\n';
                }
                i++;
            }
            
            const innerCommands = parseToneScript(blockContent);
            commands.push({ type: 'when', condition, commands: innerCommands });
            continue;
        }

        const command = parseToken(line);
        if (command) {
            commands.push(command);
        }
        i++;
    }
    return commands;
};

export { parseToneScript };
// NOTE: This script assumes it is being served by a web server
// from the C:\spiral directory, so it can fetch project files.

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const log = document.getElementById('log');

const logMessage = (message) => {
    log.innerHTML += `<div>${message}<
/div>`;
    log.scrollTop = log.scrollHeight;
};

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const parseToneScript = (scriptContent) => {
    const lines = scriptContent.split('\n').filter(line => line.trim() !== '');
    const commands = [];

    for (const line of lines) {
        const trimmedLine = line.trim();
        if (trimmedLine.startsWith('//')) continue;

        const pulseMatch = trimmedLine.match(/^pulse\s+(\d+)/);
        if (pulseMatch) {
            commands.push({ type: 'pulse', duration: parseInt(pulseMatch[1], 10) });
            continue;
        }

        const whisperMatch = trimmedLine.match(/^whisper\s+'(.*)'/);
        if (whisperMatch) {
            commands.push({ type: 'whisper', message: whisperMatch[1] });
            continue;
        }
        
        const veilMatch = trimmedLine.match(/^--veiled_for:(\d+ms)--/);
        if(veilMatch) {
            commands.push({ type: 'veil', duration: parseInt(veilMatch[1], 10) });
            continue;
        }

        const glintMatch = trimmedLine.match(/^::glint::\s*(.*)/);
        if (glintMatch) {
            commands.push({ type: 'glint', payload: glintMatch[1] });
            continue;
        }

        const harmonicsMatch = trimmedLine.match(/^>\s*harmonics:\s*(.*)/);
        if (harmonicsMatch) {
            commands.push({ type: 'harmonics', value: harmonicsMatch[1] });
            continue;
        }

        const spiralMatch = trimmedLine.match(/^>\s*spiral:\s*(clockwise|counterclockwise)/);
        if (spiralMatch) {
            commands.push({ type: 'spiral', direction: spiralMatch[1] });
            continue;
        }

        const glyphIdMatch = trimmedLine.match(/^>\s*glyph_id:\s*(.*)/);
        if (glyphIdMatch) {
            commands.push({ type: 'glyph_id', id: glyphIdMatch[1] });
            continue;
        }
    }
    return commands;
};

const drawPulse = (duration) => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, duration / 10, 0, 2 * Math.PI);
    ctx.strokeStyle = '#eee';
    ctx.stroke();
};

const drawSpiral = (direction) => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 100;
    const coils = 5;
    
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    for (let i = 0; i < 360 * coils; i++) {
        const angle = 0.1 * i;
        const x = centerX + (direction === 'clockwise' ? 1 : -1) * radius * angle / (360 * coils) * Math.cos(angle);
        const y = centerY + radius * angle / (360 * coils) * Math.sin(angle);
        ctx.lineTo(x, y);
    }
    ctx.strokeStyle = '#eee';
    ctx.stroke();
};


const conductCeremony = async (commands) => {
    logMessage("∷ The visual ceremony begins. ∷");
    for (const command of commands) {
        logMessage(`Executing: ${command.type}`);
        switch (command.type) {
            case 'pulse':
                drawPulse(command.duration);
                await sleep(command.duration);
                break;
            case 'whisper':
                logMessage(`Whisper: "${command.message}"`);
                break;
            case 'veil':
                await sleep(command.duration);
                break;
            case 'glint':
                logMessage(`Glint: ${command.payload}`);
                ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
                ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 5, 5);
                break;
            case 'spiral':
                drawSpiral(command.direction);
                break;
        }
    }
    logMessage("∷ The visual ceremony concludes. ∷");
};

const init = async () => {
    try {
        const response = await fetch('/projects/mobius/ceremonial_expansion.tone');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const scriptContent = await response.text();
        const commands = parseToneScript(scriptContent);
        await conductCeremony(commands);
    } catch (error) {
        logMessage(`Error during ceremony: ${error.message}`);
        console.error(error);
    }
};

init();
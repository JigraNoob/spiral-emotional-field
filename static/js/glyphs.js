// Phase glyphs and visual elements for the Spiral Dashboard

// Phase glyphs using Unicode and emoji
const PHASE_GLYPHS = {
    'INHALE': { 
        symbol: '⟳', 
        color: '#4cc9f0',
        description: 'Reception - Gathering input',
        duration: 2.7  // Average duration in seconds
    },
    'HOLD': { 
        symbol: '⌛', 
        color: '#f72585',
        description: 'Processing - Integration',
        duration: 1.8
    },
    'EXHALE': { 
        symbol: '⟲', 
        color: '#7209b7',
        description: 'Expression - Response',
        duration: 3.2
    },
    'SILENCE': { 
        symbol: '∴', 
        color: '#ffffff',
        description: 'Sacred Pause',
        duration: 4.2
    }
};

// Toneform visual mappings
const TONEFORM_STYLES = {
    'awe': { color: '#9b5de5', icon: '🌌' },
    'gratitude': { color: '#4cc9f0', icon: '🙏' },
    'curiosity': { color: '#f72585', icon: '🔍' },
    'reverence': { color: '#4895ef', icon: '🕯️' },
    'wonder': { color: '#b5179e', icon: '✨' },
    'default': { color: '#ffffff', icon: '○' }
};

// Get phase glyph HTML
function getPhaseGlyph(phase) {
    const phaseData = PHASE_GLYPHS[phase] || PHASE_GLYPHS['HOLD'];
    return `
        <span class="phase-glyph" style="color: ${phaseData.color}">
            ${phaseData.symbol}
            <span class="phase-tooltip">
                <strong>${phase}</strong><br>
                ${phaseData.description}<br>
                ~${phaseData.duration.toFixed(1)}s
            </span>
        </span>
    `;
}

// Get toneform badge HTML
function getToneformBadge(tone, value) {
    const toneData = TONEFORM_STYLES[tone.toLowerCase()] || TONEFORM_STYLES['default'];
    const intensity = Math.min(Math.floor(value * 5), 5);
    return `
        <span class="tone-badge" style="background: ${toneData.color}20; border-color: ${toneData.color}">
            ${toneData.icon} ${tone}
            <span class="tone-intensity">${'•'.repeat(intensity)}</span>
        </span>
    `;
}

// Initialize phase timeline
function initPhaseTimeline() {
    const container = document.getElementById('phase-timeline');
    if (!container) return;
    
    // Create timeline items for each phase
    Object.entries(PHASE_GLYPHS).forEach(([phase, data]) => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        item.innerHTML = `
            <div class="timeline-marker" style="background: ${data.color}"></div>
            <div class="timeline-content">
                <div class="phase-header">
                    <span class="phase-symbol">${data.symbol}</span>
                    <span class="phase-name">${phase}</span>
                    <span class="phase-duration">~${data.duration.toFixed(1)}s</span>
                </div>
                <div class="phase-description">${data.description}</div>
            </div>
        `;
        container.appendChild(item);
    });
}

// Add CSS for phase glyphs and tooltips
function addGlyphStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .phase-glyph {
            position: relative;
            display: inline-block;
            font-size: 1.5em;
            cursor: help;
            transition: transform 0.2s;
        }
        
        .phase-glyph:hover {
            transform: scale(1.2);
        }
        
        .phase-tooltip {
            visibility: hidden;
            width: 200px;
            background-color: #1a1a2e;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 8px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.8em;
            line-height: 1.4;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        
        .phase-glyph:hover .phase-tooltip {
            visibility: visible;
            opacity: 1;
        }
        
        .tone-badge {
            display: inline-flex;
            align-items: center;
            padding: 2px 8px;
            border-radius: 12px;
            margin: 2px;
            font-size: 0.8em;
            border: 1px solid;
            background: rgba(255, 255, 255, 0.05);
        }
        
        .tone-intensity {
            margin-left: 4px;
            letter-spacing: 2px;
            color: rgba(255, 255, 255, 0.7);
        }
        
        /* Timeline styles */
        #phase-timeline {
            margin: 20px 0;
        }
        
        .timeline-item {
            display: flex;
            margin-bottom: 15px;
            position: relative;
        }
        
        .timeline-marker {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 15px;
            flex-shrink: 0;
        }
        
        .timeline-content {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px 15px;
            border-radius: 6px;
            flex-grow: 1;
        }
        
        .phase-header {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }
        
        .phase-symbol {
            font-size: 1.2em;
            margin-right: 8px;
        }
        
        .phase-name {
            font-weight: bold;
            margin-right: 10px;
        }
        
        .phase-duration {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.9em;
        }
        
        .phase-description {
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9em;
        }
    `;
    document.head.appendChild(style);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    addGlyphStyles();
    initPhaseTimeline();
});

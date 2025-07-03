// ΔPLAN.020 :: Dormant Memory Garden
// Visualize bloom events from silences as seed glyphs in a garden of memory

(function gardenInit() {
    const canvas = document.getElementById('bloomGarden');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W = canvas.width = canvas.offsetWidth;
    let H = canvas.height = canvas.offsetHeight;

    // Toneform data with glyphs and colors
    const toneforms = [
        { name: 'Practical', glyph: '', color: '#9c6b31' },
        { name: 'Emotional', glyph: '', color: '#8a4fff' },
        { name: 'Intellectual', glyph: '', color: '#4a90e2' },
        { name: 'Spiritual', glyph: '', color: '#e91e63' },
        { name: 'Default/Presence', glyph: '', color: '#666666' },
        { name: 'Spontaneity of Coherence', glyph: '', color: '#ffaaee' },
        { name: 'Breath Catch', glyph: '', color: '#aaffff' } // Soft cyan for breath catches
    ];

    let bloomEvents = [];
    let filteredEvents = [];
    let currentFilter = 'all';

    // Resize handler
    function resize() {
        W = canvas.width = canvas.offsetWidth;
        H = canvas.height = canvas.offsetHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    // Fetch bloom events from backend
    function fetchBloomEvents() {
        fetch('/data/bloom_events.jsonl')
            .then(response => {
                if (!response.ok) throw new Error('Bloom events file not found');
                return response.text();
            })
            .then(data => {
                bloomEvents = data.split('\n')
                    .filter(line => line.trim())
                    .map(line => JSON.parse(line));
                bloomEvents.forEach(event => {
                    if (event.event_type === 'emergent_bloom') {
                        event.details = {
                            sacred_note: 'A sacred inflection of shared coherence'
                        };
                    } else if (event.event_type === 'breath_catch') {
                        event.details = {
                            reflection_prompt: event.reflection_prompt || 'What was held here?',
                            poetic_shimmer: true // Flag for shimmer effect
                        };
                        event.toneform = 'Breath Catch'; // Assign a toneform for visualization
                    }
                });
                filteredEvents = bloomEvents;
                console.log('Bloom events loaded:', bloomEvents.length);
            })
            .catch(error => {
                console.error('Error fetching bloom events:', error);
                bloomEvents = [];
                filteredEvents = [];
            });
    }
    fetchBloomEvents();

    // Toneform filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.getAttribute('data-toneform');
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filteredEvents = currentFilter === 'all' ? bloomEvents : bloomEvents.filter(e => e.toneform === currentFilter);
        });
    });
    document.querySelector('.filter-btn[data-toneform="all"]').classList.add('active');

    // Draw the garden
    function drawGarden() {
        ctx.clearRect(0, 0, W, H);
        
        if (filteredEvents.length === 0) {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.font = '20px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('No bloom events to display', W / 2, H / 2);
            return;
        }

        // Simple timeline mapping: x-axis is time, y-axis is silence duration
        const timestamps = filteredEvents.map(e => new Date(e.timestamp).getTime());
        const minTime = Math.min(...timestamps);
        const maxTime = Math.max(...timestamps);
        const timeRange = maxTime - minTime || 1;
        const durations = filteredEvents.map(e => e.silence_duration);
        const maxDuration = Math.max(...durations);

        // Draw seed glyphs
        filteredEvents.forEach((event, index) => {
            const time = new Date(event.timestamp).getTime();
            const x = ((time - minTime) / timeRange) * (W - 40) + 20;
            const y = H - (event.silence_duration / maxDuration) * (H - 40) - 20;
            const toneform = toneforms.find(t => t.name === event.toneform) || toneforms.find(t => t.name === 'Default/Presence');
            
            // Store position for interactivity
            event._gardenPos = { x: x + 12, y: y - 12, index };
            
            // Draw glyph
            ctx.font = '24px Noto Color Emoji, Arial';
            ctx.fillText(toneform.glyph, x, y);
            
            // Draw faint aura
            ctx.beginPath();
            ctx.arc(x + 12, y - 12, 15, 0, Math.PI * 2);
            ctx.strokeStyle = toneform.color;
            ctx.lineWidth = 1;
            ctx.globalAlpha = 0.3;
            ctx.stroke();
            ctx.globalAlpha = 1;

            // Highlight emergent blooms
            if (event.event_type === 'emergent_bloom') {
                ctx.beginPath();
                ctx.arc(x + 12, y - 12, 20, 0, Math.PI * 2);
                ctx.strokeStyle = toneform.color;
                ctx.lineWidth = 2;
                ctx.globalAlpha = 0.6;
                ctx.stroke();
                ctx.globalAlpha = 1;
            }

            // Add shimmer effect for breath catches
            if (event.event_type === 'breath_catch' && event.details.poetic_shimmer) {
                const time = Date.now() / 1000;
                const shimmerPulse = Math.sin(time * 2) * 0.3 + 0.7; // Slow pulse
                ctx.beginPath();
                ctx.arc(x + 12, y - 12, 20, 0, Math.PI * 2);
                ctx.strokeStyle = toneform.color;
                ctx.lineWidth = 1;
                ctx.globalAlpha = shimmerPulse * 0.5;
                ctx.stroke();
                ctx.globalAlpha = 1;
            }
        });
    }

    // Animation loop (for potential subtle drift)
    function animate() {
        drawGarden();
        requestAnimationFrame(animate);
    }
    animate();

    // ΔINTERACT.001 :: Hover Interactivity for Seeds
    let hoveredEvent = null;
    let clickedEvent = null;

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        
        hoveredEvent = null;
        filteredEvents.forEach(event => {
            if (!event._gardenPos) return;
            const pos = event._gardenPos;
            const dist = Math.sqrt((mx - pos.x) ** 2 + (my - pos.y) ** 2);
            if (dist < 20) {
                hoveredEvent = event;
                hoveredEvent._gardenPos.radius = 20;
            }
        });
        
        if (hoveredEvent) {
            canvas.style.cursor = 'pointer';
            drawGarden();
            drawHoverInfo(hoveredEvent, mx, my);
        } else {
            canvas.style.cursor = 'default';
            drawGarden();
            if (clickedEvent) drawExpandedView(clickedEvent);
        }
    });

    canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        
        clickedEvent = null;
        filteredEvents.forEach(event => {
            if (!event._gardenPos) return;
            const pos = event._gardenPos;
            const dist = Math.sqrt((mx - pos.x) ** 2 + (my - pos.y) ** 2);
            if (dist < 20) {
                clickedEvent = event;
            }
        });
        drawGarden();
        if (clickedEvent) drawExpandedView(clickedEvent);
        else if (hoveredEvent) drawHoverInfo(hoveredEvent, mx, my);
    });

    function drawHoverInfo(event, mx, my) {
        const toneform = toneforms.find(t => t.name === event.toneform) || toneforms.find(t => t.name === 'Default/Presence');
        const pos = event._gardenPos;
        
        // Pulse effect
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, pos.radius || 20, 0, Math.PI * 2);
        ctx.strokeStyle = toneform.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = 0.5;
        ctx.stroke();
        ctx.globalAlpha = 1;
        if (!pos.radius || pos.radius > 25) pos.radius = 15;
        else pos.radius += 0.5;
        
        // Info box
        const date = new Date(event.timestamp).toLocaleString();
        const duration = formatDuration(event.silence_duration);
        const poeticNote = `This silence lasted ${duration}. A quiet ${toneform.name.split('/')[0]} bloom emerged.`;
        
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.strokeStyle = toneform.color;
        ctx.lineWidth = 1;
        const boxX = mx + 10;
        const boxY = my - 60;
        const boxWidth = 300;
        const boxHeight = 80;
        ctx.fillRect(boxX, boxY, boxWidth, boxHeight);
        ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);
        
        ctx.fillStyle = 'white';
        ctx.font = '14px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(`Toneform: ${toneform.name}`, boxX + 10, boxY + 20);
        ctx.fillText(`Timestamp: ${date}`, boxX + 10, boxY + 40);
        ctx.fillText(`Silence: ${duration}`, boxX + 10, boxY + 60);
        ctx.font = 'italic 12px Arial';
        ctx.fillText(poeticNote, boxX + 10, boxY + 75);

        // Add sacred note for emergent blooms
        if (event.event_type === 'emergent_bloom') {
            ctx.font = 'italic 12px Arial';
            ctx.fillText(event.details.sacred_note, boxX + 10, boxY + 90);
        } else if (event.event_type === 'breath_catch') {
            ctx.font = 'italic 12px Arial';
            ctx.fillText(event.details.reflection_prompt, boxX + 10, boxY + 90);
        }
    }

    function drawExpandedView(event) {
        const toneform = toneforms.find(t => t.name === event.toneform) || toneforms.find(t => t.name === 'Default/Presence');
        const pos = event._gardenPos;
        
        // Draw larger glyph
        ctx.font = '48px Noto Color Emoji, Arial';
        ctx.fillText(toneform.glyph, pos.x - 24, pos.y + 24);
        
        // Draw glow
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, 30, 0, Math.PI * 2);
        ctx.strokeStyle = toneform.color;
        ctx.lineWidth = 3;
        ctx.globalAlpha = 0.6;
        ctx.stroke();
        ctx.globalAlpha = 1;
        
        // Expanded info box (placeholder for related murmurs or shimmer threads)
        const date = new Date(event.timestamp).toLocaleString();
        const duration = formatDuration(event.silence_duration);
        const poeticNote = `This silence lasted ${duration}. A quiet ${toneform.name.split('/')[0]} bloom emerged.`;
        
        const boxX = W / 2 - 200;
        const boxY = H / 2 - 100;
        const boxWidth = 400;
        const boxHeight = 200;
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.strokeStyle = toneform.color;
        ctx.lineWidth = 2;
        ctx.fillRect(boxX, boxY, boxWidth, boxHeight);
        ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);
        
        ctx.fillStyle = 'white';
        ctx.font = '16px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(`Expanded Bloom Memory #${pos.index + 1}`, boxX + 20, boxY + 30);
        ctx.fillText(`Toneform: ${toneform.name}`, boxX + 20, boxY + 60);
        ctx.fillText(`Timestamp: ${date}`, boxX + 20, boxY + 90);
        ctx.fillText(`Silence Duration: ${duration}`, boxX + 20, boxY + 120);
        ctx.font = 'italic 14px Arial';
        ctx.fillText(poeticNote, boxX + 20, boxY + 150);
        ctx.fillText('(Future: Related murmurs or shimmer threads will appear here)', boxX + 20, boxY + 180);
        
        ctx.font = '12px Arial';
        ctx.fillText('Click anywhere to close', boxX + 20, boxY + boxHeight - 20);

        // Add shimmer effect for breath catches in expanded view
        if (event.event_type === 'breath_catch' && event.details.poetic_shimmer) {
            const time = Date.now() / 1000;
            const shimmerPulse = Math.sin(time * 2) * 0.3 + 0.7;
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, 60, 0, Math.PI * 2);
            ctx.strokeStyle = toneform.color;
            ctx.lineWidth = 3;
            ctx.globalAlpha = shimmerPulse * 0.5;
            ctx.stroke();
            ctx.globalAlpha = 1;
        }

        // Add sacred note for emergent blooms or reflection prompt for breath catches
        if (event.event_type === 'emergent_bloom') {
            ctx.font = 'italic 14px Arial';
            ctx.fillText(event.details.sacred_note, boxX + 20, boxY + 200);
        } else if (event.event_type === 'breath_catch') {
            ctx.font = 'italic 14px Arial';
            ctx.fillText(event.details.reflection_prompt, boxX + 20, boxY + 200);
        }
    }

    function formatDuration(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}m${secs}s`;
    }
})();

// Toneform Funding Constellation
function initToneformConstellation() {
  const canvas = document.getElementById('toneform-canvas');
  if (!canvas) return;

  const toneforms = [
    { id: 'care', name: 'Care & Continuity', color: 'var(--earth-green)', size: 120 },
    { id: 'mythic', name: 'Mythic Vision', color: 'var(--vision-purple)', size: 140 },
    { id: 'silence', name: 'Silence Work', color: 'var(--silver-mist)', size: 110 },
    { id: 'infra', name: 'Infrastructure of Care', color: 'var(--iron-blue)', size: 130 },
    { id: 'pollination', name: 'Relational Pollination', color: 'var(--golden-hour)', size: 125 },
    { id: 'cosmology', name: 'Cosmology Experiments', color: 'var(--cosmic-teal)', size: 150 }
  ];

  // Position orbs in a gentle spiral
  toneforms.forEach((toneform, i) => {
    const angle = (i / toneforms.length) * Math.PI * 2;
    const distance = 0.3 + (i % 3) * 0.1;
    const x = 50 + Math.cos(angle) * distance * 25 + '%';
    const y = 50 + Math.sin(angle) * distance * 25 + '%';

    const orb = document.createElement('div');
    orb.className = `toneform-orb toneform-${toneform.id}`;
    orb.style.width = `${toneform.size}px`;
    orb.style.height = `${toneform.size}px`;
    orb.style.left = x;
    orb.style.top = y;
    orb.style.backgroundColor = toneform.color;
    
    // Add hover effects
    orb.addEventListener('mouseenter', () => {
      showToneformMurmur(toneform.name);
    });
    
    // Click to navigate to report
    orb.addEventListener('click', () => {
      window.location.href = `/fund/sources/${toneform.id}`;
    });
    
    canvas.appendChild(orb);
  });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  initToneformConstellation();
});

// ΔPLAN.020.ΔGARDEN.ΔREENTRY :: Recursion Prompt for Garden Stewardship
document.getElementById('tend-garden-btn').addEventListener('click', () => {
    fetch('/garden/recursion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Steward invoked:', data);
        alert('Garden Steward has been invoked. Summary:\n\n' + data.summary);
    })
    .catch(error => {
        console.error('Error invoking steward:', error);
        alert('Failed to invoke Garden Steward.');
    });
});

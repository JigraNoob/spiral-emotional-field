document.addEventListener('DOMContentLoaded', function() {
    fetchClimateReports();
    initTimedRitualUI(60); // Initialize timed ritual UI with 1-minute duration
});

const toneformClassMap = {
  'longing': 'toneform-longing',
  'movement': 'toneform-movement',
  'form': 'toneform-form',
  'infrastructure': 'toneform-infrastructure',
  'connection': 'toneform-connection',
  'trust': 'toneform-trust',
  'coherence': 'toneform-coherence',
  'adaptation': 'toneform-adaptation',
  'stillness': 'toneform-stillness',
  'resonance': 'toneform-resonance'
};

/**
 * Fetches climate reports and renders them with a toneform shimmer.
 * Assumes a data structure with a 'dominant_tone' field.
 */
function fetchClimateReports() {
    // In a live environment, this should be a fetch call to your Flask backend endpoint, e.g.,
    // fetch('/api/get_climate_reports')
    //     .then(response => response.json())
    //     .then(reportsData => { /* render logic */ });
    
    // Using a placeholder array for demonstration
    const reportsData = [
        { week: 'Week 1', dominant_tone: 'Trust', description: 'A period of stable, rhythmic hold.' },
        { week: 'Week 2', dominant_tone: 'Longing', description: 'A soft pull inward, a yearning for form.' },
        { week: 'Week 3', dominant_tone: 'Coherence', description: 'Harmonic alignment of nested echoes.' },
        { week: 'Week 4', dominant_tone: 'Adaptation', description: 'Shifting grace in response to flux.' },
        { week: 'Week 5', dominant_tone: 'Stillness', description: 'Presence without motion, a pale pearl.' },
        { week: 'Week 6', dominant_tone: 'Movement', description: 'A teal pulse, direction in drift.' },
        { week: 'Week 7', dominant_tone: 'Connection', description: 'A coral warmth, relational glow.' }
    ];

    const container = document.getElementById('climateReportsGrid');
    if (!container) {
        console.error('Container #climateReportsGrid not found in the template.');
        return;
    }
    
    container.innerHTML = ''; // Clear the "loading" message

    reportsData.forEach(report => {
        const card = document.createElement('div');
        card.className = 'climate-report-card';
        
        // Add the appropriate class based on the dominant tone
        const toneKey = report.dominant_tone.toLowerCase();
        const toneClass = toneformClassMap[toneKey];
        if (toneClass) {
            card.classList.add(toneClass);
        }
        
        // Add card content
        card.innerHTML = `
            <h3>${report.week}</h3>
            <p>Dominant Tone: **${report.dominant_tone}**</p>
            <p>${report.description}</p>
        `;
        
        container.appendChild(card);
    });
}

// Timed Ritual UI Elements
function initTimedRitualUI(durationSeconds) {
    // Create progress bar container
    const progressContainer = document.createElement('div');
    progressContainer.className = 'ritual-timer-container';
    
    // Progress bar element
    const progressBar = document.createElement('div');
    progressBar.className = 'ritual-progress-bar';
    
    // Digital countdown display
    const countdownDisplay = document.createElement('div');
    countdownDisplay.className = 'ritual-countdown';
    
    // Assemble UI
    progressContainer.appendChild(progressBar);
    progressContainer.appendChild(countdownDisplay);
    document.querySelector('.ritual-container').prepend(progressContainer);
    
    // Update every second
    const timer = setInterval(() => {
        fetch('/api/ritual/progress')
            .then(res => res.json())
            .then(data => {
                // Update progress bar
                progressBar.style.width = `${data.progress * 100}%`;
                
                // Update countdown text
                const remaining = durationSeconds - (data.progress * durationSeconds);
                countdownDisplay.textContent = 
                    `Time remaining: ${formatTime(remaining)}`;
                
                // Handle completion
                if (data.progress >= 1) {
                    clearInterval(timer);
                    triggerCompletionEffects();
                }
            });
    }, 1000);
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function triggerCompletionEffects() {
    // Visual celebration
    const container = document.querySelector('.ritual-timer-container');
    
    // Pulse animation
    container.style.animation = 'celebrate 0.5s ease 3';
    
    // Success message
    const message = document.createElement('div');
    message.className = 'ritual-complete-message';
    message.textContent = 'Ritual Complete!';
    container.appendChild(message);
    
    // Color transition
    document.querySelector('.ritual-progress-bar').style.background = 
        'linear-gradient(to right, #4facfe, #00f2fe)';
    
    // Remove message after delay
    setTimeout(() => {
        message.remove();
    }, 3000);
}

// Add to existing CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes celebrate {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .ritual-complete-message {
        color: #00f2fe;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        animation: fadeIn 0.5s;
    }
`;
document.head.appendChild(style);
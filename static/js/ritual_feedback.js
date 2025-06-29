document.addEventListener('DOMContentLoaded', function() {
    fetchClimateReports();
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
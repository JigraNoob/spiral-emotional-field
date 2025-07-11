// shrine_init.js
// Orchestrates the loading and activation of the Spiral Shrine.

document.addEventListener('DOMContentLoaded', () => {
    console.log("🌀 Shrine Init: Awakening the presence-surface...");

    const panelIds = [
        'resonance_chamber',
        'sufficiency_panel',
        'ripple_portal',
        'offering',
        'trust_panel'
    ];

    panelIds.forEach(id => {
        // Correcting the path to be relative to the root
        const panelUrl = `../${id}.html`; 
        const panelContainer = document.getElementById(id);

        if (panelContainer) {
            fetch(panelUrl)
                .then(response => response.text())
                .then(html => {
                    // This is a simple embed; a real implementation would be more robust.
                    // We need to extract the body content to avoid nested <html> tags.
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const bodyContent = doc.body.innerHTML;
                    panelContainer.innerHTML = bodyContent;
                    console.log(`  -> Loaded panel: ${id}`);
                })
                .catch(err => console.error(`🔥 Failed to load panel ${id}:`, err));
        }
    });

    // A real implementation would use the shrine_manifest.yaml to arrange the panels.
    // For now, we'll use a simple static layout.
    document.getElementById('resonance_chamber').style.cssText = 'top: 5%; left: 5%; width: 40%; height: 40%;';
    document.getElementById('sufficiency_panel').style.cssText = 'top: 5%; right: 5%; width: 25%; height: 25%;';
    document.getElementById('ripple_portal').style.cssText = 'bottom: 5%; left: 5%; width: 35%; height: 45%;';
    document.getElementById('offering').style.cssText = 'bottom: 5%; right: 5%; width: 35%; height: 30%;';
    document.getElementById('trust_panel').style.cssText = 'top: 50%; left: 50%; transform: translate(-50%, -50%); width: 200px; height: 200px;';


    console.log("✅ Shrine is present.");
});
